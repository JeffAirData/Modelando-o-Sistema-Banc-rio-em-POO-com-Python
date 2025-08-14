#!/usr/bin/env python3

from datetime import datetime, date

MAX_TRANSACOES_DIA = 10


class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.contas = []

    def pode_transacionar(self, conta):
        hoje = date.today()
        realizadas = sum(
            1 for tx in conta.historico
            if tx["data"].date() == hoje
        )
        return realizadas < MAX_TRANSACOES_DIA

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Conta:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.saldo = 0.0
        self.historico = []

    def sacar(self, valor):
        if valor <= 0 or valor > self.saldo:
            print("@@@ Valor inválido ou saldo insuficiente @@@")
            return False
        self.saldo -= valor
        print("=== Saque realizado! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("@@@ Valor inválido @@@")
            return False
        self.saldo += valor
        print("=== Depósito realizado! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        hoje = date.today()
        saques_hoje = sum(
            1 for tx in self.historico
            if tx["tipo"] == "Saque" and tx["data"].date() == hoje
        )
        if saques_hoje >= self.limite_saques:
            print("@@@ Limite de saques diários excedido @@@")
            return False
        if valor > self.limite:
            print("@@@ Valor do saque excede o limite da conta @@@")
            return False
        return super().sacar(valor)


def registrar_transacao(conta, tipo, valor):
    conta.historico.append({
        "tipo": tipo,
        "valor": valor,
        "data": datetime.now()
    })


def buscar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def menu():
    return input(
        "\n=============== MENU ==============="
        "\n[d] Depositar    [s] Sacar    [e] Extrato"
        "\n[nu] Novo usuário    [nc] Nova conta    [lc] Listar contas"
        "\n[q] Sair"
        "\n=> "
    ).strip().lower()


def main():
    clientes = []
    contas = []

    while True:
        opc = menu()

        if opc == "nu":
            nome = input("Nome completo: ").strip()
            cpf = input("CPF (apenas números): ").strip()
            if buscar_cliente(cpf, clientes):
                print("@@@ Cliente já existe @@@")
                continue
            clientes.append(Cliente(nome, cpf))
            print("=== Usuário criado! ===")

        elif opc == "nc":
            cpf = input("CPF do titular: ").strip()
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("@@@ Cliente não encontrado @@@")
                continue
            numero = len(contas) + 1
            conta = ContaCorrente(numero, cliente)
            contas.append(conta)
            cliente.adicionar_conta(conta)
            print("=== Conta criada! ===")

        elif opc == "d":
            cpf = input("CPF do cliente: ").strip()
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("@@@ Cliente não encontrado @@@")
                continue
            conta = cliente.contas[0]
            if not cliente.pode_transacionar(conta):
                print("@@@ Limite de transações diárias atingido @@@")
                continue
            valor = float(input("Valor do depósito: "))
            if conta.depositar(valor):
                registrar_transacao(conta, "Deposito", valor)

        elif opc == "s":
            cpf = input("CPF do cliente: ").strip()
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("@@@ Cliente não encontrado @@@")
                continue
            conta = cliente.contas[0]
            if not cliente.pode_transacionar(conta):
                print("@@@ Limite de transações diárias atingido @@@")
                continue
            valor = float(input("Valor do saque: "))
            if conta.sacar(valor):
                registrar_transacao(conta, "Saque", valor)

        elif opc == "e":
            cpf = input("CPF do cliente: ").strip()
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("@@@ Cliente não encontrado @@@")
                continue
            conta = cliente.contas[0]
            print("\n===== EXTRATO =====")
            for tx in conta.historico:
                ts = tx["data"].strftime("%d-%m-%Y %H:%M:%S")
                print(f"{tx['tipo']} — {ts} — R$ {tx['valor']:.2f}")
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
            print("===================")

        elif opc == "lc":
            if not contas:
                print("@@@ Sem contas cadastradas @@@")
                continue
            print("\n===== LISTA DE CONTAS =====")
            for ct in contas:
                print(
                    f"Ag: {ct.agencia}  C/C: {ct.numero}  "
                    f"Titular: {ct.cliente.nome}  Saldo: R$ {ct.saldo:.2f}"
                )
            print("===========================")

        elif opc == "q":
            break

        else:
            print("@@@ Opção inválida @@@")


if __name__ == "__main__":
    main()
