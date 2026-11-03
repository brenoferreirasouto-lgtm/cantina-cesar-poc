"""[Substituição de Liskov] O contrato que todo MeioPagamento precisa cumprir.

Os testes são escritos UMA vez, contra a abstração. Cada meio concreto herda
este mixin e só diz como criar uma instância com um certo saldo. Se algum
meio quebrar o contrato (lançar exceção numa recusa, debitar sem aprovar,
devolver None...), a Cantina deixaria de funcionar com ele, e o teste acusa.
"""
from cantina.pagamento import MeioPagamento, ResultadoPagamento


class ContratoMeioPagamento:
    def criar_meio(self, saldo: int) -> MeioPagamento:
        raise NotImplementedError

    def test_aprova_e_debita_quando_o_saldo_cobre(self):
        meio = self.criar_meio(saldo=1000)
        self.assertIsInstance(meio, MeioPagamento)

        self.assertTrue(meio.pagar(600).aprovado)
        self.assertFalse(meio.pagar(600).aprovado,
                         "o primeiro pagamento deveria ter consumido o saldo")

    def test_recusa_sem_excecao_e_sem_debitar(self):
        meio = self.criar_meio(saldo=1000)

        recusa = meio.pagar(5000)

        self.assertIsInstance(recusa, ResultadoPagamento)
        self.assertFalse(recusa.aprovado)
        self.assertTrue(recusa.motivo, "a recusa precisa explicar o motivo ao aluno")
        self.assertTrue(meio.pagar(1000).aprovado, "a recusa não pode ter consumido saldo")
