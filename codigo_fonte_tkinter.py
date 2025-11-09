import customtkinter as ctk
from chat_history import load_chat_history, save_chat_history

# =========================================================
# REGIÃO: VARIÁVEIS DE ESTADO GLOBAL E CREDENCIAIS FIXAS
# =========================================================

# Versão do Aplicativo
APP_VERSION = "v1.0.0"

# Credenciais Fictícias (Recuperadas para testes sem DB)
login_coordenador = "teste@coordenador.educa"
senha_coordenador = "123456"

login_professor = "teste@professor.educa"
senha_professor = "123456"

login_aluno = "teste@aluno.educa"
senha_aluno = "123456"

# DICIONÁRIO DE MAPEAMENTO
CREDENCIAS = {
    login_coordenador: {"senha": senha_coordenador, "perfil": "Coordenador"},
    login_professor: {"senha": senha_professor, "perfil": "Professor"},
    login_aluno: {"senha": senha_aluno, "perfil": "Aluno"},
}

# Variáveis de Estado
email_validado = None
perfil_logado = None

# Variáveis globais para os Entrys
professor_nome_entry = None
professor_email_entry = None
professor_senha_entry = None
professor_status_label = None 

professor_email_excluir_entry = None
professor_exclusao_status_label = None

aluno_email_excluir_entry = None
aluno_exclusao_status_label = None

curso_nome_excluir_entry = None
curso_exclusao_status_label = None

turma_nome_excluir_entry = None
turma_exclusao_status_label = None

# Widgets da tela de login
label_bem_vindo = None
resultado_label = None
email_entry = None
button_email = None
senha_entry = None
button_login = None
btn_mode_toggle = None
btn_exit = None

# HISTÓRICO DE CHAT SIMULADO
try:
    MENSAGENS_CHAT = load_chat_history()
except Exception as e:
    print(f"Erro ao carregar histórico do chat: {e}")
    MENSAGENS_CHAT = [{"perfil": "Sistema", "texto": "Início da Conversa"}]

# Dimensões Padrão da Janela
JANELA_WIDTH = 400
JANELA_HEIGHT = 300 

# Tupla de cores para visibilidade
TEMA_TEXT_COLOR = ("black", "white")

# Variáveis de Fonte (Serão inicializadas após ctk.CTk())
fonte_titulo = None
fonte_subtitulo = None
fonte_campos = None
fonte_botoes = None

# =========================================================
# REGIÃO: FUNÇÕES DE UTILIDADE (LAYOUT E LÓGICA CENTRAL)
# =========================================================

def center_window(app, width, height):
    """Calcula a posição e centraliza a janela principal na tela."""
    app.update_idletasks()
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()
    x = int((largura_tela / 2) - (width / 2))
    y = int((altura_tela / 2) - (height / 2))
    app.geometry(f"{width}x{height}+{x}+{y}")

def Verificar_Perfil(email):
    """Identifica o perfil do usuário pelo sufixo do e-mail (usando lógica local)."""
    email_minusculo = email.lower()
    if email_minusculo.endswith("@coordenador.educa"):
        return "Coordenador"
    elif email_minusculo.endswith("@professor.educa"):
        return "Professor"
    elif email_minusculo.endswith("@aluno.educa"):
        return "Aluno"
    return "Desconhecido"

def limpar_tela():
    """Remove todos os widgets visíveis na tela, exceto os botões persistentes."""
    for widget in app.winfo_children():
        if widget not in [btn_mode_toggle, btn_exit, version_label]:
            widget.destroy()

def toggle_appearance_mode():
    """
    Alterna o modo de aparência, atualizando o ícone (🌙/☀️) 
    e a cor da borda dos botões de controle.
    """
    current_mode = ctk.get_appearance_mode()
    
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")
        new_border_color = "black" 
        
        btn_mode_toggle.configure(
            text="☀️", text_color="#202020", fg_color="#F9F9FA", hover_color="#DDDDDD",
            border_color=new_border_color
        )
    else:
        ctk.set_appearance_mode("Dark")
        new_border_color = "white"
        btn_mode_toggle.configure(
            text="🌙", text_color="white", fg_color="#303030", hover_color="#505050",
            border_color=new_border_color
        )
        
    btn_exit.configure(
        border_color=new_border_color,
        text_color=TEMA_TEXT_COLOR 
    )

def fechar_aplicacao():
    """Função para fechar o aplicativo de forma limpa."""
    app.destroy()


# =========================================================
# REGIÃO: DECLARAÇÃO DAS TELAS DE PERFIL (EVITA NAMEERROR)
# =========================================================

# --- Funções de Tela Principal ---

def tela_coordenador():
    """Monta a tela de menu principal do perfil Coordenador."""
    limpar_tela()
    app.update_idletasks() 
    app.state('zoomed') 
    app.title("Portal Educa - Coordenador")

    ctk.CTkLabel(app, text="Bem-vindo, Coordenador!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma entidade para gerenciar:", font=fonte_subtitulo).pack(pady=5)

    # Botões de navegação para as telas de Gestão Modular
    ctk.CTkButton(app, text="Professor", font=fonte_botoes, width=300, command=tela_gestao_professor).pack(pady=10) 
    ctk.CTkButton(app, text="Aluno", font=fonte_botoes, width=300, command=tela_gestao_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Curso", font=fonte_botoes, width=300, command=tela_gestao_curso).pack(pady=10)
    ctk.CTkButton(app, text="Turma", font=fonte_botoes, width=300, command=tela_gestao_turma).pack(pady=10)
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=300, command=reiniciar_login).pack(pady=30)


