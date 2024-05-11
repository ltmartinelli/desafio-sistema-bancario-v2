menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[c] Cadastrar Cliente
[cc] Criar Conta Corrente
[lc] Lista de Clientes
[lcc] Lista de Contas Corrente
[q] Sair
=> """

LIMITE_SAQUES = 3
AGENCIA = "0001"

saldo = 0
limite = 500.00
extrato = ""
numero_saques = 0
realizou_movimentacoes = False
clientes = []
contas = []


def cadastrar_cliente(lista):
    print("Digite os dados do cliente: ")
    cliente = {key: input(f"{key.title()}: ") for key in ("nome", "data de nascimento", "cpf", "endereço")}
    if any(cliente['cpf'] == cliente_cadastrado['cpf'] for cliente_cadastrado in lista):
        print('\nErro! CPF já cadastrado')
    else:
        lista.append(cliente)
        print("\nCliente cadastrado com sucesso")
    return lista


def criar_conta(agencia, numero_conta, lista):
    cpf = input("Informe o CPF do usuário: ")
    for cliente in lista:
        if cliente["cpf"] == cpf:
            print("Conta criada com sucesso!")
            return {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}
    else:
        print("\nCliente não encontrado!")


def listar_clientes(lista):
    if not lista:
        print("Sem clientes cadastrados")
    else:
        for cliente in lista:
            print(cliente)


def listar_contas(lista):
    if not lista:
        print("Sem contas cadastradas")
    else:
        for conta in lista:
            conta_impressa = f"""
Agência: {conta['agencia']}\n
Número: {conta['numero_conta']}\n
Titular: {conta['cliente']['nome']}\n
{"#" * 100}
"""
            print(conta_impressa)


def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: + R$ {valor:.2f}\n'
    else:
        print('Apenas valores positivos!')
    return saldo, extrato


def saque(*, valor, saldo, extrato, limite, numero_saques):
    if valor > limite:
        print(f'Valor inválido, o limite de saque é de R$ {limite:.2f}')
    elif valor > saldo:
        print(f'Você não possui saldo o suficiente. Seu saldo é de R$ {saldo:.2f}')
    elif valor <= 0:
        print(f'Valor inválido, o saque deve ser maior que R$ 0.00')
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f'Saque: - R$ {valor:.2f}\n'
        print('Operação concluída!')
    return saldo, extrato, numero_saques


def imprimir_extrato(saldo, /, *, extrato):
    print('\n============EXTRATO=============:\n')
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f'Saldo Final = R$ {saldo:.2f}:')
    print('\n===============================:\n')


while True:

    opcao = input(menu)

    if opcao == 'd':
        valor = float(input('Quanto você quer depositar? '))
        saldo, extrato = deposito(saldo, valor, extrato)
    elif opcao == 's':
        if numero_saques >= LIMITE_SAQUES:
            print('Limite de saques diário atingido! Tente novamente amanhã.')
        else:
            valor = float(input('Quanto você quer sacar?'))
            saldo, extrato, numero_saques = saque(valor=valor, saldo=saldo, extrato=extrato, limite=limite,
                                                  numero_saques=numero_saques)
    elif opcao == 'e':
        imprimir_extrato(saldo, extrato=extrato)
    elif opcao == 'c':
        clientes = cadastrar_cliente(clientes)
    elif opcao == 'cc':
        numero = len(contas) + 1
        conta = criar_conta(AGENCIA, numero, clientes)
        if conta:
            contas.append(conta)
    elif opcao == 'lc':
        listar_clientes(clientes)
    elif opcao == 'lcc':
        listar_contas(contas)
    elif opcao == 'q':
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
