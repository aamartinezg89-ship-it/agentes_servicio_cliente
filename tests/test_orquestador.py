from core.orquestador import Orquestador


class EjecutivoFalso:
    def atender(self, pregunta, historial):
        return {'accion': 'ofrecer_gerente', 'respuesta': 'Este caso requiere revisión especial.'}


class GerenteFalso:
    def __init__(self):
        self.consultas = []

    def atender(self, pregunta, historial):
        self.consultas.append(pregunta)
        assert any(m['role'] == 'user' for m in historial)
        return 'Buen día. Ya revisé su caso. ¿Cuál es el motivo de la devolución?'


def test_escala_con_consentimiento():
    gerente = GerenteFalso()
    sistema = Orquestador(EjecutivoFalso(), gerente)
    agente, mensaje = sistema.conversar('Necesito un reembolso extraordinario')
    assert agente == 'ejecutivo'
    assert '¿Desea' in mensaje
    agente, mensaje = sistema.conversar('sí')
    assert agente == 'gerente'
    assert 'Ya revisé su caso' in mensaje
    assert gerente.consultas[-1] == 'Necesito un reembolso extraordinario'


def test_cliente_pide_gerente():
    sistema = Orquestador(EjecutivoFalso(), GerenteFalso())
    agente, _ = sistema.conversar('Quiero hablar con el gerente')
    assert agente == 'gerente'


def test_gerente_no_vuelve_a_transferir():
    gerente = GerenteFalso()
    sistema = Orquestador(EjecutivoFalso(), gerente)
    sistema.conversar('Quiero hablar con el gerente')
    agente, mensaje = sistema.conversar('Ya pasaron 45 días')
    assert agente == 'gerente'
    assert '¿Desea que lo transfiera' not in mensaje
    assert gerente.consultas[-1] == 'Ya pasaron 45 días'
