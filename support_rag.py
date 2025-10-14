#!/usr/bin/env python3
from __future__ import annotations
import os, sys, json, shutil
from pathlib import Path
from typing import List, TypedDict, Dict, Any, Tuple
from pydantic import BaseModel
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, START, END
import gradio as gr

class Settings(BaseModel):
    OLLAMA_LLM: str = os.getenv("OLLAMA_LLM", "gemma3:1b")
    OLLAMA_EMBED: str = os.getenv("OLLAMA_EMBED", "nomic-embed-text")
    DOCS_DIR: Path = Path(os.getenv("DOCS_DIR", "./docs")).resolve()
    CHROMA_DIR: Path = Path(os.getenv("CHROMA_DIR", "./chroma_db")).resolve()
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 900))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 150))
    TOP_K: int = int(os.getenv("TOP_K", 4))
    STAMP_FILE: Path = Path(os.getenv("STAMP_FILE", "./chroma_db/index.stamp")).resolve()

class Indexer:
    def __init__(self, s: Settings):
        self.s = s
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=s.CHUNK_SIZE, chunk_overlap=s.CHUNK_OVERLAP, add_start_index=True, separators=["\n\n","\n"," ",""])
        self.emb = OllamaEmbeddings(model=s.OLLAMA_EMBED)

    def _iter_md(self) -> List[Path]:
        if not self.s.DOCS_DIR.exists():
            self.s.DOCS_DIR.mkdir(parents=True, exist_ok=True)
        return [p for p in self.s.DOCS_DIR.rglob("*") if p.is_file() and p.suffix.lower()==".md"]

    def latest_mtime(self) -> float:
        files = self._iter_md()
        if not files: return 0.0
        return max(p.stat().st_mtime for p in files)

    def read_stamp(self) -> float:
        if not self.s.STAMP_FILE.exists(): return -1.0
        try: return float(json.loads(self.s.STAMP_FILE.read_text()).get("latest_mtime",-1.0))
        except Exception: return -1.0

    def write_stamp(self, m: float) -> None:
        self.s.STAMP_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.s.STAMP_FILE.write_text(json.dumps({"latest_mtime": m}))

    def needs_reindex(self) -> bool:
        latest = self.latest_mtime()
        if not self.s.CHROMA_DIR.exists(): return True if latest>0 else False
        return latest > self.read_stamp()

    def _reset_store(self) -> None:
        if self.s.CHROMA_DIR.exists():
            shutil.rmtree(self.s.CHROMA_DIR)
        self.s.CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    def load_documents(self) -> List[Document]:
        docs: List[Document] = []
        for f in self._iter_md():
            try: text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception: continue
            docs.append(Document(page_content=text, metadata={"source_path":str(f),"source_name":f.name,"rel_path":str(f.relative_to(self.s.DOCS_DIR))}))
        return docs

    def reindex(self) -> None:
        raw = self.load_documents()
        if not raw: return
        chunks = self.splitter.split_documents(raw)
        self._reset_store()
        vs = Chroma(collection_name="rag_md", embedding_function=self.emb, persist_directory=str(self.s.CHROMA_DIR))
        vs.add_documents(chunks)
        self.write_stamp(self.latest_mtime())

    def ensure_index(self) -> None:
        if self.needs_reindex(): self.reindex()

class RAGState(TypedDict):
    question: str
    docs: List[Document]
    context: str
    answer: str

class RagAgent:
    def __init__(self, s: Settings):
        self.s = s
        self.emb = OllamaEmbeddings(model=s.OLLAMA_EMBED)
        self.llm = ChatOllama(model=s.OLLAMA_LLM, temperature=0.2)

    def retriever(self) -> Chroma:
        return Chroma(collection_name="rag_md", embedding_function=self.emb, persist_directory=str(self.s.CHROMA_DIR))

    def node_retrieve(self, state: RAGState) -> RAGState:
        r = self.retriever().as_retriever(search_kwargs={"k": self.s.TOP_K})
        docs = r.invoke(state["question"])
        return {**state, "docs": docs}

    def _fmt(self, docs: List[Document]) -> str:
        lines=[]
        for i,d in enumerate(docs,1):
            src = d.metadata.get("rel_path") or d.metadata.get("source_name") or d.metadata.get("source_path")
            lines.append(f"[Doc {i}] ({src})\n{d.page_content}")
        return "\n\n".join(lines)

    def node_synthesize(self, state: RAGState) -> RAGState:
        ctx = self._fmt(state.get("docs",[])) if state.get("docs") else ""
        system = ("Eres un agente de mesa de ayuda para tiendas de FashionPark. Da instrucciones rápidas en listas con acciones de 60–120 segundos y validaciones. Empieza con un resumen en una línea. Si falta un dato, pídele al usuario exactamente ese dato y ofrece una alternativa de verificación. Cierra con listo/no listo y próximos pasos. Incluye al final fuentes entre paréntesis con nombres de archivos.")
        user = f"Ticket:\n{state['question']}\n\nContexto:\n{ctx}"
        res = self.llm.invoke([("system",system),("user",user)])
        ans = res.content if hasattr(res,"content") else str(res)
        return {**state,"context":ctx,"answer":ans}

    def graph(self):
        g = StateGraph(RAGState)
        g.add_node("retrieve", self.node_retrieve)
        g.add_node("synthesize", self.node_synthesize)
        g.add_edge(START,"retrieve")
        g.add_edge("retrieve","synthesize")
        g.add_edge("synthesize",END)
        return g.compile()

    def ask(self, q: str) -> Dict[str,Any]:
        app = self.graph()
        fs: RAGState = app.invoke({"question": q})
        srcs=[]
        for d in fs.get("docs",[]):
            s = d.metadata.get("rel_path") or d.metadata.get("source_name") or d.metadata.get("source_path")
            if s and s not in srcs: srcs.append(s)
        return {"answer":fs["answer"],"sources":srcs}

