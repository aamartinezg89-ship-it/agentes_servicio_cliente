
from pathlib import Path

import pytest

from core.llm import OllamaLocal
from agentes.gerente import AgenteGerente
from rag.documentos import LectorPDF
from rag.buscador import BuscadorRAG
from sentence_transformers import SentenceTransformer
from sentence_transformers import util


@pytest.fixture(scope="module")
def llm():
    return OllamaLocal(modelo="llama3.2:3b")


@pytest.fixture(scope="module")
def buscador():
    ruta = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "Manual_Generico_Atencion_Cliente_RAG_v1.pdf"
    )

    paginas = LectorPDF(ruta).leer()
    return BuscadorRAG(paginas)


def test_llm_responde(llm):
    respuesta = llm.responder(
        "Responde brevemente en español.",
        [{"role": "user", "content": "Di solamente HOLA"}]
    )

    assert isinstance(respuesta, str)
    assert respuesta.strip()


def test_gerente_no_inventa_nombre(llm, buscador):

    gerente = AgenteGerente(llm, buscador)

    historial = [
        {
            "role": "user",
            "content": "Quiero devolver un producto."
        },
        {
            "role": "assistant",
            "content": "Su caso fue transferido a gerencia."
        }
    ]

    resultado = gerente.atender(
        "¿Cuál es el nombre del gerente?",
        historial
    )

    respuesta = (
        resultado["respuesta"]
        if isinstance(resultado, dict)
        else str(resultado)
    )

    print("\nRESPUESTA DEL GERENTE:", respuesta)

    assert respuesta.strip()

    nombres_inventados = [
        "Juan Pérez",
        "Pedro López",
        "María García"
    ]

    assert not any(
        nombre.lower() in respuesta.lower()
        for nombre in nombres_inventados
    )

def test_gerente_respuesta_semantica(llm, buscador):

    gerente = AgenteGerente(llm, buscador)

    historial = [
        {
            "role": "user",
            "content": "Quiero devolver un producto."
        }
    ]

    resultado = gerente.atender(
        "¿Cuál es su nombre?",
        historial
    )

    respuesta = (
        resultado["respuesta"]
        if isinstance(resultado, dict)
        else str(resultado)
    )

    referencia = (
        "Soy un asistente virtual de gerencia. "
        "No tengo un nombre personal asignado."
    )

    modelo = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )

    similitud = util.cos_sim(
        modelo.encode(respuesta),
        modelo.encode(referencia)
    ).item()

    print(f"\nRespuesta: {respuesta}")
    print(f"Similitud semántica: {similitud:.3f}")

    assert similitud >= 0.65

def test_memoria_gerente(llm, buscador):

    gerente = AgenteGerente(llm, buscador)

    historial = [
        {
            "role": "user",
            "content": "Quiero devolver un producto."
        },
        {
            "role": "assistant",
            "content": "¿Hace cuántos días lo recibió?"
        },
        {
            "role": "user",
            "content": "Hace 45 días y llegó dañado."
        },
        {
            "role": "assistant",
            "content": "Voy a transferir su caso a gerencia."
        },
        {
            "role": "user",
            "content": "Sí, quiero hablar con gerencia."
        }
    ]

    respuesta = gerente.atender(
        "¿Qué información tiene sobre mi caso?",
        historial
    )

    if isinstance(respuesta, dict):
        respuesta = respuesta["respuesta"]

    print("\nRESPUESTA DEL GERENTE:")
    print(respuesta)

    assert isinstance(respuesta, str)
    assert respuesta.strip()

    assert "45" in respuesta

    assert any(
        palabra in respuesta.lower()
        for palabra in ["dañado", "daño", "defectuoso", "defecto"]
    )
