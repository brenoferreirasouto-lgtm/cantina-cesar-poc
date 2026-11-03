import unittest

from cantina.cardapio import cardapio_do_dia
from cantina.descontos import DescontoCombo, SemDesconto
from cantina.pedido import Pedido

CARDAPIO = cardapio_do_dia()


def pedido_com(politica, *nomes):
    pedido = Pedido("Ana", politica)
    for nome in nomes:
        pedido.adicionar(CARDAPIO.buscar(nome))
    return pedido


class TestPedido(unittest.TestCase):
    def test_lanche_mais_bebida_ganha_desconto_de_combo(self):
        pedido = pedido_com(DescontoCombo(10), "Coxinha", "Suco de laranja")
        self.assertEqual(pedido.subtotal(), 1250)
        self.assertEqual(pedido.total(), 1125)

    def test_sem_bebida_nao_e_combo(self):
        pedido = pedido_com(DescontoCombo(10), "Sanduíche natural", "Brigadeiro")
        self.assertEqual(pedido.total(), 1200)

    def test_trocar_a_politica_muda_o_preco_sem_mudar_o_pedido(self):
        itens = ("Coxinha", "Café")
        self.assertEqual(pedido_com(SemDesconto(), *itens).total(), 1050)
        self.assertEqual(pedido_com(DescontoCombo(20), *itens).total(), 840)

    def test_pedido_pago_nao_aceita_novos_itens(self):
        pedido = pedido_com(SemDesconto(), "Café")
        pedido.confirmar_pagamento(senha=1)
        with self.assertRaises(RuntimeError):
            pedido.adicionar(CARDAPIO.buscar("Brigadeiro"))


if __name__ == "__main__":
    unittest.main()
