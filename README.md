# 🧠 Soporte FashionPark RAG

Asistente automático de **mesa de ayuda para tiendas FashionPark**, basado en **LangGraph + Ollama (gemma3:1b) + Chroma** con interfaz **Gradio**.
Responde de forma contextualizada a incidentes operativos (POS, red, impresoras, handhelds, etc.), usando tus procedimientos en Markdown como base de conocimiento.

## 🚀 Características
- **Ingesta automática** de `./docs/**/*.md` y reindexación cuando cambian.
- **RAG local**: Chroma como vector store + Ollama para LLM y embeddings.
- **UI Gradio** con 2 modos: Formulario (Resolver) y Chat.
- Respuestas **operativas**: pasos de 60–120 s, validaciones y criterio **Listo/No listo**.
- **Fuentes** al final, citando archivos relevantes.

## 📁 Estructura
```
rag_ollama_langgraph/
├─ support_rag.py          # Script principal (autoindex + agente + UI)
├─ docs/                   # Conocimiento en .md (recursivo)
└─ chroma_db/              # Base vectorial (autogenerada)
```

## 🧩 Requisitos
1) Ollama en ejecución.
2) Modelos:
```bash
ollama pull gemma3:1b
ollama pull nomic-embed-text
```
3) Dependencias Python:
```bash
pip install -U langgraph langchain langchain-community langchain-chroma langchain-ollama langchain-text-splitters chromadb pydantic gradio
```

## ▶️ Ejecución
**Gradio (recomendado)**
```bash
python3 support_rag.py
```
Abrirá `http://localhost:7860`.

**CLI**
```bash
python3 support_rag.py ask "POS no imprime boleta en Tienda 102"
```

## 🧠 Cómo funciona
- Al iniciar, verifica cambios en `./docs`; si hay modificaciones, **reindexa**.
- Consulta el vector store con **k = 4** y arma un contexto.
- **LangGraph** orquesta `retrieve → synthesize` con `gemma3:1b`.
- Devuelve pasos prácticos y fuentes.

## 🛠️ Personalización
- Añade/edita SOPs en `./docs/` (por ejemplo `sops/reinicio_pos.md`, `red/red_caida.md`).
- Variables por entorno (opcionales):
  - `OLLAMA_LLM`, `OLLAMA_EMBED`, `DOCS_DIR`, `CHROMA_DIR`, `TOP_K`, `CHUNK_SIZE`, `CHUNK_OVERLAP`.

## ❗ Troubleshooting
- Error `connection refused`: confirma `ollama serve` corriendo.
- `AttributeError: ... persist`: ya está resuelto en el script; usa `langchain-chroma` actualizado.
- Sin resultados: verifica que existan `.md` con contenido en `./docs`.

## © Autor
**lab-ai SpA** — Desarrollado por **Juan Carlos Lanas Ocampo**
