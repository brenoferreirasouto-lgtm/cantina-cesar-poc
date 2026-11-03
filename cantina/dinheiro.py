"""Dinheiro sempre em centavos (int).

[Integridade conceitual] Uma única representação de valor monetário em todo
o sistema. A versão go-horse misturava float (6.5, total * 0.9), o que gera
erros de arredondamento (0.1 + 0.2 != 0.3). Aqui, todo preço, desconto e
saldo é um int em centavos, e só este módulo sabe transformar isso em texto.
"""


def formatar(centavos: int) -> str:
    """650 -> 'R$ 6,50'."""
    sinal = "-" if centavos < 0 else ""
    reais, resto = divmod(abs(centavos), 100)
    return f"{sinal}R$ {reais},{resto:02d}"
