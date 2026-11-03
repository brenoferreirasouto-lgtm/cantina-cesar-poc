"""O fluxo do intervalo: pagar, entrar na fila, ser avisado, buscar o lanche."""
from __future__ import annotations

from itertools import count
from typing import Optional

from cantina.dinheiro import formatar
from cantina.fila import FilaCantina
from cantina.notificacao import Notificador
from cantina.pagamento import MeioPagamento
from cantina.pedido import Pedido


class Cantina:
    """Orquestra o fluxo, delegando cada parte para quem é responsável por ela.

    [Inversão de Dependências] Depende das abstrações MeioPagamento e
    Notificador, nunca de Pix, CreditoCarteirinha ou print(). Por isso aceitar
    um meio de pagamento novo não exige mudar esta classe (Aberto/Fechado).

    [Demeter] Só conversa com seus campos e parâmetros: pede pedido.total(),
    não percorre pedido.itens()[i].preco; pede fila.posicao(pedido), não
    mexe no deque interno da fila.
    """

    def __init__(self, notificador: Notificador, minutos_por_pedido: int = 2) -> None:
        self._notificador = notificador
        self._minutos_por_pedido = minutos_por_pedido
        self._fila = FilaCantina()
        self._senhas = count(1)

    def fazer_pedido(self, pedido: Pedido, meio: MeioPagamento) -> bool:
        if pedido.total() <= 0:
            raise ValueError("Pedido vazio: adicione itens antes de pagar.")
        resultado = meio.pagar(pedido.total())
        if not resultado.aprovado:
            self._avisar(pedido, f"❌ Pagamento recusado: {resultado.motivo}. Tente outro meio.")
            return False
        pedido.confirmar_pagamento(senha=next(self._senhas))
        self._fila.entrar(pedido)
        self._avisar(pedido, f"✅ Pedido #{pedido.senha} pago ({formatar(pedido.total())}). "
                             f"{self._situacao(pedido)}")
        return True

    def preparar_proximo(self) -> Optional[Pedido]:
        pedido = self._fila.proximo()
        if pedido is None:
            return None
        pedido.marcar_pronto()
        self._avisar(pedido, f"🍔 Pedido #{pedido.senha} pronto! Pode buscar no balcão.")
        self._atualizar_quem_espera()
        return pedido

    def posicao(self, pedido: Pedido) -> int:
        return self._fila.posicao(pedido)

    def estimativa_minutos(self, pedido: Pedido) -> int:
        return self.posicao(pedido) * self._minutos_por_pedido

    def _situacao(self, pedido: Pedido) -> str:
        return f"Você é o {self.posicao(pedido)}º da fila (~{self.estimativa_minutos(pedido)} min)."

    def _atualizar_quem_espera(self) -> None:
        for pedido in self._fila.aguardando():
            self._avisar(pedido, f"⏳ Andou! {self._situacao(pedido)}")

    def _avisar(self, pedido: Pedido, mensagem: str) -> None:
        self._notificador.notificar(pedido.aluno, mensagem)
