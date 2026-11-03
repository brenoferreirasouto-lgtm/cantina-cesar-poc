"""Novo meio de pagamento: Voucher CESAR.

[Aberto/Fechado] Esta classe é a ÚNICA coisa nova para a cantina aceitar
vouchers. Nenhum arquivo de cantina/ foi editado: a Cantina já aceita
qualquer MeioPagamento (Inversão de Dependências), a interface só pede
pagar() (Segregação de Interfaces) e o voucher cumpre o mesmo contrato dos
outros meios (Liskov), verificado em testes/test_voucher.py.

Prova: git show --stat prova-aberto-fechado

No go-horse, aceitar voucher exigiria mais um elif dentro de
processar_pedido(), a função que já fazia tudo.
"""
from cantina.dinheiro import formatar
from cantina.pagamento import MeioPagamento, ResultadoPagamento


class VoucherCesar(MeioPagamento):
    """Voucher de uso único, distribuído em eventos do CESAR."""

    def __init__(self, codigo: str, valor: int) -> None:
        self._codigo = codigo
        self._valor = valor
        self._usado = False

    def pagar(self, valor: int) -> ResultadoPagamento:
        if self._usado:
            return ResultadoPagamento.recusar(f"voucher {self._codigo} já foi usado")
        if valor > self._valor:
            return ResultadoPagamento.recusar(
                f"voucher {self._codigo} cobre só até {formatar(self._valor)}")
        self._usado = True
        return ResultadoPagamento.aprovar()
