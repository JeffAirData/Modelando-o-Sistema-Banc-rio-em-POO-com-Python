from datetime import date

# Pessoa Física
class PessoaFisica:
    def __init__(self, nome: str, cpf: str, data_nascimento: date):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# Cliente
class Cliente(PessoaFisica):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(nome, cpf, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

# Transações
class Transacao:
    def registrar(self, conta):
        raise NotImplementedError("Implementar método registrar")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

# Histórico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
        })

# Conta
class Conta:
    def __init__(self, numero: int, cliente: Cliente, agencia: str = "0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor: float) -> bool:
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.saldo += valor
            return True
        return False

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)

# Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, agencia="0001", limite=500.0, limite_saques=3):
        super().__init__(numero, cliente, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor: float) -> bool:
        if valor > self.saldo + self.limite:
            return False
        if self.saques_realizados >= self.limite_saques:
            return False
        if valor > 0:
            self.saldo -= valor
            self.saques_realizados += 1
            return True
        return False

# Execução de exemplo
if __name__ == "__main__":
    cliente = Cliente("Jefferson Melo", "12345678900", date(1990, 5, 20), "Rua Python, 42")
    conta = ContaCorrente.nova_conta(cliente, numero=1)
    cliente.adicionar_conta(conta)

    deposito = Deposito(1000)
    saque = Saque(200)

    cliente.realizar_transacao(conta, deposito)
    cliente.realizar_transacao(conta, saque)

    print(f"Saldo final: R$ {conta.saldo_atual():.2f}")
    print("Histórico de transações:")
    for t in conta.historico.transacoes:
        print(f"{t['tipo']}: R$ {t['valor']:.2f}")
