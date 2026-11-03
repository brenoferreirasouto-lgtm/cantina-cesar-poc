"""O que aconteceu com um pedido, sem dizer COMO isso é mostrado ao aluno.

[Responsabilidade Única] A Cantina publica estes fatos; quem transforma fato
em texto, emoji ou push no celular é a implementação de Notificador.
[Acoplamento] Os eventos carregam só dados simples (nome, senha, valores), então
quem os recebe não precisa conhecer Pedido, FilaCantina nem Cantina.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class PagamentoRecusado:
    aluno: str
    motivo: str


@dataclass(frozen=True)
class PedidoPago:
    aluno: str
    senha: int
    valor: int  # centavos
    posicao: int
    minutos: int


@dataclass(frozen=True)
class FilaAndou:
    aluno: str
    posicao: int
    minutos: int


@dataclass(frozen=True)
class PedidoPronto:
    aluno: str
    senha: int
