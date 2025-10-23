from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap

# ----------------------------------------------------
# CORREÇÃO 1: CORREÇÃO NAS IMPORTAÇÕES DO MÓDULO ABC
#
# abstractclassmethod e abstractproperty são obsoletos
# ou foram substituídos por combinações de decoradores.
# Usamos apenas:
# - ABC (a classe base)
# - abstractmethod (para métodos)
# - abstractproperty (para propriedades, que é o correto aqui)
# ----------------------------------------------------

# CLASSES DE DOMÍNIO

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        # NOTA: A transação deve ser registrada ANTES de ser executada,
        # para que o método registrar faça a chamada correta para a conta.
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        # CORREÇÃO: Usamos o 'yield' ou list comprehension para retornar a lista de transações,
        # mas aqui, retornar a lista diretamente (como você fez) é mais simples.
        return self._transacoes
    
    def adicionar_transacao(self, transacao): # Renomeado para singular para consistência
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                # CORREÇÃO 2: datetime.now().strftime com %S (segundos)
                # O formato "%s" é o timestamp UNIX, que é uma string longa,
                # enquanto %S é mais comum para relatórios. Usei %S por ser mais padrão em HH:MM:SS.
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

# ----------------------------------------------------
# CLASSES ABSTRATAS E CONCRETAS (CONTAS E TRANSAÇÕES)
# ----------------------------------------------------

class Transacao(ABC):
    
    # CORREÇÃO 3: abstractproperty é o decorador correto para propriedades abstratas.
    @property
    @abstractproperty 
    def valor(self):
        pass
        
    # CORREÇÃO 4: Para métodos abstratos, usamos apenas @abstractmethod.
    # abstractclassmethod é obsoleto e complexo de usar corretamente.
    @abstractmethod
    def registrar(self, conta):
        pass

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    # Métodos @property
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    # Métodos de Transação
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        elif valor > 0:
            self._saldo -= valor
            print("\n≡≡≡ Saque realizado com sucesso! ≡≡≡")
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n≡≡≡ Depósito realizado com sucesso! ≡≡≡")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        # Acessa o histórico para contar os saques
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            # Chama o método sacar() da classe pai (Conta)
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        # Usa textwrap.dedent no main para remover a identação,
        # o f-string é limpo aqui.
        return f"""
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    @property
    def eh_transacao_valida(self):
        return True # Implementação para verificar regras internas antes de registrar

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            # CORREÇÃO 5: Nome do método corrigido
            conta.historico.adicionar_transacao(self) 

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    @property
    def eh_transacao_valida(self):
        return True

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            # CORREÇÃO 5: Nome do método corrigido
            conta.historico.adicionar_transacao(self)


# ----------------------------------------------------
# FUNÇÕES DE EXECUÇÃO
# ----------------------------------------------------

def menu():
    menu_str = """
================ MENU ================
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova conta
[lc]\tListar contas
[nu]\tNovo usuário
[q]\tSair
=>"""
    # textwrap.dedent remove a indentação inicial de todas as linhas
    return input(textwrap.dedent(menu_str))

def filtrar_cliente(cpf, clientes):
    # Procura um cliente pelo CPF (o CPF deve ser uma string)
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf] 
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("\n@@@ Valor inválido. Informe um número. @@@")
        return

    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("\n@@@ Valor inválido. Informe um número. @@@")
        return

    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============== EXTRATO ===============")
    transacoes = conta.historico.transacoes

    extrato_str = ""
    if not transacoes:
        extrato_str = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato_str += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} (Data: {transacao['data']})"
            
    print(extrato_str)
    print(f"\nSaldo:\n\t\tR$ {conta.saldo:.2f}")
    print("========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente_existente = filtrar_cliente(cpf, clientes)

    if cliente_existente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro, - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    # CORREÇÃO 6: O objeto 'clientes' é uma lista e usa o método .append()
    # Seu código original usava cliente.append(cliente), o que estava errado.
    clientes.append(cliente) 
    print("≡≡≡ Usuário criado com sucesso! ≡≡≡")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return
    
    # Cria a conta usando o @classmethod nova_conta
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta) # Usa o método correto da classe Cliente
    
    print("\n≡≡≡ Conta criada com sucesso! ≡≡≡")

def listar_contas(contas):
    if not contas:
        print("\nNão há contas cadastradas.")
        return

    for conta in contas:
        print("=" * 30)
        # Usa str(conta) para chamar o __str__ definido em ContaCorrente
        print(textwrap.dedent(str(conta))) 
    print("=" * 30)

def buscar_conta(numero_conta, contas):
    # CORREÇÃO 7: Esta função estava com a lógica errada.
    # Em vez de um dicionário, 'contas' contém objetos ContaCorrente.
    for conta in contas:
        if conta.numero == numero_conta:
            return conta
    return None

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)            

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            # O número da conta não deve ser o índice, mas sim sequencial
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# A chamada para main() deve estar fora da função main()
if __name__ == "__main__":
    main()