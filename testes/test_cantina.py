"""Testes da Cantina usando dublês.

Só é possível testar a Cantina sem banco, sem Pix de verdade e sem terminal
porque ela depende de abstrações (Inversão de Dependências): aqui entram
implementações falsas de MeioPagamento e Notificador.
"""
import unittest

from cantina.cantina import Cantina
from cantina.cardapio import cardapio_do_dia
from cantina.notificacao import Notificador
from cantina.pagamento import MeioPagamento, ResultadoPagamento
from cantina.pedido import Pedido, StatusPedido

CARDAPIO = cardapio_do_dia()


class NotificadorEmMemoria(Notificador):
    def __init__(self):
        self.mensagens = []

    def notificar(self, aluno, mensagem):
        self.mensagens.append((aluno, mensagem))

    def para(self, aluno):
        return [mensagem for destino, mensagem in self.mensagens if destino == aluno]


class MeioFalso(MeioPagamento):
    def __init__(self, aprova=True):
        self._aprova = aprova
        self.cobrancas = []

    def pagar(self, valor):
        self.cobrancas.append(valor)
        if self._aprova:
            return ResultadoPagamento.aprovar()
        return ResultadoPagamento.recusar("cartão de teste recusado")


def pedido_de(aluno):
    pedido = Pedido(aluno)
    pedido.adicionar(CARDAPIO.buscar("Coxinha"))
    return pedido


class TestCantina(unittest.TestCase):
    def setUp(self):
        self.avisos = NotificadorEmMemoria()
        self.cantina = Cantina(self.avisos, minutos_por_pedido=2)

    def test_pagamento_recusado_nao_entra_na_fila_e_explica_o_motivo(self):
        pedido = pedido_de("Caio")

        self.assertFalse(self.cantina.fazer_pedido(pedido, MeioFalso(aprova=False)))

        self.assertEqual(pedido.status, StatusPedido.ABERTO)
        self.assertIsNone(self.cantina.preparar_proximo())
        self.assertIn("cartão de teste recusado", self.avisos.para("Caio")[0])

    def test_pagamento_aprovado_recebe_senha_posicao_e_estimativa(self):
        self.cantina.fazer_pedido(pedido_de("Ana"), MeioFalso())
        bruno = pedido_de("Bruno")

        self.cantina.fazer_pedido(bruno, MeioFalso())

        self.assertEqual(bruno.senha, 2)
        self.assertEqual(self.cantina.posicao(bruno), 2)
        self.assertEqual(self.cantina.estimativa_minutos(bruno), 4)

    def test_pedido_pronto_avisa_o_dono_e_atualiza_quem_espera(self):
        ana, bruno = pedido_de("Ana"), pedido_de("Bruno")
        self.cantina.fazer_pedido(ana, MeioFalso())
        self.cantina.fazer_pedido(bruno, MeioFalso())

        self.assertIs(self.cantina.preparar_proximo(), ana)

        self.assertEqual(ana.status, StatusPedido.PRONTO)
        self.assertIn("pronto", self.avisos.para("Ana")[-1])
        self.assertIn("1º da fila", self.avisos.para("Bruno")[-1])

    def test_pedido_vazio_nao_chega_a_ser_cobrado(self):
        meio = MeioFalso()
        with self.assertRaises(ValueError):
            self.cantina.fazer_pedido(Pedido("Duda"), meio)
        self.assertEqual(meio.cobrancas, [])


if __name__ == "__main__":
    unittest.main()
