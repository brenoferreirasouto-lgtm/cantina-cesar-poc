import unittest

from cantina.fila import FilaCantina
from cantina.pedido import Pedido


class TestFilaCantina(unittest.TestCase):
    def test_primeiro_a_pagar_e_o_primeiro_a_ser_atendido(self):
        fila = FilaCantina()
        ana, bruno = Pedido("Ana"), Pedido("Bruno")
        fila.entrar(ana)
        fila.entrar(bruno)

        self.assertEqual(fila.posicao(bruno), 2)
        self.assertIs(fila.proximo(), ana)
        self.assertEqual(fila.posicao(bruno), 1)

    def test_fila_vazia_nao_tem_proximo(self):
        self.assertIsNone(FilaCantina().proximo())


if __name__ == "__main__":
    unittest.main()
