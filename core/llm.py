import json
from urllib.request import Request, urlopen


class OllamaLocal:
    def __init__(self, modelo='llama3.2', url='http://localhost:11434/api/chat'):
        self.modelo = modelo
        self.url = url

    def responder(self, instrucciones, mensajes, estructurado=False):
        carga = {
            'model': self.modelo,
            'stream': False,
            'messages': [{'role': 'system', 'content': instrucciones}, *mensajes],
            'options': {'temperature': 0},
        }
        if estructurado:
            carga['format'] = 'json'
        solicitud = Request(
            self.url,
            data=json.dumps(carga).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
        )
        try:
            with urlopen(solicitud, timeout=120) as respuesta:
                return json.load(respuesta)['message']['content'].strip()
        except Exception as error:
            raise RuntimeError('No se pudo consultar Ollama. Verifica ollama serve y el modelo instalado.') from error
