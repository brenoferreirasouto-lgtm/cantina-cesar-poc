"""Prova real do Aberto/Fechado: um meio de pagamento novo, sem editar nada.

Rode: python demo_voucher.py
"""
from cantina.cantina import Cantina
from cantina.cardapio import cardapio_do_dia
from cantina.descontos import DescontoCombo
from cantina.notificacao import NotificadorConsole
from cantina.pedido import Pedido
from extensoes.voucher import VoucherCesar


def etapa(texto: str) -> None:
    print(f"\n▶ {texto}")


def main() -> None:
    print("🎟️  NOVIDADE NA CANTINA: Voucher CESAR")
    print("   Arquivos de cantina/ alterados para isso: nenhum.")
    print("   Confira: git show --stat prova-aberto-fechado")

    cardapio = cardapio_do_dia()
    cantina = Cantina(NotificadorConsole())
    voucher = VoucherCesar(codigo="TECHDESIGN-15", valor=1500)

    etapa("Duda ganhou um voucher de R$ 15,00 na palestra e pede Sanduíche natural + Café")
    duda = Pedido("Duda", DescontoCombo(percentual=10))
    duda.adicionar(cardapio.buscar("Sanduíche natural"))
    duda.adicionar(cardapio.buscar("Café"))
    cantina.fazer_pedido(duda, voucher)

    etapa("Duda tenta usar o mesmo voucher para um Brigadeiro")
    sobremesa = Pedido("Duda")
    sobremesa.adicionar(cardapio.buscar("Brigadeiro"))
    cantina.fazer_pedido(sobremesa, voucher)

    etapa("Edu tenta pagar 3 Coxinhas com um voucher de R$ 10,00")
    edu = Pedido("Edu")
    edu.adicionar(cardapio.buscar("Coxinha"), quantidade=3)
    cantina.fazer_pedido(edu, VoucherCesar(codigo="CALOURO-10", valor=1000))

    etapa("A cozinha prepara")
    while cantina.preparar_proximo():
        pass


if __name__ == "__main__":
    main()
