from pathlib import Path
from agentes.ejecutivo import AgenteEjecutivo
from agentes.gerente import AgenteGerente
from core.llm import OllamaLocal
from core.orquestador import Orquestador
from rag.buscador import BuscadorRAG
from rag.documentos import LectorPDF


def main():
    archivo = Path(__file__).parent / 'data' / 'Manual_Generico_Atencion_Cliente_RAG_v1.pdf'
    paginas = LectorPDF(archivo).leer()
    buscador = BuscadorRAG(paginas)
    llm = OllamaLocal(modelo='llama3.2:3b')
    sistema = Orquestador(AgenteEjecutivo(llm, buscador), AgenteGerente(llm, buscador))

    print('CustomerCare AI | /salir para terminar')
    print('Ejecutivo: Bienvenido. ¿Cómo puedo ayudarle?')
    while True:
        mensaje = input('\nCliente > ').strip()
        if mensaje.lower() == '/salir':
            break
        try:
            agente, respuesta = sistema.conversar(mensaje)
            print(f'{agente.capitalize()} > {respuesta}')
        except RuntimeError as error:
            print(f'Error: {error}')


if __name__ == '__main__':
    main()
