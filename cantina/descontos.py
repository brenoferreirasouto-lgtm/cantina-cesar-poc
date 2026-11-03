"""Regras de desconto, separadas do pedido."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from cantina.cardapio import Categoria, Produto


class PoliticaDesconto(ABC):
    """[Composição em vez de herança] O Pedido POSSUI uma política de desconto.

    A alternativa por herança seria PedidoComDesconto(Pedido),
    PedidoComboFidelidade(Pedido)... uma subclasse para cada regra e para cada
    combinação de regras. Com composição, trocar a regra é trocar o objeto,
    inclusive em tempo de execução, e o Pedido não muda.
    """

    @abstractmethod
    def calcular(self, itens: Sequence[Produto]) -> int:
        """Desconto em centavos (>= 0) para estes itens."""


class SemDesconto(PoliticaDesconto):
    def calcular(self, itens: Sequence[Produto]) -> int:
        return 0


class DescontoCombo(PoliticaDesconto):
    """Lanche + bebida no mesmo pedido = combo com desconto percentual."""

    def __init__(self, percentual: int = 10) -> None:
        self._percentual = percentual

    def calcular(self, itens: Sequence[Produto]) -> int:
        if not self._eh_combo(itens):
            return 0
        subtotal = sum(produto.preco for produto in itens)
        return subtotal * self._percentual // 100

    @staticmethod
    def _eh_combo(itens: Sequence[Produto]) -> bool:
        categorias = {produto.categoria for produto in itens}
        return {Categoria.LANCHE, Categoria.BEBIDA} <= categorias