def tela_professor():
    """Monta a tela de menu principal do perfil Professor."""
    limpar_tela()
    app.update_idletasks()
    app.state('zoomed')
    app.title("Portal Educa - Professor")

    ctk.CTkLabel(app, text="Bem-vindo, Professor!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma opção do menu para continuar.", font=fonte_campos).pack(pady=5)

    # Botões de navegação para funcionalidades
    ctk.CTkButton(app, text="Visualizar Turmas", font=fonte_botoes, width=250, command=tela_visualizar_turmas).pack(pady=5)
    ctk.CTkButton(app, text="Postar Atividades", font=fonte_botoes, width=250, command=tela_postar_atividades).pack(pady=5)
    ctk.CTkButton(app, text="Visualizar Atividades", font=fonte_botoes, width=250, command=tela_visualizar_atividades_prof).pack(pady=5)
    ctk.CTkButton(app, text="Lançar Notas", font=fonte_botoes, width=250, command=tela_lancar_notas).pack(pady=5)
    ctk.CTkButton(app, text="Visualizar Notas", font=fonte_botoes, width=250, command=tela_visualizar_notas_prof).pack(pady=5)
    ctk.CTkButton(app, text="Lançar Frequência", font=fonte_botoes, width=250, command=tela_lancar_frequencia).pack(pady=5)
    ctk.CTkButton(app, text="Visualizar Frequência", font=fonte_botoes, width=250, command=tela_visualizar_frequencia_prof).pack(pady=5)
    
    # CHAT COM ALUNOS
    ctk.CTkButton(app, text="Chat com Alunos", font=fonte_botoes, width=250, command=tela_chat_alunos_prof).pack(pady=5) 

    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=250, command=reiniciar_login).pack(pady=15)

# =========================================================
# REGIÃO: FUNÇÕES DO PERFIL ALUNO
# =========================================================

def tela_acessar_diario():
    """Desenha a tela de acesso ao diário eletrônico do aluno."""
    limpar_tela()
    app.title("Aluno - Diário Eletrônico")
    
    ctk.CTkLabel(app, text="Diário Eletrônico", font=fonte_titulo).pack(pady=30)
    
    # Frame para mostrar as informações do diário
    diario_frame = ctk.CTkFrame(app)
    diario_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    dados_diario = [
        "Matrícula: A20240001",
        "Nome: Aluno Teste",
        "Curso: Engenharia de Software",
        "Turma: 2024-A",
        "Status: Matriculado"
    ]
    
    for dado in dados_diario:
        ctk.CTkLabel(diario_frame, text=dado, font=fonte_campos).pack(pady=5)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", 
                 font=fonte_botoes, width=250, 
                 command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_aulas():
    """Desenha a tela para verificar as aulas do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Aulas")
    
    ctk.CTkLabel(app, text="Minhas Aulas", font=fonte_titulo).pack(pady=30)
    
    aulas_frame = ctk.CTkFrame(app)
    aulas_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    aulas = [
        "Segunda-feira: Programação I (08:00 - 10:00)",
        "Terça-feira: Banco de Dados (10:00 - 12:00)",
        "Quarta-feira: Engenharia de Software (14:00 - 16:00)",
        "Quinta-feira: Algoritmos (16:00 - 18:00)",
        "Sexta-feira: Projeto Integrador (19:00 - 21:00)"
    ]
    
    for aula in aulas:
        ctk.CTkLabel(aulas_frame, text=aula, font=fonte_campos).pack(pady=5)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", 
                 font=fonte_botoes, width=250, 
                 command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_atividades_aluno():
    """Desenha a tela para verificar as atividades do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Atividades")
    
    ctk.CTkLabel(app, text="Minhas Atividades", font=fonte_titulo).pack(pady=30)
    
    atividades_frame = ctk.CTkFrame(app)
    atividades_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    atividades = [
        "Trabalho de Programação I - Entrega: 20/11/2023",
        "Prova de Banco de Dados - Data: 25/11/2023",
        "Projeto de Engenharia de Software - Entrega: 30/11/2023",
        "Lista de Exercícios Algoritmos - Entrega: 05/12/2023"
    ]
    
    for atividade in atividades:
        ctk.CTkLabel(atividades_frame, text=atividade, font=fonte_campos).pack(pady=5)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", 
                 font=fonte_botoes, width=250, 
                 command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_desempenho():
    """Desenha a tela para verificar o desempenho do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Desempenho")
    
    ctk.CTkLabel(app, text="Meu Desempenho", font=fonte_titulo).pack(pady=30)
    
    notas_frame = ctk.CTkFrame(app)
    notas_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    notas = [
        "Programação I: 8.5",
        "Banco de Dados: 9.0",
        "Engenharia de Software: 8.0",
        "Algoritmos: 7.5",
        "Projeto Integrador: 9.5",
        "Média Geral: 8.5"
    ]
    
    for nota in notas:
        ctk.CTkLabel(notas_frame, text=nota, font=fonte_campos).pack(pady=5)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", 
                 font=fonte_botoes, width=250, 
                 command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_frequencia_aluno():
    """Desenha a tela para verificar a frequência do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Frequência")
    
    ctk.CTkLabel(app, text="Minha Frequência", font=fonte_titulo).pack(pady=30)
    
    freq_frame = ctk.CTkFrame(app)
    freq_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    frequencias = [
        "Programação I: 90%",
        "Banco de Dados: 85%",
        "Engenharia de Software: 95%",
        "Algoritmos: 88%",
        "Projeto Integrador: 92%",
        "Frequência Geral: 90%"
    ]
    
    for freq in frequencias:
        ctk.CTkLabel(freq_frame, text=freq, font=fonte_campos).pack(pady=5)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", 
                 font=fonte_botoes, width=250, 
                 command=voltar_ao_menu_principal).pack(pady=30)

def tela_aluno():
    """Monta a tela de menu principal do perfil Aluno."""
    limpar_tela()
    app.update_idletasks()
    app.state('zoomed')
    app.title("Portal Educa - Aluno")

    ctk.CTkLabel(app, text="Bem-vindo, Aluno!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma opção do menu para continuar.", font=fonte_campos).pack(pady=5)
    
    # Botões de navegação para funcionalidades
    ctk.CTkButton(app, text="Acessar Diário Eletrônico", font=fonte_botoes, width=250, command=tela_acessar_diario).pack(pady=5)
    ctk.CTkButton(app, text="Verificar Aulas", font=fonte_botoes, width=250, command=tela_verificar_aulas).pack(pady=5)
    ctk.CTkButton(app, text="Verificar Atividades", font=fonte_botoes, width=250, command=tela_verificar_atividades_aluno).pack(pady=5)
    ctk.CTkButton(app, text="Verificar Desempenho", font=fonte_botoes, width=250, command=tela_verificar_desempenho).pack(pady=5)
    ctk.CTkButton(app, text="Verificar Frequência", font=fonte_botoes, width=250, command=tela_verificar_frequencia_aluno).pack(pady=5)
    ctk.CTkButton(app, text="Chat com Professores", font=fonte_botoes, width=250, command=tela_chat_professores_aluno).pack(pady=5) 
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=250, command=reiniciar_login).pack(pady=15)


