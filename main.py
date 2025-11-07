import os
import time
import sys

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_and_clear():
    time.sleep(2)
    clear_console()

def exit():
    sys.exit()

login_coordenador = "teste@coordenador.educa"
senha_coordenador = "123456"

login_professor = "teste@professor.educa"
senha_professor = "123456"

login_aluno = "teste@aluno.educa"
senha_aluno = "123456"


def Verificar_Perfil(email):

    email_minusculo = email.lower()

    if email_minusculo.endswith("@coordenador.educa"):
        return "Perfil: Coordenador"
    elif email_minusculo.endswith("@professor.educa"):
        return "Perfil: Professor"
    elif email_minusculo.endswith("@aluno.educa"):
        return "Perfil: Aluno"
    else:
        return "E-mail informado está errado."


login_input = input("Digite o E-mail fornecido pela instituição: ")
clear_console()

while True:
    if login_input != login_coordenador and login_input != login_professor and login_input != login_aluno:

        login_input = input("E-mail inválido. Digite o E-mail fornecido pela instituição: ")
        clear_console()
    else:
        break

print(Verificar_Perfil(login_input))

senha_input = input("Digite a senha fornecida pela instituição: ")
clear_console()

while True:
    if (login_input == login_coordenador and senha_input != senha_coordenador) or \
       (login_input == login_professor and senha_input != senha_professor) or \
       (login_input == login_aluno and senha_input != senha_aluno):

        print(Verificar_Perfil(login_input))
        senha_input = input("Senha inválida. Digite a senha fornecida pela instituição: ")
        clear_console()
    else:
        print("Login realizado com sucesso!")
        pause_and_clear()
        break

def Login_Coordenador():
        if login_input == login_coordenador:
            print("Bem-vindo, Coordenador!")
            print("Escolha uma opção do menu para continuar.")

            print("\nOpção 1: Cadastrar Professor")
            print("Opção 2: Cadastrar Aluno")
            print("Opção 3: Cadastrar Curso")
            print("Opção 4: Cadastrar Turma")
            print("Opção 5: Sair")
            print("\n")

def Login_Professor():
    if login_input == login_professor:
        print("Bem-vindo, Professor!")
        print("Escolha uma opção do menu para continuar.")

        print("\nOpção 1: Adicionar Aluno à Turma")
        print("Opção 2: Visualizar Turmas")
        print("Opção 3: Postar Atividades")
        print("Opção 4: Visualizar Atividades")
        print("Opção 5: Lançar Notas")
        print("Opção 6: Visualizar Notas")
        print("Opção 7: Lançar Frequência")
        print("Opção 8: Visualizar Frequência")
        print("Opção 9: Sair")
        print("\n")

def Login_Aluno():
    if login_input == login_aluno:
        print("Bem-vindo, Aluno!")
        print("Escolha uma opção do menu para continuar.")

        print("\nOpção 1: Acessar Diario Eletrônico")
        print("Opção 2: Verificar Aulas")
        print("Opção 3: Verificar Atividades")
        print("Opção 4: Verificar Desempenho")
        print("Opção 5: Verificar Frequência")
        print("Opção 6: Sair")
        print("\n")

Login_Coordenador()
Login_Professor()
Login_Aluno()

def Login_Coordenador_Repetir():
        if login_input == login_coordenador:
            print("Escolha uma opção do menu para continuar.")

            print("\nOpção 1: Cadastrar Professor")
            print("Opção 2: Cadastrar Aluno")
            print("Opção 3: Cadastrar Curso")
            print("Opção 4: Cadastrar Turma")
            print("Opção 5: Sair")
            print("\n")

def Login_Professor_Repetir():
    if login_input == login_professor:
        print("Escolha uma opção do menu para continuar.")

        print("\nOpção 1: Adicionar Aluno à Turma")
        print("Opção 2: Visualizar Turmas")
        print("Opção 3: Postar Atividades")
        print("Opção 4: Visualizar Atividades")
        print("Opção 5: Lançar Notas")
        print("Opção 6: Visualizar Notas")
        print("Opção 7: Lançar Frequência")
        print("Opção 8: Visualizar Frequência")
        print("Opção 9: Sair")
        print("\n")

def Login_Aluno_Repetir():
    if login_input == login_aluno:
        print("Escolha uma opção do menu para continuar.")

        print("\nOpção 1: Acessar Diario Eletrônico")
        print("Opção 2: Verificar Aulas")
        print("Opção 3: Verificar Atividades")
        print("Opção 4: Verificar Desempenho")
        print("Opção 5: Verificar Frequência")
        print("Opção 6: Sair")
        print("\n")

def Sair():
    print("Saindo do sistema...")
    pause_and_clear()
    exit()

def Cadastrar_Professor():
    if login_input == login_coordenador:
        nome_professor = input("Digite o nome do professor: ")
        email_professor = input("Digite o e-mail do professor: ")
        senha_professor = input("Digite a senha do professor: ")
        clear_console()
        print(f"Professor \"{nome_professor}\" cadastrado com sucesso!")
        pause_and_clear()

def Cadastrar_Aluno():
    if login_input == login_coordenador:
        nome_aluno = input("Digite o nome do aluno: ")
        email_aluno = input("Digite o e-mail do aluno: ")
        senha_aluno = input("Digite a senha do aluno: ")
        clear_console()
        print(f"Aluno \"{nome_aluno}\" cadastrado com sucesso!")
        pause_and_clear()

