# Cantina CESAR - versao go-horse (Entrega 1)
# Feito em 24h, "funciona na minha maquina".
# Mantido aqui SO para a comparacao antes/depois com a PoC final em cantina/.
# Rode: python go_horse/cantina_go_horse.py

fila = []  # fila global: qualquer parte do codigo le e altera
senha_atual = 0
saldos_carteirinha = {"Bruno": 25.0, "Caio": 3.0}


def processar_pedido(nome, itens, forma_pagamento, saldo=0):
    global senha_atual
    total = 0
    tem_lanche = False
    tem_bebida = False
    for item in itens:
        if item == "coxinha":
            total = total + 6.5
            tem_lanche = True
        elif item == "pao de queijo":
            total = total + 4.5
            tem_lanche = True
        elif item == "sanduiche":
            total = total + 9
            tem_lanche = True
        elif item == "suco":
            total = total + 6
            tem_bebida = True
        elif item == "cafe":
            total = total + 4
            tem_bebida = True
        elif item == "brigadeiro":
            total = total + 3
        else:
            print("item nao existe: " + item)
            return False
    if tem_lanche and tem_bebida:
        total = total * 0.9  # combo
    if forma_pagamento == "pix":
        if saldo < total:
            print(nome + ", pix recusado: saldo insuficiente")
            return False
    elif forma_pagamento == "carteirinha":
        if saldos_carteirinha.get(nome, 0) < total:
            print(nome + ", carteirinha sem credito")
            return False
        saldos_carteirinha[nome] = saldos_carteirinha[nome] - total
    else:
        print("forma de pagamento invalida")
        return False
    senha_atual = senha_atual + 1
    fila.append([senha_atual, nome, itens, total])
    print(nome + ", pedido " + str(senha_atual) + " pago! R$" + str(round(total, 2))
          + " - posicao na fila: " + str(len(fila)) + " (~" + str(len(fila) * 2) + " min)")
    return True


def preparar():
    if len(fila) > 0:
        p = fila.pop(0)
        print(p[1] + ", seu pedido " + str(p[0]) + " ficou pronto!")
        for i in range(len(fila)):
            print(fila[i][1] + ", agora voce e o " + str(i + 1) + " da fila")


if __name__ == "__main__":
    processar_pedido("Ana", ["coxinha", "suco"], "pix", 50)
    processar_pedido("Bruno", ["pao de queijo", "cafe"], "carteirinha")
    processar_pedido("Caio", ["sanduiche", "brigadeiro"], "carteirinha")
    processar_pedido("Caio", ["sanduiche", "brigadeiro"], "pix", 20)
    # alguem "so queria ver a fila" e acabou apagando o pedido do Bruno:
    fila.pop(1)
    preparar()
    preparar()
    preparar()