# =========================================================
# REGIÃO: FUNÇÕES DE FLUXO - LOGIN E REINICIALIZAÇÃO (CORRIGIDA)
# =========================================================

def voltar_ao_menu_principal():
    """Redireciona o usuário para o menu específico do seu perfil logado."""
    global perfil_logado
    
    if perfil_logado == "Coordenador":
        tela_coordenador()
    elif perfil_logado == "Professor":
        tela_professor()
    elif perfil_logado == "Aluno":
        tela_aluno()

def Tentar_Login(event=None):
    """Verifica a senha e, em caso de sucesso, chama a tela de menu correta (SIMULAÇÃO)."""
    global perfil_logado 
    
    app.focus() 
    
    senha_digitada = senha_entry.get()
    
    # SIMULAÇÃO DE BUSCA NO DB (Usando variáveis globais)
    credencial = CREDENCIAS.get(email_validado)
    senha_correta = credencial["senha"] if credencial else None
    
    # 1. Validação da senha
    if credencial and senha_digitada == senha_correta:
        
        # SUCESSO NO LOGIN
        perfil_logado = credencial["perfil"]
        
        # Redireciona para o menu principal do perfil
        if perfil_logado == "Coordenador":
            tela_coordenador()
        elif perfil_logado == "Professor":
            tela_professor() 
        elif perfil_logado == "Aluno":
            tela_aluno()
    else:
        # FALHA: Exibe mensagem de erro
        resultado_label.configure(
            text="SENHA INCORRETA. Tente novamente.",
            text_color="red"
        )
        senha_entry.delete(0, 'end')

def Validar_Email(event=None):
    """Valida o e-mail digitado e faz a transição para a etapa de senha (SIMULAÇÃO)."""
    global email_validado
    
    app.focus() 
    
    email_digitado = email_entry.get().lower()
    
    # SIMULAÇÃO DE BUSCA NO DB (Usando dicionário de credenciais)
    usuario_encontrado = CREDENCIAS.get(email_digitado)

    # Verifica se o usuário foi encontrado na SIMULAÇÃO
    if usuario_encontrado:
        
        # --- E-MAIL VÁLIDO: PREPARA PARA A SENHA ---
        email_validado = email_digitado 
        perfil = usuario_encontrado["perfil"] 
        
        # Oculta elementos da fase de e-mail (Bem-vindo, Entry E-mail, Botão Validar)
        label_bem_vindo.pack_forget()
        email_entry.pack_forget()
        button_email.pack_forget()
        
        # Atualiza a mensagem de instrução
        resultado_label.configure(
            text=f"Perfil encontrado: {perfil}\nDigite sua senha:", 
            text_color=TEMA_TEXT_COLOR,
            font=fonte_subtitulo
        )
        
        # Exibe os novos campos de senha
        senha_entry.pack(pady=10)
        button_login.pack(pady=10)
        
        # ATIVANDO O BIND DO ENTER PARA A SENHA
        senha_entry.bind("<Return>", Tentar_Login)
        senha_entry.focus_set() 

    else:
        # --- E-MAIL INVÁLIDO: EXIBE ERRO ---
        resultado_label.configure(
            text="E-mail inválido. Tente novamente.",
            text_color="red"
        )
        email_entry.delete(0, 'end')

def reiniciar_login():
    """Redefine o estado da aplicação e exibe a tela de login inicial."""
    global email_validado, perfil_logado
    global label_bem_vindo, resultado_label, email_entry, button_email, senha_entry, button_login
    
    # Reseta o estado
    email_validado = None
    perfil_logado = None
    
    limpar_tela() 
    app.title("Portal Educa")

    # Retorna a janela ao tamanho e posição original
    center_window(app, JANELA_WIDTH, JANELA_HEIGHT)
    app.state('normal') 

    # Recria os widgets necessários
    label_bem_vindo = ctk.CTkLabel(
        app, 
        text="Bem-vindo ao Portal Educa", 
        font=fonte_titulo
    )
    
    resultado_label = ctk.CTkLabel(
        app, 
        text="Digite seu e-mail para continuar:", 
        font=fonte_campos,
        text_color=TEMA_TEXT_COLOR
    )
    
    email_entry = ctk.CTkEntry(
        app, 
        placeholder_text="E-mail (ex: teste@coordenador.educa)", 
        font=fonte_campos, 
        justify="center", 
        width=350
    )
    
    button_email = ctk.CTkButton(
        app, 
        text="Validar E-mail", 
        font=fonte_botoes, 
        width=100,
        command=Validar_Email
    )
    
    senha_entry = ctk.CTkEntry(
        app, 
        placeholder_text="Digite sua senha", 
        font=fonte_campos, 
        justify="center", 
        show="*",
        width=300
    )
    
    button_login = ctk.CTkButton(
        app, 
        text="Login", 
        font=fonte_botoes, 
        width=100,
        command=Tentar_Login
    )

    # Monta os widgets iniciais
    label_bem_vindo.pack(pady=20)
    resultado_label.pack(pady=10)
    email_entry.pack(pady=10)
    button_email.pack(pady=10)
    
    # ATIVANDO O BIND DO ENTER PARA O E-MAIL
    email_entry.bind("<Return>", Validar_Email)
    email_entry.focus_set() 

    # 3. Limpa o Entry de senha (se existir)
    try:
        if senha_entry and senha_entry.winfo_exists():
            senha_entry.delete(0, 'end')
    except:
        pass

# =========================================================
# REGIÃO: FUNÇÕES DE SIMULAÇÃO (COMPLETAS)
# =========================================================

def simular_cadastro_sucesso(nome, email, status_label):
    """Simula o sucesso do cadastro e limpa os campos."""
    status_label.configure(text=f"'{nome}' cadastrado (Simulação OK).", text_color="green")
    
    global professor_nome_entry, professor_email_entry, professor_senha_entry
    if professor_nome_entry: professor_nome_entry.delete(0, 'end')
    if professor_email_entry: professor_email_entry.delete(0, 'end')
    if professor_senha_entry: professor_senha_entry.delete(0, 'end')
    
