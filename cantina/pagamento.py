"""Meios de pagamento aceitos pela cantina."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoPagamento:
    aprovado: bool
    motivo: str = ""

    @classmethod
    def aprovar(cls) -> "ResultadoPagamento":
        return cls(aprovado=True)

    @classmethod
    def recusar(cls, motivo: str) -> "ResultadoPagamento":
        return cls(aprovado=False, motivo=motivo)


class MeioPagamento(ABC):
    """A abstração da qual a Cantina depende.

    [Segregação de Interfaces] Um único método: é tudo o que a Cantina precisa.
    Recarregar crédito, consultar saldo ou validar código são assuntos de cada
    meio; se estivessem aqui, todo meio novo seria obrigado a implementá-los.

    [Substituição de Liskov] Contrato que TODO meio precisa cumprir:
      - recebe um valor em centavos (> 0, garantido pela Cantina);
      - devolve SEMPRE um ResultadoPagamento, nunca lança exceção por recusa;
      - se aprovou, debitou; se recusou, não debitou e explicou o motivo.
    O contrato é verificado para cada meio em testes/contrato_pagamento.py.
    """

    @abstractmethod
    def pagar(self, valor: int) -> ResultadoPagamento:
        ...


class Pix(MeioPagamento):
    """Pix com a conta bancária do aluno simulada (PoC: sem banco real)."""

    def __init__(self, saldo_conta: int) -> None:
        self._saldo_conta = saldo_conta

    def pagar(self, valor: int) -> ResultadoPagamento:
        if valor > self._saldo_conta:
            return ResultadoPagamento.recusar("saldo insuficiente no banco")
        self._saldo_conta -= valor
        return ResultadoPagamento.aprovar()


class CreditoCarteirinha(MeioPagamento):
    """Créditos pré-pagos na carteirinha CESAR.

    Tem um método a mais, recarregar(), que NÃO está em MeioPagamento: a
    Cantina não precisa dele, então não depende dele (Segregação de Interfaces).
    """

    def __init__(self, creditos: int) -> None:
        self._creditos = creditos

    def recarregar(self, valor: int) -> None:
        self._creditos += valor

    def pagar(self, valor: int) -> ResultadoPagamento:
        if valor > self._creditos:
            return ResultadoPagamento.recusar("créditos insuficientes na carteirinha")
        self._creditos -= valor
        return ResultadoPagamento.aprovar()
