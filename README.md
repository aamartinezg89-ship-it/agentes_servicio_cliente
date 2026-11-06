# CustomerCare AI — demostración multiagente con RAG

Proyecto educativo de atención al cliente, sin vinculación con una empresa real. Las políticas del PDF son ficticias.

## Instalación

```bash
python -m pip install -r requirements.txt
ollama pull llama3.2
ollama serve  # solo si Ollama no está ejecutándose
python main.py
```

La primera ejecución descargará el modelo de embeddings. Ollama debe estar instalado y funcionando en localhost:11434.

## Pruebas

```bash
python -m pytest -q
```

## Arquitectura

- `rag/documentos.py`: extrae texto y páginas del PDF.
- `rag/buscador.py`: divide por fragmentos y recupera contenido mediante embeddings.
- `core/llm.py`: cliente local para Ollama.
- `agentes/ejecutivo.py`: responde o recomienda escalamiento.
- `agentes/gerente.py`: atiende el caso transferido.
- `core/memoria.py`: historial conversacional.
- `core/orquestador.py`: reglas de transferencia.
- `main.py`: consola.

**Limitaciones:** demo local; no realiza reembolsos ni decisiones reales. Un score vectorial no prueba veracidad. La evaluación de RAG y el enrutamiento deben ampliarse antes de un uso real.