def simular_exclusao_sucesso(item, tipo, entry, status_label):
    """Simula o sucesso da exclusão e limpa o campo."""
    status_label.configure(text=f"{tipo} '{item}' excluído (Simulação OK).", text_color="green")
    entry.delete(0, 'end')

# --- CADASTRO SIMULADO ---

def salvar_cadastro_professor():
    """
    Lê os dados e simula o cadastro de professor.
    """
    global professor_nome_entry, professor_email_entry, professor_senha_entry, professor_status_label
    
    nome = professor_nome_entry.get().strip()
    email = professor_email_entry.get().strip().lower()
    
    if not nome or not email or not professor_senha_entry.get().strip():
        professor_status_label.configure(text="Erro: Preencha todos os campos.", text_color="red")
        return
    
    if not email.endswith("@professor.educa"):
        professor_status_label.configure(text="Erro: E-mail deve terminar com @professor.educa", text_color="red")
        return

    if email == login_professor:
        professor_status_label.configure(text="Erro: Este e-mail já está em uso. (Simulação Duplicidade)", text_color="red")
        return

    simular_cadastro_sucesso(nome, email, professor_status_label)


# --- EXCLUSÃO SIMULADA ---

def acao_excluir_professor():
    """Ação de exclusão do professor (SIMULAÇÃO)."""
    global professor_email_excluir_entry, professor_exclusao_status_label
    
    email = professor_email_excluir_entry.get().strip().lower()
    if not email:
        professor_exclusao_status_label.configure(text="Erro: Digite o e-mail para excluir.", text_color="red")
        return
    
    if email == login_professor:
        professor_exclusao_status_label.configure(text="Erro: Professor com vínculos. (Simulação Integridade)", text_color="orange")
        return

    simular_exclusao_sucesso(email, "Professor", professor_email_excluir_entry, professor_exclusao_status_label)

def acao_excluir_aluno():
    """Ação de exclusão do aluno (SIMULAÇÃO)."""
    global aluno_email_excluir_entry, aluno_exclusao_status_label
    
    email = aluno_email_excluir_entry.get().strip().lower()
    if not email:
        aluno_exclusao_status_label.configure(text="Erro: Digite o e-mail para excluir.", text_color="red")
        return

    simular_exclusao_sucesso(email, "Aluno", aluno_email_excluir_entry, aluno_exclusao_status_label)

def acao_excluir_curso():
    """Ação de exclusão do curso (SIMULAÇÃO)."""
    global curso_nome_excluir_entry, curso_exclusao_status_label
    
    nome = curso_nome_excluir_entry.get().strip()
    if not nome:
        curso_exclusao_status_label.configure(text="Erro: Digite o nome do curso para excluir.", text_color="red")
        return
    
    simular_exclusao_sucesso(nome, "Curso", curso_nome_excluir_entry, curso_exclusao_status_label)

def acao_excluir_turma():
    """Ação de exclusão da turma (SIMULAÇÃO)."""
    global turma_nome_excluir_entry, turma_exclusao_status_label
    
    nome = turma_nome_excluir_entry.get().strip()
    if not nome:
        turma_exclusao_status_label.configure(text="Erro: Digite o nome da turma para excluir.", text_color="red")
        return
    
    simular_exclusao_sucesso(nome, "Turma", turma_nome_excluir_entry, turma_exclusao_status_label)

# --- LISTAR/VISUALIZAR SIMULADO ---

def tela_listar_professores():
    """SIMULAÇÃO: Exibe a lista de professores."""
    limpar_tela()
    app.title("Coordenador - Listar Professores")
    ctk.CTkLabel(app, text="LISTA DE PROFESSORES (Simulação)", font=fonte_titulo).pack(pady=30)
    
    professores_lista = [
        "ID: 2 | Nome: Prof. Ana Silva | Email: teste@professor.educa",
        "ID: 10 | Nome: Prof. Carlos | Email: carlos@professor.educa",
        "ID: 15 | Nome: Prof. Mariana | Email: mariana@professor.educa",
    ]
    
    ctk.CTkLabel(app, text="\n".join(professores_lista), font=fonte_campos, justify="left").pack(pady=10, padx=20)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Professor", font=fonte_botoes, width=250, command=tela_gestao_professor).pack(pady=20)


def tela_listar_alunos():
    """SIMULAÇÃO: Exibe a lista de alunos."""
    limpar_tela()
    app.title("Coordenador - Listar Alunos")
    ctk.CTkLabel(app, text="LISTA DE ALUNOS (Simulação)", font=fonte_titulo).pack(pady=30)
    
    alunos_lista = [
        "Mat: A20240001 | Nome: Aluno Bruno | Email: teste@aluno.educa",
        "Mat: A20240002 | Nome: Aluna Luiza | Turma: 2024-A",
        "Mat: A20240003 | Nome: Aluno Pedro | Turma: 2024-B",
    ]
    
    ctk.CTkLabel(app, text="\n".join(alunos_lista), font=fonte_campos, justify="left").pack(pady=10, padx=20)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Aluno", font=fonte_botoes, width=250, command=tela_gestao_aluno).pack(pady=20)

def tela_listar_cursos():
    """SIMULAÇÃO: Exibe a lista de cursos."""
    limpar_tela()
    app.title("Coordenador - Listar Cursos")
    ctk.CTkLabel(app, text="LISTA DE CURSOS (Simulação)", font=fonte_titulo).pack(pady=30)
    
    cursos_lista = ["Engenharia de Software", "Administração", "Ciências Contábeis"]
    
    ctk.CTkLabel(app, text="\n".join([f"Curso: {c}" for c in cursos_lista]), font=fonte_campos, justify="left").pack(pady=10, padx=20)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Curso", font=fonte_botoes, width=250, command=tela_gestao_curso).pack(pady=20)

