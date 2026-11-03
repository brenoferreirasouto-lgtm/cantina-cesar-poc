"""Como o aluno fica sabendo das coisas."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Notificador(ABC):
    """[Inversão de Dependências] A Cantina avisa por esta abstração, não por print().

    Hoje os avisos vão para o terminal; amanhã podem ir para push no celular,
    WhatsApp ou um painel na parede da cantina. Basta outra implementação.
    Nos testes usamos uma que só guarda as mensagens numa lista.
    """

    @abstractmethod
    def notificar(self, aluno: str, mensagem: str) -> None:
        ...


class NotificadorConsole(Notificador):
    def notificar(self, aluno: str, mensagem: str) -> None:
        print(f"   📱 [{aluno}] {mensagem}")
