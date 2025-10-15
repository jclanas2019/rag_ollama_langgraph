# -*- coding: utf-8 -*-
"""
LangGraph + (opcional) Ollama gemma3:1b — Pipeline de resumen por frecuencia
-----------------------------------------------------------------------------
Características:
- Ingesta de archivos .txt y .md (configurable), búsqueda recursiva opcional.
- Autofill opcional de 2 documentos si el directorio está vacío.
- Análisis determinista (frecuencia de términos) + (opcional) resumen LLM por archivo.
- Nodo LLM usa Ollama local con gemma3:1b (si está instalado y corriendo).
- Umbral --min-chars para invocar LLM solo en textos lo suficientemente grandes.

Instalación:
    pip install langgraph
    # (opcional) cliente de Ollama para Python
    pip install ollama
    # (en sistema) instalar daemon + modelo
    ollama pull gemma3:1b

Uso típico:
    python langgraph_ollama_gemma3_pipeline.py \
      --input ./docs --out ./out --top 8 \
      --ext .txt,.md --recursive true --autofill true \
      --ollama --model gemma3:1b --temp 0.2 --min-chars 200

Flags útiles:
    --ollama       habilita nodo LLM (booleano)
    --no-ollama    deshabilita nodo LLM
"""

from __future__ import annotations
from typing import TypedDict, Dict, List, Tuple, Optional
from collections import Counter
from pathlib import Path
import argparse
import re
import json
import time

from langgraph.graph import StateGraph, END

# ---- Cliente Ollama (opcional) ----
try:
    import ollama
    _OLLAMA_AVAILABLE = True
except Exception:
    _OLLAMA_AVAILABLE = False


# ===========================
#        ESTADO GLOBAL
# ===========================

class PipelineState(TypedDict):
    # I/O y parámetros
    input_dir: str
    out_dir: str
    top_n: int
    exts: List[str]
    recursive: bool
    autofill: bool
    min_chars_llm: int
    # Datos y resultados
    files: List[str]
    counts: Dict[str, List[Tuple[str, int]]]
    global_top: List[Tuple[str, int]]
    llm_enabled: bool
    llm_model: str
    llm_temperature: float
    llm_summaries: Dict[str, str]
    report_path: str
    summary_path: str
    warnings: List[str]


# ===========================
#         UTILIDADES
# ===========================

TOKEN_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", re.UNICODE)
STOP = {
    "a","acá","ahí","al","algo","algunas","algunos","allí","allá","ante","antes","aquel","aquella",
    "aquellas","aquellos","aqui","aquí","así","aun","aún","bajo","bien","cada","como","cómo","con",
    "contra","cual","cuales","cualquier","cuando","cuándo","de","del","desde","donde","dónde","dos",
    "el","él","ella","ellas","ellos","en","era","erais","eran","eras","eres","es","esa","esas","ese",
    "eso","esos","esta","estaba","estaban","estado","estamos","están","estar","estas","este","esto",
    "estos","fue","fueron","gran","ha","hace","hacen","hacer","hacia","han","hasta","hay","la","las",
    "lo","los","más","me","mi","mis","mismo","mucho","muy","nada","ni","no","nos","nosotros","o","os",
    "otra","otros","para","pero","poco","por","porque","que","qué","se","si","sí","sin","sobre","su",
    "sus","tal","tanto","te","ten","tiene","tienen","toda","todas","todo","todos","tu","tus","un","una",
    "uno","unos","usted","y","ya"
}

def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text.lower())

def filter_tokens(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t not in STOP and len(t) > 2]

def ensure_demo_data(path: Path):
    """Crea 2 documentos de ejemplo si la carpeta está vacía."""
    path.mkdir(parents=True, exist_ok=True)
    samples = {
        "ticket1.txt": (
            "El sistema POS registra ventas, inventario y devoluciones. "
            "La rapidez del cajero es clave para la experiencia del cliente."
        ),
        "ticket2.md": (
            "# Incidente: Lentitud Intermitente\n\n"
            "La terminal presenta lentitud intermitente. "
            "Se requiere diagnóstico de red y revisión del flujo "
            "de sincronización nocturna."
        ),
    }
    # Solo escribir si efectivamente está vacío
    if not any(path.iterdir()):
        for name, txt in samples.items():
            (path / name).write_text(txt, encoding="utf-8")


# ===========================
#           NODOS
# ===========================