def tela_listar_turmas():
    """SIMULAÇÃO: Exibe a lista de turmas."""
    limpar_tela()
    app.title("Coordenador - Listar Turmas")
    ctk.CTkLabel(app, text="LISTA DE TURMAS (Simulação)", font=fonte_titulo).pack(pady=30)
    
    turmas_lista = [
        "Turma: 2024-A | Curso: Engenharia de Software | Alunos: 30",
        "Turma: 2024-B | Curso: Administração | Alunos: 25",
    ]
    
    ctk.CTkLabel(app, text="\n".join(turmas_lista), font=fonte_campos, justify="left").pack(pady=10, padx=20)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Turma", font=fonte_botoes, width=250, command=tela_gestao_turma).pack(pady=20)


# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - TELAS DE GESTÃO MODULAR
# =========================================================

def tela_gestao_professor():
    """Menu modular para gestão de Professores: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Professor")

    ctk.CTkLabel(app, text="GESTÃO DE PROFESSOR", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="1. Cadastrar Professor", font=fonte_botoes, width=300, command=tela_cadastrar_professor).pack(pady=10)
    ctk.CTkButton(app, text="2. Apagar Professor", font=fonte_botoes, width=300, command=tela_excluir_professor).pack(pady=10)
    ctk.CTkButton(app, text="3. Listar Professores", font=fonte_botoes, width=300, command=tela_listar_professores).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_coordenador).pack(pady=30)

def tela_gestao_aluno():
    """Menu modular para gestão de Alunos: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Aluno")

    ctk.CTkLabel(app, text="GESTÃO DE ALUNO", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="1. Cadastrar Aluno", font=fonte_botoes, width=300, command=tela_cadastrar_aluno).pack(pady=10)
    ctk.CTkButton(app, text="2. Apagar Aluno", font=fonte_botoes, width=300, command=tela_excluir_aluno).pack(pady=10)
    ctk.CTkButton(app, text="3. Listar Alunos", font=fonte_botoes, width=300, command=tela_listar_alunos).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_coordenador).pack(pady=30)

def tela_gestao_curso():
    """Menu modular para gestão de Cursos: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Curso")

    ctk.CTkLabel(app, text="GESTÃO DE CURSO", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="1. Cadastrar Curso", font=fonte_botoes, width=300, command=tela_cadastrar_curso).pack(pady=10)
    ctk.CTkButton(app, text="2. Apagar Curso", font=fonte_botoes, width=300, command=tela_excluir_curso).pack(pady=10)
    ctk.CTkButton(app, text="3. Listar Cursos", font=fonte_botoes, width=300, command=tela_listar_cursos).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_coordenador).pack(pady=30)

def tela_gestao_turma():
    """Menu modular para gestão de Turmas: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Turma")

    ctk.CTkLabel(app, text="GESTÃO DE TURMA", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="1. Cadastrar Turma", font=fonte_botoes, width=300, command=tela_cadastrar_turma).pack(pady=10)
    ctk.CTkButton(app, text="2. Apagar Turma", font=fonte_botoes, width=300, command=tela_excluir_turma).pack(pady=10)
    ctk.CTkButton(app, text="3. Listar Turmas", font=fonte_botoes, width=300, command=tela_listar_turmas).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_coordenador).pack(pady=30)


# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - MÓDULO COORDENADOR (TELAS)
# =========================================================

def tela_coordenador():
    """Monta a tela de menu principal do perfil Coordenador."""
    limpar_tela()
    app.update_idletasks() 
    app.state('zoomed') 
    app.title("Portal Educa - Coordenador")

    ctk.CTkLabel(app, text="Bem-vindo, Coordenador!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma entidade para gerenciar:", font=fonte_subtitulo).pack(pady=5)

    # Botões de navegação para as telas de Gestão Modular
    ctk.CTkButton(app, text="Professor", font=fonte_botoes, width=300, command=tela_gestao_professor).pack(pady=10) 
    ctk.CTkButton(app, text="Aluno", font=fonte_botoes, width=300, command=tela_gestao_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Curso", font=fonte_botoes, width=300, command=tela_gestao_curso).pack(pady=10)
    ctk.CTkButton(app, text="Turma", font=fonte_botoes, width=300, command=tela_gestao_turma).pack(pady=10)
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=300, command=reiniciar_login).pack(pady=30)


# --- TELAS DE CADASTRO (Acessadas pelos menus de gestão) ---

