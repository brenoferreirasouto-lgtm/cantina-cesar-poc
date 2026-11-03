"""O que a cantina vende e quanto custa."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Iterator


class Categoria(Enum):
    LANCHE = "lanche"
    BEBIDA = "bebida"
    DOCE = "doce"


@dataclass(frozen=True)
class Produto:
    """Imutável: ninguém muda o preço de uma coxinha depois que ela está num pedido."""

    nome: str
    preco: int  # centavos
    categoria: Categoria


class Cardapio:
    """[Responsabilidade Única] Só sabe quais produtos existem e seus preços.

    No go-horse os preços eram um if/elif dentro da função de pedido: mudar o
    preço do suco exigia mexer no mesmo código que cobra e controla a fila.
    """

    def __init__(self, produtos: Iterable[Produto]) -> None:
        self._produtos = {produto.nome: produto for produto in produtos}

    def buscar(self, nome: str) -> Produto:
        try:
            return self._produtos[nome]
        except KeyError:
            raise ValueError(f"'{nome}' não está no cardápio de hoje") from None

    def __iter__(self) -> Iterator[Produto]:
        return iter(self._produtos.values())


def cardapio_do_dia() -> Cardapio:
    return Cardapio([
        Produto("Coxinha", 650, Categoria.LANCHE),
        Produto("Pão de queijo", 450, Categoria.LANCHE),
        Produto("Sanduíche natural", 900, Categoria.LANCHE),
        Produto("Suco de laranja", 600, Categoria.BEBIDA),
        Produto("Café", 400, Categoria.BEBIDA),
        Produto("Brigadeiro", 300, Categoria.DOCE),
    ])
