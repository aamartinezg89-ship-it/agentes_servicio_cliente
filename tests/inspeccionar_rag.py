
from pathlib import Path

from rag.documentos import LectorPDF
from rag.buscador import BuscadorRAG


def main():

    ruta = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "Manual_Generico_Atencion_Cliente_RAG_v1.pdf"
    )

    paginas = LectorPDF(ruta).leer()
    buscador = BuscadorRAG(paginas)

    pregunta = (
        "Recibí un producto dañado hace 45 días. "
        "¿Puedo solicitar una devolución?"
    )

    resultados = buscador.buscar(pregunta)

    for i, resultado in enumerate(resultados, start=1):
        print(f"\n{'=' * 60}")
        print(f"RESULTADO {i}")
        print(f"Página: {resultado['pagina']}")
        print(f"Similitud: {resultado['similitud']:.3f}")
        print(f"{'=' * 60}")
        print(resultado["texto"])


if __name__ == "__main__":
    main()
