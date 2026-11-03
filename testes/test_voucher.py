"""O voucher entra no MESMO contrato dos outros meios: nenhum teste novo foi
escrito para isso, só a fábrica que cria um voucher (Substituição de Liskov)."""
import unittest

from extensoes.voucher import VoucherCesar
from testes.contrato_pagamento import ContratoMeioPagamento


class TestVoucherCesar(ContratoMeioPagamento, unittest.TestCase):
    def criar_meio(self, saldo):
        return VoucherCesar(codigo="TESTE", valor=saldo)


if __name__ == "__main__":
    unittest.main()
