"""Complexidade ciclomática das duas versões (seção 5.7 do livro).

CC de McCabe = número de decisões + 1. Contamos como decisão: if/elif, for,
while, except, assert, expressão condicional (x if c else y), cada for/if
dentro de compreensões e cada and/or. Calculado aqui mesmo com o módulo ast
da biblioteca padrão, sem instalar nada. Métodos abstratos (sem corpo) ficam
de fora para não inflar a média.

CC também é o número de caminhos independentes de uma função, ou seja, o
mínimo de casos de teste para percorrer todos eles.

Rode: python metricas.py
"""
import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
VERSOES = [
    ("GO-HORSE (Entrega 1)", ["go_horse"]),
    ("POC FINAL", ["cantina", "extensoes"]),
]
DECISOES = (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.Assert)
ESCOPOS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def contar_decisoes(no):
    total = 0
    for filho in ast.iter_child_nodes(no):
        if isinstance(filho, ESCOPOS):
            continue  # funções e classes internas são medidas separadamente
        if isinstance(filho, DECISOES):
            total += 1
        elif isinstance(filho, ast.comprehension):
            total += 1 + len(filho.ifs)
        elif isinstance(filho, ast.BoolOp):
            total += len(filho.values) - 1
        total += contar_decisoes(filho)
    return total


def eh_abstrato(funcao):
    return any(getattr(d, "id", getattr(d, "attr", "")) == "abstractmethod"
               for d in funcao.decorator_list)


def funcoes(arvore, prefixo=""):
    for no in ast.iter_child_nodes(arvore):
        if isinstance(no, ast.ClassDef):
            yield from funcoes(no, f"{prefixo}{no.name}.")
        elif isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield f"{prefixo}{no.name}", no
            yield from funcoes(no, f"{prefixo}{no.name}.")


def medir(pastas):
    medidas = []
    for pasta in pastas:
        for arquivo in sorted((RAIZ / pasta).rglob("*.py")):
            arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
            for nome, no in funcoes(arvore):
                if not eh_abstrato(no):
                    loc = no.end_lineno - no.lineno + 1
                    medidas.append((contar_decisoes(no) + 1, loc, nome))
    return sorted(medidas, reverse=True)


def relatorio(titulo, pastas):
    medidas = medir(pastas)
    print(f"\n{titulo}  ·  {' + '.join(p + '/' for p in pastas)}")
    print("   CC  LOC  função")
    relevantes = [m for m in medidas if m[0] > 1]
    for cc, loc, nome in relevantes:
        print(f"  {cc:>3}  {loc:>3}  {nome:<34} {'█' * cc}")
    simples = len(medidas) - len(relevantes)
    if simples:
        print(f"    1    ·  + {simples} funções sem nenhuma decisão")
    ccs = [m[0] for m in medidas]
    print(f"  → pior: {max(ccs)}  ·  média: {sum(ccs) / len(ccs):.1f}  ·  "
          f"funções: {len(ccs)}  ·  acima de 10: {sum(cc > 10 for cc in ccs)}")
    return medidas[0]


def main():
    print("COMPLEXIDADE CICLOMÁTICA  (CC = decisões + 1)")
    print("Escala de McCabe: 1–10 simples · 11–20 moderada · 21+ complexa")
    piores = [relatorio(titulo, pastas) for titulo, pastas in VERSOES]
    (cc_antes, _, nome_antes), (cc_depois, _, nome_depois) = piores
    queda = 100 * (cc_antes - cc_depois) / cc_antes
    print(f"\nRESULTADO: a pior função caiu de CC {cc_antes} ({nome_antes}) "
          f"para CC {cc_depois} ({nome_depois}), {queda:.0f}% menor.")
    print(f"Cobrir os caminhos independentes de {nome_antes} exige pelo menos {cc_antes} testes;"
          f" na versão final, nenhuma função passa de {cc_depois}.")


if __name__ == "__main__":
    main()
