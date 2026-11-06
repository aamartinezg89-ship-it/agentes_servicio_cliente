class Memoria:
    def __init__(self):
        self.mensajes = []

    def agregar(self, rol, contenido):
        self.mensajes.append({'role': rol, 'content': contenido})

    def contexto(self):
        return self.mensajes[-12:].copy()