def node_ingest(state: PipelineState) -> PipelineState:
    """Lista archivos por extensión; soporta recursivo y autofill."""
    in_dir = Path(state["input_dir"])
    exts = [e.strip().lower() for e in state["exts"]]
    recursive = state["recursive"]
    autofill = state["autofill"]

    if not in_dir.exists():
        in_dir.mkdir(parents=True, exist_ok=True)

    def match(p: Path) -> bool:
        return p.is_file() and p.suffix.lower() in exts

    files: List[Path]
    if recursive:
        files = sorted([p for p in in_dir.rglob("*") if match(p)])
    else:
        files = sorted([p for p in in_dir.glob("*") if match(p)])

    if not files and autofill:
        ensure_demo_data(in_dir)
        if recursive:
            files = sorted([p for p in in_dir.rglob("*") if match(p)])
        else:
            files = sorted([p for p in in_dir.glob("*") if match(p)])

    if not files:
        raise RuntimeError(
            f"No se encontraron archivos con extensiones {exts} en {in_dir} "
            f"(recursive={recursive}). Crea .txt/.md o usa --autofill."
        )

    state["files"] = [str(p) for p in files]
    return state


def node_analyze(state: PipelineState) -> PipelineState:
    """Tokeniza, filtra stopwords y calcula top-N por archivo + top global."""
    top_n = state["top_n"]
    results: Dict[str, List[Tuple[str, int]]] = {}
    global_counter = Counter()

    for fp in state["files"]:
        text = Path(fp).read_text(encoding="utf-8", errors="ignore")
        tokens = filter_tokens(tokenize(text))
        cnt = Counter(tokens)
        results[Path(fp).name] = cnt.most_common(top_n)
        global_counter.update(cnt)

    state["counts"] = results
    state["global_top"] = global_counter.most_common(top_n)
    return state


def _ollama_ready(model: str) -> Tuple[bool, Optional[str]]:
    """Verifica que el cliente/daemon/modelo de Ollama esté listo."""
    if not _OLLAMA_AVAILABLE:
        return False, "Paquete 'ollama' no está instalado (pip install ollama)."
    try:
        _ = ollama.list()  # comprueba daemon
    except Exception as e:
        return False, f"Ollama no responde: {e}. Asegura que el daemon esté corriendo."
    try:
        _ = ollama.show(model)  # comprueba modelo local
        return True, None
    except Exception:
        return False, f"Modelo '{model}' no encontrado localmente. Ejecuta: ollama pull {model}"


def _build_prompt(file_name: str, raw_text: str, top_terms: List[Tuple[str, int]]) -> List[Dict[str, str]]:
    excerpt = raw_text.strip().replace("\n", " ")
    if len(excerpt) > 1200:
        excerpt = excerpt[:1200] + "…"
    bullets = "\n".join([f"- {t}: {f}" for t, f in top_terms])

    system_msg = (
        "Eres un analista de soporte POS. Redacta un resumen técnico breve en español (3–5 oraciones), "
        "claro y accionable, sin inventar datos. Enfatiza síntomas, posibles causas y próximos pasos."
    )
    user_msg = (
        f"Archivo: {file_name}\n"
        f"Top términos:\n{bullets}\n\n"
        f"Texto (extracto):\n{excerpt}\n\n"
        "Entrega SOLO el resumen, sin prefacios ni viñetas."
    )
    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]


def node_llm_refine(state: PipelineState) -> PipelineState:
    """Genera resumen por archivo con Ollama (si habilitado y elegible por tamaño)."""
    if not state["llm_enabled"]:
        return state

    ok, warn = _ollama_ready(state["llm_model"])
    if not ok:
        state["warnings"].append(warn or "Ollama no disponible.")
        state["llm_enabled"] = False
        return state

    summaries: Dict[str, str] = {}
    for fp in state["files"]:
        fname = Path(fp).name
        raw_text = Path(fp).read_text(encoding="utf-8", errors="ignore")

        # Invocar LLM solo si supera el umbral de longitud
        if len(raw_text) < state["min_chars_llm"]:
            summaries[fname] = "(Texto breve: se omite resumen LLM.)"
            continue

        top = state["counts"].get(fname, [])
        messages = _build_prompt(fname, raw_text, top)

        try:
            rsp = ollama.chat(
                model=state["llm_model"],
                messages=messages,
                options={"temperature": state["llm_temperature"]},
            )
            content = (rsp.get("message", {}) or {}).get("content", "").strip()
            if not content:
                raise RuntimeError("Respuesta vacía.")
            summaries[fname] = content
            time.sleep(0.05)  # respiro corto para modelos locales
        except Exception as e:
            state["warnings"].append(f"Fallo LLM en {fname}: {e}")
            summaries[fname] = "(No se pudo generar resumen con LLM.)"

    state["llm_summaries"] = summaries
    return state