class SupportApp:
    def __init__(self):
        self.s = Settings()
        self.idx = Indexer(self.s)
        self.agent = RagAgent(self.s)
        self.idx.ensure_index()

    def ensure(self): self.idx.ensure_index()

    def ask(self, q: str) -> Dict[str,Any]:
        self.ensure()
        return self.agent.ask(q)

    def _build_q(self, tienda:str, terminal:str, area:str, sintoma:str, error:str, reinicio:str, hora:str, impacto:str, extra:str) -> str:
        parts=[f"tienda={tienda.strip()}" if tienda else "", f"terminal={terminal.strip()}" if terminal else "", f"area={area}", f"sintoma={sintoma}", f"error={error.strip()}" if error else "", f"reinicio={reinicio}", f"hora={hora.strip()}" if hora else "", f"impacto={impacto}", f"extra={extra.strip()}" if extra else ""]
        return " | ".join([p for p in parts if p])

    def gradio_ui(self):
        def infer_form(tienda, terminal, area, sintoma, error, reinicio, hora, impacto, extra):
            q = self._build_q(tienda, terminal, area, sintoma, error, reinicio, hora, impacto, extra)
            out = self.ask(q)
            srcs = "\n".join(f"- {s}" for s in out.get("sources",[]))
            return out.get("answer",""), srcs

        def infer_chat(chat: List[Tuple[str,str]], msg: str):
            out = self.ask(msg)
            ans = out.get("answer","")
            chat = (chat or []) + [(msg, ans)]
            return chat, ""

        areas=["POS","Inventario","Impresora","Etiquetado","Red","Handheld"]
        sintomas=["No imprime","Sin conexión","Lento","Error al cerrar caja","No sincroniza","Pantalla en blanco","Código de error"]
        reinicios=["Si","No"]
        impactos=["Caja detenida","Atención parcial","Tienda detenida"]

        with gr.Blocks(title="Soporte FashionPark RAG") as demo:
            with gr.Tab("Resolver"):
                with gr.Row():
                    tienda = gr.Textbox(label="Tienda")
                    terminal = gr.Textbox(label="Terminal")
                with gr.Row():
                    area = gr.Dropdown(choices=areas, value="POS", label="Área")
                    sintoma = gr.Dropdown(choices=sintomas, value="Sin conexión", label="Síntoma")
                error = gr.Textbox(label="Mensaje o detalle")
                with gr.Row():
                    reinicio = gr.Radio(choices=reinicios, value="No", label="¿Reinició POS/switch?")
                    hora = gr.Textbox(label="Hora aprox.")
                    impacto = gr.Radio(choices=impactos, value="Caja detenida", label="Impacto")
                extra = gr.Textbox(label="Dato extra")
                btn = gr.Button("Resolver")
                out = gr.Textbox(label="Respuesta", lines=14)
                src = gr.Textbox(label="Fuentes", lines=6)
                btn.click(infer_form, inputs=[tienda,terminal,area,sintoma,error,reinicio,hora,impacto,extra], outputs=[out,src])
            with gr.Tab("Chat"):
                chat = gr.Chatbot()
                chat_in = gr.Textbox(label="Mensaje")
                send = gr.Button("Enviar")
                send.click(infer_chat, inputs=[chat,chat_in], outputs=[chat,chat_in])
        demo.launch()

def main():
    app = SupportApp()
    if len(sys.argv)>=2:
        cmd = sys.argv[1].lower()
        if cmd=="ask":
            q=" ".join(sys.argv[2:]).strip() or "Problema de POS al cerrar caja"
            print(app.ask(q)["answer"]); return
        if cmd=="gradio":
            app.gradio_ui(); return
    app.gradio_ui()

if __name__=="__main__":
    main()
