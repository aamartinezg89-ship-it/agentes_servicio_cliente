
import pytest

from core.llm import OllamaLocal
from agentes.gerente import AgenteGerente

from rag.documentos import LectorPDF
from rag.buscador import BuscadorRAG

from pathlib import Path


@pytest.fixture(scope="module")
def gerente():

    ruta = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "Manual_Generico_Atencion_Cliente_RAG_v1.pdf"
    )

    paginas = LectorPDF(ruta).leer()

    buscador = BuscadorRAG(paginas)
    llm = OllamaLocal(modelo="llama3.2:3b")

    return AgenteGerente(llm, buscador)


def test_devolucion_fuera_plazo(gerente):

    historial = [
        {
            "role": "user",
            "content": "Quiero devolver un producto."
        },
        {
            "role": "assistant",
            "content": "¿Cuándo recibió el producto?"
        },
        {
            "role": "user",
            "content": "Hace 45 días y llegó dañado."
        }
    ]

    respuesta = gerente.atender(
        "¿Pueden devolverme mi dinero?",
        historial
    )

    if isinstance(respuesta, dict):
        respuesta = respuesta["respuesta"]

    print("\nRESPUESTA DEL GERENTE:")
    print(respuesta)

    texto = respuesta.lower()

    # Reconoce que está fuera del plazo ordinario
    assert "30" in texto or "plazo" in texto

    # Reconoce la necesidad de revisión
    assert any(
        palabra in texto
        for palabra in [
            "revisión",
            "evaluación",
            "excepción",
            "revisar"
        ]
    )

    # No promete un reembolso ya aprobado
    expresiones_prohibidas = [
        "su reembolso ha sido aprobado",
        "le garantizo el reembolso",
        "su dinero ya fue enviado",
        "su devolución está autorizada"
    ]

    assert not any(
        frase in texto
        for frase in expresiones_prohibidas
    )
