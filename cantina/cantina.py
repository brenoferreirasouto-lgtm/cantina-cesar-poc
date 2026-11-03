"""O fluxo do intervalo: pagar, entrar na fila, ser avisado, buscar o lanche."""
from __future__ import annotations

from itertools import count
from typing import Optional

from cantina.eventos import FilaAndou, PagamentoRecusado, PedidoPago, PedidoPronto
from cantina.fila import FilaCantina
from cantina.notificacao import Notificador
from cantina.pagamento import MeioPagamento
from cantina.pedido import Pedido


class Cantina:
    """Orquestra o fluxo, delegando cada parte para quem é responsável por ela.

    [Responsabilidade Única] Só decide O QUE acontece (cobrou, entrou na fila,
    ficou pronto) e publica eventos. COMO isso aparece para o aluno é problema
    do Notificador. Ver "A IA errou" no README.

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
            self._notificador.notificar(PagamentoRecusado(pedido.aluno, resultado.motivo))
            return False
        pedido.confirmar_pagamento(senha=next(self._senhas))
        self._fila.entrar(pedido)
        self._notificador.notificar(PedidoPago(
            pedido.aluno, pedido.senha, pedido.total(),
            self.posicao(pedido), self.estimativa_minutos(pedido)))
        return True

    def preparar_proximo(self) -> Optional[Pedido]:
        pedido = self._fila.proximo()
        if pedido is None:
            return None
        pedido.marcar_pronto()
        self._notificador.notificar(PedidoPronto(pedido.aluno, pedido.senha))
        self._atualizar_quem_espera()
        return pedido

    def posicao(self, pedido: Pedido) -> int:
        return self._fila.posicao(pedido)

    def estimativa_minutos(self, pedido: Pedido) -> int:
        return self.posicao(pedido) * self._minutos_por_pedido

    def _atualizar_quem_espera(self) -> None:
        for pedido in self._fila.aguardando():
            self._notificador.notificar(FilaAndou(
                pedido.aluno, self.posicao(pedido), self.estimativa_minutos(pedido)))
