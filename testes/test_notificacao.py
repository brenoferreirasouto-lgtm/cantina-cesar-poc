"""A apresentação é testada à parte, sem precisar montar Cantina, fila ou pagamento."""
import io
import unittest
from contextlib import redirect_stdout

from cantina.eventos import PagamentoRecusado, PedidoPago
from cantina.notificacao import NotificadorConsole


def texto_impresso(evento):
    saida = io.StringIO()
    with redirect_stdout(saida):
        NotificadorConsole().notificar(evento)
    return saida.getvalue()


class TestNotificadorConsole(unittest.TestCase):
    def test_pedido_pago_mostra_valor_em_reais_e_lugar_na_fila(self):
        texto = texto_impresso(PedidoPago("Ana", senha=1, valor=1125, posicao=2, minutos=4))
        self.assertIn("[Ana]", texto)
        self.assertIn("R$ 11,25", texto)
        self.assertIn("2º da fila (~4 min)", texto)

    def test_recusa_explica_o_motivo(self):
        texto = texto_impresso(PagamentoRecusado("Caio", "saldo insuficiente"))
        self.assertIn("recusado: saldo insuficiente", texto)


if __name__ == "__main__":
    unittest.main()
