import unittest

from cantina.pagamento import CreditoCarteirinha, Pix
from testes.contrato_pagamento import ContratoMeioPagamento


class TestPix(ContratoMeioPagamento, unittest.TestCase):
    def criar_meio(self, saldo):
        return Pix(saldo_conta=saldo)


class TestCreditoCarteirinha(ContratoMeioPagamento, unittest.TestCase):
    def criar_meio(self, saldo):
        return CreditoCarteirinha(creditos=saldo)


if __name__ == "__main__":
    unittest.main()
