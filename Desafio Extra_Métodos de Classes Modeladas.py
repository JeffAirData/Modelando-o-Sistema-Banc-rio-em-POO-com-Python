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

# Histórico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
        })

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
            print("✅ Depósito realizado com sucesso.")
        else:
            print("❌ Operação falhou! Valor inválido.")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print("✅ Saque realizado com sucesso.")
        else:
            print("❌ Saque não realizado.")

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
            print("❌ Saldo + limite insuficiente.")
            return False
        if self.saques_realizados >= self.limite_saques:
            print("❌ Limite diário de saques excedido.")
            return False
        if valor <= 0:
            print("❌ Valor inválido.")
            return False
        self.saldo -= valor
        self.saques_realizados += 1
        return True

# Funções de interface
def exibir_menu():
    print("\n=== MENU ===")
    print("[d] Depositar")
    print("[s] Sacar")
    print("[e] Extrato")
    print("[1] Criar Usuário")
    print("[2] Criar Conta")
    print("[3] Listar Contas")
    print("[q] Sair")

def exibir_extrato(conta):
    print("\n🧾 === EXTRATO ===")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"\n💰 Saldo atual: R$ {conta.saldo_atual():.2f}")
    print("===================")

def criar_usuario(lista_usuarios):
    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    nascimento = input("Data de nascimento (aaaa-mm-dd): ")
    endereco = input("Endereço: ")

    if any(u.cpf == cpf for u in lista_usuarios):
        print("❌ Usuário já cadastrado.")
        return None

    try:
        data_nascimento = date.fromisoformat(nascimento)
    except ValueError:
        print("❌ Data inválida.")
        return None

    cliente = Cliente(nome, cpf, data_nascimento, endereco)
    lista_usuarios.append(cliente)
    print("✅ Usuário criado com sucesso!")
    return cliente

def criar_conta(lista_usuarios, lista_contas):
    cpf = input("CPF do titular: ")
    cliente = next((u for u in lista_usuarios if u.cpf == cpf), None)

    if not cliente:
        print("❌ Usuário não encontrado.")
        return

    numero = len(lista_contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero)
    cliente.adicionar_conta(conta)
    lista_contas.append(conta)
    print("✅ Conta criada com sucesso!")

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Titular: {conta.cliente.nome}, Saldo: R$ {conta.saldo_atual():.2f}")

# Execução principal
def main():
    usuarios = []
    contas = []

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").lower()

        if opcao == "d":
            cpf = input("CPF do titular: ")
            cliente = next((u for u in usuarios if u.cpf == cpf), None)
            if cliente and cliente.contas:
                valor = float(input("Valor do depósito: R$ "))
                deposito = Deposito(valor)
                cliente.realizar_transacao(cliente.contas[0], deposito)
            else:
                print("❌ Cliente ou conta não encontrada.")

        elif opcao == "s":
            cpf = input("CPF do titular: ")
            cliente = next((u for u in usuarios if u.cpf == cpf), None)
            if cliente and cliente.contas:
                valor = float(input("Valor do saque: R$ "))
                saque = Saque(valor)
                cliente.realizar_transacao(cliente.contas[0], saque)
            else:
                print("❌ Cliente ou conta não encontrada.")

        elif opcao == "e":
            cpf = input("CPF do titular: ")
            cliente = next((u for u in usuarios if u.cpf == cpf), None)
            if cliente and cliente.contas:
                exibir_extrato(cliente.contas[0])
            else:
                print("❌ Cliente ou conta não encontrada.")

        elif opcao == "1":
            criar_usuario(usuarios)

        elif opcao == "2":
            criar_conta(usuarios, contas)

        elif opcao == "3":
            listar_contas(contas)

        elif opcao == "q":
            print("👋 Sessão encerrada. Obrigado por usar o Banco DIO Jefferson Edition!")
            break

        else:
            print("⚠️ Opção inválida. Tente novamente.")

main()