def tela_cadastrar_professor():
    """Desenha a tela para cadastro de Professor."""
    global professor_nome_entry, professor_email_entry, professor_senha_entry, professor_status_label
    
    limpar_tela()
    app.title("Coordenador - Cadastrar Professor")

    ctk.CTkLabel(app, text="Cadastrar Novo Professor", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    professor_nome_entry = ctk.CTkEntry(app, placeholder_text="Nome Completo", font=fonte_campos, width=350)
    professor_nome_entry.pack(pady=5)
    
    professor_email_entry = ctk.CTkEntry(app, placeholder_text="E-mail (@professor.educa)", font=fonte_campos, width=350)
    professor_email_entry.pack(pady=5)
    
    professor_senha_entry = ctk.CTkEntry(app, placeholder_text="Senha Inicial", font=fonte_campos, width=350, show="*")
    professor_senha_entry.pack(pady=5)

    # Rótulo para feedback de sucesso ou erro
    professor_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    professor_status_label.pack(pady=5)

    ctk.CTkButton(app, text="Salvar Cadastro", font=fonte_botoes, width=250, command=salvar_cadastro_professor).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Professor", font=fonte_botoes, width=250, command=tela_gestao_professor).pack(pady=20)


def tela_cadastrar_aluno():
    """Desenha a tela para cadastro de Aluno."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Aluno")

    ctk.CTkLabel(app, text="Cadastrar Novo Aluno", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome Completo", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="E-mail (@aluno.educa)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Senha Inicial", font=fonte_campos, width=350, show="*").pack(pady=5)

    ctk.CTkButton(app, text="Salvar Cadastro (Simulação)", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar à Gestão de Aluno", font=fonte_botoes, width=250, command=tela_gestao_aluno).pack(pady=20)


def tela_cadastrar_curso():
    """Desenha a tela para cadastro de Curso."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Curso")

    ctk.CTkLabel(app, text="Cadastrar Novo Curso", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome do Curso", font=fonte_campos, width=350).pack(pady=5)
    # Textbox para a descrição
    ctk.CTkTextbox(app, width=350, height=100, font=fonte_campos).insert("0.0", "Descrição do Curso")
    
    ctk.CTkButton(app, text="Salvar Cadastro (Simulação)", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar à Gestão de Curso", font=fonte_botoes, width=250, command=tela_gestao_curso).pack(pady=20)


def tela_cadastrar_turma():
    """Desenha a tela para cadastro de Turma."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Turma")

    # SIMULAÇÃO: Lista de cursos fixa, já que o DB foi removido
    lista_cursos = ["Engenharia de Software", "Administração", "Ciências Contábeis"]
    
    ctk.CTkLabel(app, text="Cadastrar Nova Turma", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome da Turma (Ex: 2024-A)", font=fonte_campos, width=350).pack(pady=5)
    
    ctk.CTkLabel(app, text="Selecione o Curso:", font=fonte_campos).pack(pady=(15, 0))
    ctk.CTkComboBox(
        app, 
        values=lista_cursos, 
        font=fonte_campos, 
        width=350,
        state="readonly"
    ).pack(pady=5)

    ctk.CTkButton(app, text="Salvar Cadastro (Simulação)", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar à Gestão de Turma", font=fonte_botoes, width=250, command=tela_gestao_turma).pack(pady=20)

def tela_matricular_aluno_turma():
    """Permite ao Coordenador matricular um aluno em uma turma."""
    limpar_tela()
    app.title("Coordenador - Matricular Aluno")
    ctk.CTkLabel(app, text="Matricular Aluno em Turma", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="E-mail do Aluno (@aluno.educa)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Nome da Turma", font=fonte_campos, width=350).pack(pady=5)
    
    ctk.CTkButton(app, text="Confirmar Matrícula (Simulação)", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=tela_coordenador).pack(pady=20)


# --- TELAS DE EXCLUSÃO ---

def tela_excluir_professor():
    """Desenha a tela para exclusão de Professor."""
    global professor_email_excluir_entry, professor_exclusao_status_label
    limpar_tela()
    app.title("Coordenador - Apagar Professor")

    ctk.CTkLabel(app, text="Apagar Professor", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Atenção: A exclusão é permanente.", font=fonte_campos).pack(pady=5)

    # Input de Dados
    professor_email_excluir_entry = ctk.CTkEntry(app, placeholder_text="E-mail do Professor a Apagar", font=fonte_campos, width=350)
    professor_email_excluir_entry.pack(pady=10)

    # Rótulo de Status
    professor_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    professor_exclusao_status_label.pack(pady=5)

    ctk.CTkButton(app, text="APAGAR PERMANENTEMENTE", font=fonte_botoes, width=250, fg_color="red", hover_color="#B00000", command=acao_excluir_professor).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Professor", font=fonte_botoes, width=250, command=tela_gestao_professor).pack(pady=20)


def tela_excluir_aluno():
    """Desenha a tela para exclusão de Aluno."""
    global aluno_email_excluir_entry, aluno_exclusao_status_label
    limpar_tela()
    app.title("Coordenador - Apagar Aluno")

    ctk.CTkLabel(app, text="Apagar Aluno", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Atenção: A exclusão é permanente.", font=fonte_campos).pack(pady=5)

    # Input de Dados
    aluno_email_excluir_entry = ctk.CTkEntry(app, placeholder_text="E-mail do Aluno a Apagar", font=fonte_campos, width=350)
    aluno_email_excluir_entry.pack(pady=10)

    # Rótulo de Status
    aluno_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    aluno_exclusao_status_label.pack(pady=5)

    ctk.CTkButton(app, text="APAGAR PERMANENTEMENTE", font=fonte_botoes, width=250, fg_color="red", hover_color="#B00000", command=acao_excluir_aluno).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Aluno", font=fonte_botoes, width=250, command=tela_gestao_aluno).pack(pady=20)


def tela_excluir_curso():
    """Desenha a tela para exclusão de Curso."""
    global curso_nome_excluir_entry, curso_exclusao_status_label
    limpar_tela()
    app.title("Coordenador - Apagar Curso")

    ctk.CTkLabel(app, text="Apagar Curso", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Atenção: Cursos com turmas ativas não podem ser apagados.", font=fonte_campos).pack(pady=5)

    # Input de Dados
    curso_nome_excluir_entry = ctk.CTkEntry(app, placeholder_text="Nome do Curso a Apagar", font=fonte_campos, width=350)
    curso_nome_excluir_entry.pack(pady=10)

    # Rótulo de Status
    curso_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    curso_exclusao_status_label.pack(pady=5)

    ctk.CTkButton(app, text="APAGAR PERMANENTEMENTE", font=fonte_botoes, width=250, fg_color="red", hover_color="#B00000", command=acao_excluir_curso).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Curso", font=fonte_botoes, width=250, command=tela_gestao_curso).pack(pady=20)


def tela_excluir_turma():
    """Desenha a tela para exclusão de Turma."""
    global turma_nome_excluir_entry, turma_exclusao_status_label
    limpar_tela()
    app.title("Coordenador - Apagar Turma")

    ctk.CTkLabel(app, text="Apagar Turma", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Atenção: Turmas com alunos matriculados não podem ser apagadas.", font=fonte_campos).pack(pady=5)

    # Input de Dados
    turma_nome_excluir_entry = ctk.CTkEntry(app, placeholder_text="Nome da Turma a Apagar", font=fonte_campos, width=350)
    turma_nome_excluir_entry.pack(pady=10)

    # Rótulo de Status
    turma_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    turma_exclusao_status_label.pack(pady=5)

    ctk.CTkButton(app, text="APAGAR PERMANENTEMENTE", font=fonte_botoes, width=250, fg_color="red", hover_color="#B00000", command=acao_excluir_turma).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Turma", font=fonte_botoes, width=250, command=tela_gestao_turma).pack(pady=20)


# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - MÓDULO PROFESSOR
# =========================================================

def tela_visualizar_turmas():
    """Desenha a tela de visualização de Turmas atribuídas."""
    limpar_tela()
    app.title("Professor - Visualizar Turmas")
    ctk.CTkLabel(app, text="Visualizar Turmas Atribuídas", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a lista de turmas.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_postar_atividades():
    """Desenha a tela para postagem de Atividades."""
    limpar_tela()
    app.title("Professor - Postar Atividades")
    ctk.CTkLabel(app, text="Postar Nova Atividade", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Título da Atividade", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkTextbox(app, width=350, height=100, font=fonte_campos).insert("0.0", "Descrição da Atividade")
    ctk.CTkButton(app, text="Postar (Simulação)", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_lancar_notas():
    """Desenha a tela para lançamento de Notas."""
    limpar_tela()
    app.title("Professor - Lançar Notas")
    ctk.CTkLabel(app, text="Lançar Notas", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Nome do Aluno", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Nota (0-10)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkButton(app, text="Lançar (Simulação)", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_lancar_frequencia():
    """Desenha a tela para lançamento de Frequência."""
    limpar_tela()
    app.title("Professor - Lançar Frequência")
    ctk.CTkLabel(app, text="Lançar Frequência", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Nome do Aluno", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Frequência (P/F)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkButton(app, text="Lançar (Simulação)", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_visualizar_atividades_prof():
    """Desenha a tela de visualização de Atividades postadas."""
    limpar_tela()
    app.title("Professor - Visualizar Atividades")
    ctk.CTkLabel(app, text="Atividades Postadas", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a lista das suas atividades postadas.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_visualizar_notas_prof():
    """Desenha a tela de visualização de Notas lançadas."""
    limpar_tela()
    app.title("Professor - Visualizar Notas")
    ctk.CTkLabel(app, text="Notas Lançadas", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a visualização das notas por turma.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_visualizar_frequencia_prof():
    """Desenha a tela de visualização de Frequência lançada."""
    limpar_tela()
    app.title("Professor - Visualizar Frequência")
    ctk.CTkLabel(app, text="Frequência Lançada", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a visualização da frequência por turma.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def encerrar_chat_e_voltar():
    """Salva o histórico e volta ao menu principal."""
    save_chat_history(MENSAGENS_CHAT)
    voltar_ao_menu_principal()

def tela_chat_alunos_prof():
    """Desenha a tela de chat para o Professor interagir com os Alunos."""
    global MENSAGENS_CHAT
    
    # Garantir que MENSAGENS_CHAT está carregado
    if not MENSAGENS_CHAT:
        MENSAGENS_CHAT = load_chat_history()
    
    limpar_tela()
    app.title("Professor - Chat com Alunos")
    ctk.CTkLabel(app, text="Chat Global", font=fonte_titulo).pack(pady=10)

    # Textbox para histórico de mensagens (readonly)
    chat_history_box = ctk.CTkTextbox(app, width=500, height=450, font=fonte_campos, state="disabled")
    chat_history_box.pack(pady=10, padx=20)
    
    def atualizar_historico():
        """Atualiza a CTkTextbox com todas as mensagens globais."""
        chat_history_box.configure(state="normal")
        chat_history_box.delete("1.0", "end")
        
        for msg in MENSAGENS_CHAT:
            chat_history_box.insert("end", f"[{msg['perfil']}]: {msg['texto']}\n")
            
        chat_history_box.configure(state="disabled")
        chat_history_box.yview_moveto(1.0)

    def enviar_mensagem(event=None):
        """Lê a mensagem, adiciona à lista global e atualiza a tela."""
        mensagem = chat_input_entry.get().strip()
        if mensagem:
            MENSAGENS_CHAT.append({"perfil": perfil_logado, "texto": mensagem})
            save_chat_history(MENSAGENS_CHAT)  # Salva após cada mensagem
            chat_input_entry.delete(0, 'end')
            atualizar_historico()
            
    input_frame = ctk.CTkFrame(app, fg_color="transparent")
    input_frame.pack(pady=10, padx=20, fill="x")

    chat_input_entry = ctk.CTkEntry(input_frame, placeholder_text="Digite sua mensagem...", font=fonte_campos)
    chat_input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    chat_input_entry.focus_set() 

    ctk.CTkButton(input_frame, text="Enviar", font=fonte_botoes, width=80, command=enviar_mensagem).pack(side="left", padx=(0, 10))
    
    ctk.CTkButton(
        input_frame, 
        text="Voltar ao Menu", 
        font=fonte_botoes, 
        width=150, 
        command=encerrar_chat_e_voltar, 
        fg_color="#4CAF50", 
        hover_color="#388E3C"
    ).pack(side="left", padx=(0, 10))

    chat_input_entry.bind("<Return>", enviar_mensagem)
    
    # Carrega o histórico ao abrir o chat
    MENSAGENS_CHAT = load_chat_history()
    atualizar_historico()

# A função tela_chat_professores_aluno deve ser atualizada de forma similar
def tela_chat_professores_aluno():
    """Desenha a tela de chat para o Aluno interagir com os Professores."""
    global MENSAGENS_CHAT
    
    # Garantir que MENSAGENS_CHAT está carregado
    if not MENSAGENS_CHAT:
        MENSAGENS_CHAT = load_chat_history()
    
    limpar_tela()
    app.title("Aluno - Chat com Professores")
    ctk.CTkLabel(app, text="Chat Global", font=fonte_titulo).pack(pady=10)

    # Textbox para histórico de mensagens (readonly)
    chat_history_box = ctk.CTkTextbox(app, width=500, height=450, font=fonte_campos, state="disabled")
    chat_history_box.pack(pady=10, padx=20)
    
    def atualizar_historico():
        """Atualiza a CTkTextbox com todas as mensagens globais."""
        chat_history_box.configure(state="normal")
        chat_history_box.delete("1.0", "end")
        
        for msg in MENSAGENS_CHAT:
            chat_history_box.insert("end", f"[{msg['perfil']}]: {msg['texto']}\n")
            
        chat_history_box.configure(state="disabled")
        chat_history_box.yview_moveto(1.0)

    def enviar_mensagem(event=None):
        """Lê a mensagem, adiciona à lista global e atualiza a tela."""
        mensagem = chat_input_entry.get().strip()
        if mensagem:
            MENSAGENS_CHAT.append({"perfil": perfil_logado, "texto": mensagem})
            save_chat_history(MENSAGENS_CHAT)  # Salva após cada mensagem
            chat_input_entry.delete(0, 'end')
            atualizar_historico()
            
    input_frame = ctk.CTkFrame(app, fg_color="transparent")
    input_frame.pack(pady=10, padx=20, fill="x")

    chat_input_entry = ctk.CTkEntry(input_frame, placeholder_text="Digite sua mensagem...", font=fonte_campos)
    chat_input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    chat_input_entry.focus_set() 

    ctk.CTkButton(input_frame, text="Enviar", font=fonte_botoes, width=80, command=enviar_mensagem).pack(side="left", padx=(0, 10))
    
    ctk.CTkButton(
        input_frame, 
        text="Voltar ao Menu", 
        font=fonte_botoes, 
        width=150, 
        command=encerrar_chat_e_voltar, 
        fg_color="#4CAF50", 
        hover_color="#388E3C"
    ).pack(side="left", padx=(0, 10))

    chat_input_entry.bind("<Return>", enviar_mensagem)
    
    atualizar_historico()


def limpar_historico_chat():
    """Limpa todo o histórico do chat."""
    global MENSAGENS_CHAT
    MENSAGENS_CHAT = [{"perfil": "Sistema", "texto": "Início da Conversa. Histórico apagado."}]
    save_chat_history(MENSAGENS_CHAT)


# =========================================================
# REGIÃO: CONFIGURAÇÕES E INICIALIZAÇÃO DA JANELA PRINCIPAL
# =========================================================

# Configurações iniciais do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Inicialização e Configuração da Janela Principal (root)
app = ctk.CTk()
app.title("Portal Educa")
center_window(app, JANELA_WIDTH, JANELA_HEIGHT)
app.resizable(False, False)

# Carregamento do Ícone (mantido o tratamento de erro)
try:
    app.iconbitmap("C:\\Users\\willi\\OneDrive\\Documentos\\VS Code\\Portal Educa\\images\\icon.ico")
except Exception as e:
    print(f"Aviso: Não foi possível carregar o ícone. Verifique o caminho. {e}") 

# Configuração de Fontes (Definidas após a criação do 'app')
fonte_titulo = ctk.CTkFont(family="Comic Sans MS", size=20, weight="bold")
fonte_subtitulo = ctk.CTkFont(family="Comic Sans MS", size=16, weight="bold")
fonte_campos = ctk.CTkFont(family="Comic Sans MS", size=12)
fonte_botoes = ctk.CTkFont(family="Comic Sans MS", size=12, weight="bold")


# =========================================================
# REGIÃO: CRIAÇÃO DE WIDGETS
# =========================================================
# Estes widgets são criados globalmente para serem acessados em qualquer função.

# Criação de Widgets: Fase 1 (E-mail - Visíveis na inicialização)

# Rótulo de Boas-vindas 
label_bem_vindo = ctk.CTkLabel(
    app, 
    text="Bem-vindo ao Portal Educa", 
    font=fonte_titulo
)

# Rótulo de Status (Usado para instruções e mensagens de erro/sucesso)
resultado_label = ctk.CTkLabel(
    app, 
    text="", 
    font=fonte_campos
)

# Entrada de E-mail
email_entry = ctk.CTkEntry(
    app, 
    placeholder_text="E-mail (ex: teste@coordenador.educa)", 
    font=fonte_campos, 
    justify="center", 
    width=350
)

# Botão de Validação do E-mail
button_email = ctk.CTkButton(
    app, 
    text="Validar E-mail", 
    font=fonte_botoes, 
    width=100,
    command=Validar_Email
)

# Criação de Widgets: Fase 2 (Senha - Inicialmente Ocultos)

# Entrada de Senha
senha_entry = ctk.CTkEntry(
    app, 
    placeholder_text="Digite sua senha", 
    font=fonte_campos, 
    justify="center", 
    show="*", # Caracteres ocultos
    width=300
)

# Botão de Login
button_login = ctk.CTkButton(
    app, 
    text="Login", 
    font=fonte_botoes, 
    width=100,
    command=Tentar_Login
)

# CONSTANTES VISUAIS PARA BOTÕES PERSISTENTES
BTN_SIZE = 40
BTN_BORDER_WIDTH = 2
# Cor da Borda: Branco no Dark, Preto no Light
BTN_BORDER_COLOR_DARK = "white"
BTN_BORDER_COLOR_LIGHT = "black"


# Botão de Tema (Dark/Light) - Persistente
btn_mode_toggle = ctk.CTkButton(
    app,
    text="🌙", 
    width=BTN_SIZE,
    height=BTN_SIZE,
    corner_radius=BTN_SIZE, 
    font=("Arial", 22, "bold"), 
    fg_color="#303030", 
    hover_color="#505050", 
    text_color="white",
    border_width=BTN_BORDER_WIDTH, 
    border_color=BTN_BORDER_COLOR_DARK, 
    command=toggle_appearance_mode
)
btn_mode_toggle.place(relx=1.0, rely=1.0, x=-15, y=-15, anchor="se") 

# Botão de Sair/Fechar o Aplicativo - Persistente 
btn_exit = ctk.CTkButton(
    app,
    text="X", 
    width=BTN_SIZE,
    height=BTN_SIZE,
    corner_radius=BTN_SIZE, 
    font=("Arial", 18, "bold"),
    fg_color="red", 
    hover_color="#B00000",
    text_color=TEMA_TEXT_COLOR, 
    border_width=BTN_BORDER_WIDTH, 
    border_color=BTN_BORDER_COLOR_DARK, 
    command=fechar_aplicacao
)
btn_exit.place(relx=0.0, rely=1.0, x=15, y=-15, anchor="sw") 

# Label de Versão - Persistente
version_label = ctk.CTkLabel(
    app,
    text=f"Portal Educa {APP_VERSION}",
    font=("Arial", 10),
    text_color="gray"
)
version_label.place(relx=0.5, rely=1.0, y=-10, anchor="s")


# =========================================================
# REGIÃO: INICIALIZAÇÃO DO FLUXO
# =========================================================

# 1. Inicia a aplicação na tela de login
reiniciar_login()
app.mainloop()# Após as variáveis globais
try:
    MENSAGENS_CHAT = load_chat_history()
except Exception as e:
    print(f"Erro ao carregar histórico do chat: {e}")
    MENSAGENS_CHAT = []