def Cadastrar_Curso():
    if login_input == login_coordenador:
        nome_curso = input("Digite o nome do curso: ")
        descricao_curso = input("Digite a descrição do curso: ")
        clear_console()
        print(f"Curso \"{nome_curso}\" cadastrado com sucesso!")
        pause_and_clear()

def Cadastrar_Turma():
    if login_input == login_coordenador:
        nome_turma = input("Digite o nome da turma: ")
        curso_turma = input("Digite o curso da turma: ")
        clear_console()
        print(f"Turma \"{nome_turma}\" cadastrada com sucesso!")
        pause_and_clear()


def Menu_Coordenador():
    if login_input == login_coordenador:
        input_opção = input("Digite o número da opção desejada: ")
        clear_console()
    
        if input_opção == "1":
                Cadastrar_Professor()
        elif input_opção == "2":
            Cadastrar_Aluno()
        elif input_opção == "3":
            Cadastrar_Curso()
        elif input_opção == "4":
            Cadastrar_Turma()
        elif input_opção == "5":
            Sair()
        else:
            print("Opção inválida.")

def Adicionar_Aluno_Turma():
    if login_input == login_professor:
        nome_aluno = input("Digite o nome do aluno a ser adicionado à turma: ")
        nome_turma = input("Digite o nome da turma: ")
        clear_console()
        print(f"Aluno \"{nome_aluno}\" adicionado à turma \"{nome_turma}\" com sucesso!")
        pause_and_clear()

def Visualizar_Turmas():
    if login_input == login_professor:
        print("Visualizando turmas atribuídas ao professor...")
        pause_and_clear()

def Postar_Atividades():
    if login_input == login_professor:
        titulo_atividade = input("Digite o título da atividade: ")
        descricao_atividade = input("Digite a descrição da atividade: ")
        clear_console()
        print(f"Atividade \"{titulo_atividade}\" postada com sucesso!")
        pause_and_clear()

def Visualizar_Atividades():
    if login_input == login_professor:
        print("Visualizando atividades postadas...")
        pause_and_clear()

def Lançar_Notas():
    if login_input == login_professor:
        nome_aluno = input("Digite o nome do aluno: ")
        nota = input("Digite a nota a ser lançada: ")
        clear_console()
        print(f"Nota \"{nota}\" lançada para o aluno \"{nome_aluno}\" com sucesso!")
        pause_and_clear()

def Visualizar_Notas():
    if login_input == login_professor:
        print("Visualizando notas lançadas...")
        pause_and_clear()

def Lançar_Frequência():
    if login_input == login_professor:
        nome_aluno = input("Digite o nome do aluno: ")
        frequencia = input("Digite a frequência a ser lançada: ")
        clear_console()
        print(f"Frequência \"{frequencia}\" lançada para o aluno \"{nome_aluno}\" com sucesso!")
        pause_and_clear()

def Visualizar_Frequência():
    if login_input == login_professor:
        print("Visualizando frequências lançadas...")
        pause_and_clear()

def Menu_Professor():
    if login_input == login_professor:
        input_opção = input("Digite o número da opção desejada: ")
        clear_console()
     
        if input_opção == "1":
            Adicionar_Aluno_Turma()
        elif input_opção == "2":
            Visualizar_Turmas()
        elif input_opção == "3":
            Postar_Atividades()
        elif input_opção == "4":
            Visualizar_Atividades()
        elif input_opção == "5":
            Lançar_Notas()
        elif input_opção == "6":
            Visualizar_Notas()
        elif input_opção == "7":
            Lançar_Frequência()
        elif input_opção == "8":
            Visualizar_Frequência()
        elif input_opção == "9":
            Sair()
        else:
            print("Opção inválida.")   

def Acessar_Diario_Eletronico():
    if login_input == login_aluno:
        print("Acessando diário eletrônico...")
        pause_and_clear()

def Verificar_Aulas():
    if login_input == login_aluno:
        print("Verificando aulas...")
        pause_and_clear()

def Verificar_Atividades():
    if login_input == login_aluno:
        print("Verificando atividades...")
        pause_and_clear()

def Verificar_Desempenho():
    if login_input == login_aluno:
        print("Verificando desempenho...")
        pause_and_clear()

def Verificar_Frequência():
    if login_input == login_aluno:
        print("Verificando frequência...")
        pause_and_clear()

def Menu_Aluno():
    if login_input == login_aluno:
        input_opção = input("Digite o número da opção desejada: ")
        clear_console()
    
        if input_opção == "1":
            Acessar_Diario_Eletronico()
        elif input_opção == "2":
            Verificar_Aulas()
        elif input_opção == "3":
            Verificar_Atividades()
        elif input_opção == "4":
            Verificar_Desempenho()
        elif input_opção == "5":
            Verificar_Frequência()
        elif input_opção == "6":
            Sair()
        else:
            print("Opção inválida.")

Menu_Coordenador()
Menu_Professor()
Menu_Aluno()

print("Deseja realizar outra operação? (s/n)")

while True:
    repetir = input().lower()
    clear_console()
    if repetir == "s":
        Login_Coordenador_Repetir()
        Menu_Coordenador()
        Login_Professor_Repetir()
        Menu_Professor()
        Login_Aluno_Repetir()
        Menu_Aluno()
        print("Deseja realizar outra operação? (s/n)")
    elif repetir == "n":
        print("Obrigado por usar o sistema. Até logo!")
        Sair()
    else:
        print("Opção inválida. Digite 's' para sim ou 'n' para não.")