def node_compile_report(state: PipelineState) -> PipelineState:
    """Escribe report.md (Markdown) y summary.json (estadísticos)."""
    out_dir = Path(state["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    md = ["# Reporte de Frecuencia de Términos\n"]
    if state["warnings"]:
        md.append("> **Avisos**:")
        for w in state["warnings"]:
            md.append(f"> - {w}")
        md.append("")

    for fname, pairs in state["counts"].items():
        md.append(f"## {fname}\n")
        md.append("| Término | Frecuencia |")
        md.append("|---|---:|")
        for term, freq in pairs:
            md.append(f"| {term} | {freq} |")
        md.append("")

        # Adjunta resumen LLM si corresponde
        if state["llm_enabled"] and state["llm_summaries"].get(fname):
            md.append("**Resumen LLM (gemma3:1b):**")
            md.append(state["llm_summaries"][fname])
            md.append("")

    (out_dir / "report.md").write_text("\n".join(md), encoding="utf-8")

    # JSON con metadatos del procesamiento
    unique_vocab = {t for _, pairs in state["counts"].items() for t, _ in pairs}
    summary = {
        "archivos": list(state["counts"].keys()),
        "top_global": state["global_top"],
        "unique_vocab_top_terms": len(unique_vocab),
        "llm_enabled": state["llm_enabled"],
        "warnings": state["warnings"],
        "params": {
            "top_n": state["top_n"],
            "exts": state["exts"],
            "recursive": state["recursive"],
            "autofill": state["autofill"],
            "min_chars_llm": state["min_chars_llm"],
            "model": state["llm_model"],
            "temperature": state["llm_temperature"],
        },
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    state["report_path"] = str(out_dir / "report.md")
    state["summary_path"] = str(out_dir / "summary.json")
    return state


# ===========================
#       CONSTRUCCIÓN GRAFO
# ===========================

def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("ingest", node_ingest)
    graph.add_node("analyze", node_analyze)
    graph.add_node("llm_refine", node_llm_refine)
    graph.add_node("compile_report", node_compile_report)

    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "analyze")
    graph.add_edge("analyze", "llm_refine")
    graph.add_edge("llm_refine", "compile_report")
    graph.add_edge("compile_report", END)

    return graph.compile()


# ===========================
#            CLI
# ===========================

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="./data", help="Directorio de entrada.")
    ap.add_argument("--out", default="./out", help="Directorio de salida.")
    ap.add_argument("--top", type=int, default=8, help="Top-N términos por archivo.")
    ap.add_argument("--ext", default=".txt,.md", help="Extensiones separadas por coma (ej: .txt,.md)")
    ap.add_argument("--recursive", default="false", choices=["true","false"], help="Búsqueda recursiva.")
    ap.add_argument("--autofill", default="true", choices=["true","false"], help="Autollenar si no hay archivos.")
    ap.add_argument("--min-chars", type=int, default=200, dest="min_chars", help="Invocar LLM si texto >= a este tamaño.")
    # Flags booleanos para LLM
    ap.add_argument("--ollama", dest="ollama", action="store_true", help="Habilita nodo LLM.")
    ap.add_argument("--no-ollama", dest="ollama", action="store_false", help="Deshabilita nodo LLM.")
    ap.set_defaults(ollama=True)
    # Modelo y sampling
    ap.add_argument("--model", default="gemma3:1b", help="Modelo Ollama (gemma3:1b por defecto).")
    ap.add_argument("--temp", type=float, default=0.2, help="Temperatura LLM.")
    return ap.parse_args()


def main():
    args = parse_args()
    app = build_graph()

    state: PipelineState = {
        "input_dir": str(Path(args.input)),
        "out_dir": str(Path(args.out)),
        "top_n": int(args.top),
        "exts": [e.strip() for e in args.ext.split(",") if e.strip()],
        "recursive": (args.recursive == "true"),
        "autofill": (args.autofill == "true"),
        "min_chars_llm": int(args.min_chars),
        "files": [],
        "counts": {},
        "global_top": [],
        "llm_enabled": bool(args.ollama),
        "llm_model": str(args.model),
        "llm_temperature": float(args.temp),
        "llm_summaries": {},
        "report_path": "",
        "summary_path": "",
        "warnings": [],
    }

    final_state = app.invoke(state)

    print("[OK] Reporte:", final_state["report_path"])
    print("[OK] Resumen:", final_state["summary_path"])
    if final_state["warnings"]:
        print("Avisos:")
        for w in final_state["warnings"]:
            print(" -", w)


if __name__ == "__main__":
    main()
