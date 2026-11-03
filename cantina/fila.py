"""A fila de pedidos pagos aguardando preparo."""
from __future__ import annotations

from collections import deque
from typing import Optional, Tuple

from cantina.pedido import Pedido


class FilaCantina:
    """[Ocultamento de informação] Ninguém de fora sabe que existe um deque aqui.

    Quem usa a fila conhece só entrar(), proximo(), posicao() e aguardando().
    Poderíamos trocar o deque por uma lista, uma fila de prioridade (pedido de
    professor primeiro?) ou um Redis, sem alterar uma linha fora deste arquivo.

    No go-horse a fila era uma lista global e pública: qualquer trecho de
    código podia dar fila.pop(1) e sumir com o pedido de alguém.
    """

    def __init__(self) -> None:
        self._pedidos = deque()

    def entrar(self, pedido: Pedido) -> None:
        self._pedidos.append(pedido)

    def proximo(self) -> Optional[Pedido]:
        if not self._pedidos:
            return None
        return self._pedidos.popleft()

    def posicao(self, pedido: Pedido) -> int:
        """1 = é o próximo a ser preparado."""
        return self._pedidos.index(pedido) + 1

    def aguardando(self) -> Tuple[Pedido, ...]:
        return tuple(self._pedidos)  # cópia somente leitura

    def __len__(self) -> int:
        return len(self._pedidos)
