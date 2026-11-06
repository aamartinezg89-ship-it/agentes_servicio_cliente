from core.memoria import Memoria


class Orquestador:
    AFIRMATIVAS = {'si', 'sí', 'claro', 'acepto', 'de acuerdo', 'por favor'}
    NEGATIVAS = {'no', 'no gracias', 'prefiero no'}

    def __init__(self, ejecutivo, gerente):
        self.ejecutivo = ejecutivo
        self.gerente = gerente
        self.memoria = Memoria()
        self.agente_actual = 'ejecutivo'
        self.transferencia_pendiente = False

    def conversar(self, mensaje):
        texto = mensaje.strip()
        if not texto:
            return self.agente_actual, 'Cuénteme cómo puedo ayudarle.'

        normalizado = texto.casefold()
        contexto_previo = self.memoria.contexto()
        self.memoria.agregar('user', texto)
        contexto = self.memoria.contexto()

        solicitud_directa = self.agente_actual == 'ejecutivo' and any(
            frase in normalizado for frase in (
                'hablar con el gerente', 'pásame con el gerente',
                'pasame con el gerente', 'quiero un supervisor',
                'hablar con un supervisor', 'comunícame con gerencia',
                'comunicame con gerencia'
            )
        )

        if self.agente_actual == 'ejecutivo' and (
            solicitud_directa or (self.transferencia_pendiente and normalizado in self.AFIRMATIVAS)
        ):
            self.agente_actual = 'gerente'
            self.transferencia_pendiente = False
            # El 'sí' solo confirma la transferencia; recuperamos el asunto real.
            consulta_original = next(
                (m['content'] for m in reversed(contexto_previo)
                 if m['role'] == 'user' and m['content'].strip().casefold() not in self.AFIRMATIVAS),
                'Solicitud de atención al cliente'
            )
            respuesta = self.gerente.atender(consulta_original, contexto)

        elif self.agente_actual == 'ejecutivo':
            if self.transferencia_pendiente and normalizado in self.NEGATIVAS:
                self.transferencia_pendiente = False
                respuesta = 'De acuerdo, seguimos por aquí. ¿En qué más puedo ayudarle?'
            else:
                self.transferencia_pendiente = False
                resultado = self.ejecutivo.atender(texto, contexto)
                respuesta = resultado['respuesta'].strip()
                if resultado['accion'] == 'ofrecer_gerente':
                    self.transferencia_pendiente = True
                    respuesta += '\n¿Desea que lo transfiera con gerencia? (sí/no)'
        else:
            respuesta = self.gerente.atender(texto, contexto)

        self.memoria.agregar('assistant', respuesta)
        return self.agente_actual, respuesta
