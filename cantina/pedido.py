"""O pedido de um aluno: itens, valores e estado."""
from __future__ import annotations

from enum import Enum
from typing import Optional, Tuple

from cantina.cardapio import Produto
from cantina.descontos import PoliticaDesconto, SemDesconto


class StatusPedido(Enum):
    ABERTO = "aberto"
    PAGO = "pago"
    PRONTO = "pronto"


class Pedido:
    """[Responsabilidade Única] Sabe o que foi pedido e quanto custa.

    Não sabe cobrar, não sabe de fila e não imprime nada: cada uma dessas
    coisas muda por um motivo diferente e mora em outra classe.

    [Ocultamento de informação] A lista de itens e o status são privados. O
    estado só muda pelos métodos abaixo, que impedem, por exemplo, adicionar
    itens num pedido já pago.
    """

    def __init__(self, aluno: str, politica: Optional[PoliticaDesconto] = None) -> None:
        self.aluno = aluno
        self._itens: list = []
        self._politica = politica or SemDesconto()
        self._status = StatusPedido.ABERTO
        self._senha: Optional[int] = None

    # ---- montagem -------------------------------------------------------
    def adicionar(self, produto: Produto, quantidade: int = 1) -> None:
        self._exigir_status(StatusPedido.ABERTO, "adicionar itens")
        self._itens.extend([produto] * quantidade)

    def itens(self) -> Tuple[Produto, ...]:
        return tuple(self._itens)  # cópia: ninguém altera o pedido por fora

    # ---- valores (sempre em centavos) ------------------------------------
    def subtotal(self) -> int:
        return sum(produto.preco for produto in self._itens)

    def desconto(self) -> int:
        return self._politica.calcular(self.itens())

    def total(self) -> int:
        return self.subtotal() - self.desconto()

    # ---- ciclo de vida ----------------------------------------------------
    @property
    def status(self) -> StatusPedido:
        return self._status

    @property
    def senha(self) -> Optional[int]:
        return self._senha

    def confirmar_pagamento(self, senha: int) -> None:
        self._exigir_status(StatusPedido.ABERTO, "confirmar pagamento")
        self._senha = senha
        self._status = StatusPedido.PAGO

    def marcar_pronto(self) -> None:
        self._exigir_status(StatusPedido.PAGO, "marcar como pronto")
        self._status = StatusPedido.PRONTO

    def _exigir_status(self, esperado: StatusPedido, acao: str) -> None:
        if self._status is not esperado:
            raise RuntimeError(f"Não dá para {acao}: pedido está {self._status.value}.")
