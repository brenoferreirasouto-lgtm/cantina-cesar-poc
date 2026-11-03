"""Como o aluno fica sabendo das coisas."""
from __future__ import annotations

from abc import ABC, abstractmethod

from cantina.dinheiro import formatar
from cantina.eventos import FilaAndou, PagamentoRecusado, PedidoPago, PedidoPronto


class Notificador(ABC):
    """[Inversão de Dependências] A Cantina avisa por esta abstração, não por print().

    [Segregação de Interfaces] Um único método, que recebe um evento de
    cantina/eventos.py. Um painel na parede que só mostra "pedido pronto" pode
    ignorar os outros eventos, sem ser obrigado a implementar métodos inúteis.
    """

    @abstractmethod
    def notificar(self, evento) -> None:
        ...


def _espera(posicao: int, minutos: int) -> str:
    return f"Você é o {posicao}º da fila (~{minutos} min)."


class NotificadorConsole(Notificador):
    """[Responsabilidade Única] Toda a apresentação mora aqui: texto, emoji e R$.

    Mudar a frase de "pedido pronto" ou traduzir o app para inglês mexe só
    nesta classe; a Cantina e seus testes não mudam.
    """

    _TEXTOS = {
        PagamentoRecusado: lambda e: f"❌ Pagamento recusado: {e.motivo}. Tente outro meio.",
        PedidoPago: lambda e: f"✅ Pedido #{e.senha} pago ({formatar(e.valor)}). "
                              f"{_espera(e.posicao, e.minutos)}",
        FilaAndou: lambda e: f"⏳ Andou! {_espera(e.posicao, e.minutos)}",
        PedidoPronto: lambda e: f"🍔 Pedido #{e.senha} pronto! Pode buscar no balcão.",
    }

    def notificar(self, evento) -> None:
        texto = self._TEXTOS[type(evento)](evento)
        print(f"   📱 [{evento.aluno}] {texto}")
