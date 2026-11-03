"""Um intervalo de 15 minutos na Cantina CESAR.

Rode: python demo.py
"""
from cantina.cantina import Cantina
from cantina.cardapio import cardapio_do_dia
from cantina.descontos import DescontoCombo
from cantina.dinheiro import formatar
from cantina.notificacao import NotificadorConsole
from cantina.pagamento import CreditoCarteirinha, Pix
from cantina.pedido import Pedido

MINUTOS_POR_PEDIDO = 2


def etapa(texto: str) -> None:
    print(f"\n▶ {texto}")


def mostrar_cardapio(cardapio) -> None:
    print("Cardápio do dia  (lanche + bebida = combo com 10% de desconto)")
    for produto in cardapio:
        print(f"   {produto.nome:.<24} {formatar(produto.preco)}")


def main() -> None:
    print("☕ CANTINA CESAR · 15 minutos de intervalo, zero minutos de fila\n")
    cardapio = cardapio_do_dia()
    mostrar_cardapio(cardapio)

    cantina = Cantina(NotificadorConsole(), minutos_por_pedido=MINUTOS_POR_PEDIDO)
    combo = DescontoCombo(percentual=10)

    etapa("Ana pede Coxinha + Suco de laranja (combo) ainda na aula, e paga no Pix")
    ana = Pedido("Ana", combo)
    ana.adicionar(cardapio.buscar("Coxinha"))
    ana.adicionar(cardapio.buscar("Suco de laranja"))
    cantina.fazer_pedido(ana, Pix(saldo_conta=5000))

    etapa("Bruno pede 2 Pães de queijo + Café e paga com a carteirinha")
    bruno = Pedido("Bruno", combo)
    bruno.adicionar(cardapio.buscar("Pão de queijo"), quantidade=2)
    bruno.adicionar(cardapio.buscar("Café"))
    cantina.fazer_pedido(bruno, CreditoCarteirinha(creditos=2500))

    etapa("Caio pede Sanduíche natural + Brigadeiro, mas a carteirinha está quase zerada")
    caio = Pedido("Caio", combo)
    caio.adicionar(cardapio.buscar("Sanduíche natural"))
    caio.adicionar(cardapio.buscar("Brigadeiro"))
    cantina.fazer_pedido(caio, CreditoCarteirinha(creditos=300))

    etapa("Caio tenta de novo, agora no Pix")
    cantina.fazer_pedido(caio, Pix(saldo_conta=2000))

    etapa("Toca o sinal do intervalo. A cozinha começa a entregar 🍳")
    preparados = 0
    while cantina.preparar_proximo():
        preparados += 1

    sobra = 15 - preparados * MINUTOS_POR_PEDIDO
    print(f"\nFila zerada em ~{preparados * MINUTOS_POR_PEDIDO} min: "
          f"sobram {sobra} dos 15 minutos para comer com calma. 😌")


if __name__ == "__main__":
    main()
