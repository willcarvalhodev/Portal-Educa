import customtkinter as ctk

# =========================================================
# REGIÃO: VARIÁVEIS DE AUTENTICAÇÃO E ESTADO GLOBAL
# =========================================================

# Credenciais Fictícias (para testes iniciais)
login_coordenador = "teste@coordenador.educa"
senha_coordenador = "123456"

login_professor = "teste@professor.educa"
senha_professor = "123456"

login_aluno = "teste@aluno.educa"
senha_aluno = "123456"

# Variáveis de Estado (usadas para controlar o fluxo de login e navegação)
email_validado = None
perfil_logado = None

# Dimensões Padrão da Janela
JANELA_WIDTH = 400
JANELA_HEIGHT = 300

# Tupla de cores para garantir que o texto seja visível em ambos os modos
# (Cor Modo Claro, Cor Modo Escuro)
TEMA_TEXT_COLOR = ("black", "white") 

# =========================================================
# REGIÃO: FUNÇÕES DE UTILIDADE (LAYOUT E LÓGICA CENTRAL)
# =========================================================

def center_window(app, width, height):
    """Calcula a posição e centraliza a janela principal na tela."""
    app.update_idletasks()
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()

    # Cálculo da posição inicial (canto superior esquerdo)
    x = int((largura_tela / 2) - (width / 2))
    y = int((altura_tela / 2) - (height / 2))

    app.geometry(f"{width}x{height}+{x}+{y}")

def Verificar_Perfil(email):
    """Identifica o perfil do usuário pelo sufixo do e-mail."""
    email_minusculo = email.lower()
    if email_minusculo.endswith("@coordenador.educa"):
        return "Coordenador"
    elif email_minusculo.endswith("@professor.educa"):
        return "Professor"
    elif email_minusculo.endswith("@aluno.educa"):
        return "Aluno"
    return "Desconhecido"

def limpar_tela():
    """Remove todos os widgets visíveis na tela, exceto o botão de tema (persistente)."""
    for widget in app.winfo_children():
        # Verifica se o widget não é o botão de tema antes de removê-lo
        if widget is not btn_mode_toggle:
            widget.pack_forget()
        
def toggle_appearance_mode():
    """Alterna o modo de aparência entre Dark e Light, atualizando o ícone do botão."""
    current_mode = ctk.get_appearance_mode()
    
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")
        # Configuração visual para tema Claro
        btn_mode_toggle.configure(text="☀️", text_color="#202020", fg_color="#F9F9FA", hover_color="#EEEEEE") 
    else:
        ctk.set_appearance_mode("Dark")
        # Configuração visual para tema Escuro
        btn_mode_toggle.configure(text="🌙", text_color="white", fg_color="#303030", hover_color="#404040")

def voltar_ao_menu_principal():
    """Redireciona o usuário para o menu específico do seu perfil logado."""
    global perfil_logado
    
    if perfil_logado == "Coordenador":
        tela_coordenador()
    elif perfil_logado == "Professor":
        tela_professor()
    elif perfil_logado == "Aluno":
        tela_aluno()

# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - MÓDULO COORDENADOR (CADASTROS)
# =========================================================

def tela_cadastrar_professor():
    """Desenha a tela para cadastro de Professor."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Professor")

    ctk.CTkLabel(app, text="Cadastrar Novo Professor", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome Completo", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="E-mail (@professor.educa)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Senha Inicial", font=fonte_campos, width=350, show="*").pack(pady=5)

    ctk.CTkButton(app, text="Salvar Cadastro", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=20)


def tela_cadastrar_aluno():
    """Desenha a tela para cadastro de Aluno."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Aluno")

    ctk.CTkLabel(app, text="Cadastrar Novo Aluno", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome Completo", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="E-mail (@aluno.educa)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Senha Inicial", font=fonte_campos, width=350, show="*").pack(pady=5)

    ctk.CTkButton(app, text="Salvar Cadastro", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=20)


def tela_cadastrar_curso():
    """Desenha a tela para cadastro de Curso."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Curso")

    ctk.CTkLabel(app, text="Cadastrar Novo Curso", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome do Curso", font=fonte_campos, width=350).pack(pady=5)
    # Textbox para a descrição
    ctk.CTkTextbox(app, width=350, height=100, font=fonte_campos).insert("0.0", "Descrição do Curso")
    
    ctk.CTkButton(app, text="Salvar Cadastro", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=20)


def tela_cadastrar_turma():
    """Desenha a tela para cadastro de Turma."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Turma")

    ctk.CTkLabel(app, text="Cadastrar Nova Turma", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome da Turma (Ex: 2024-A)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Curso (Referência)", font=fonte_campos, width=350).pack(pady=5)

    ctk.CTkButton(app, text="Salvar Cadastro", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=20)

# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - MÓDULO PROFESSOR
# =========================================================

def tela_adicionar_aluno_turma():
    """Desenha a tela para adicionar Aluno à Turma."""
    limpar_tela()
    app.title("Professor - Adicionar Aluno")
    ctk.CTkLabel(app, text="Adicionar Aluno à Turma", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Nome do Aluno", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Nome da Turma", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkButton(app, text="Adicionar", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

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
    ctk.CTkButton(app, text="Postar", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_lancar_notas():
    """Desenha a tela para lançamento de Notas."""
    limpar_tela()
    app.title("Professor - Lançar Notas")
    ctk.CTkLabel(app, text="Lançar Notas", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Nome do Aluno", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Nota (0-10)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkButton(app, text="Lançar", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_lancar_frequencia():
    """Desenha a tela para lançamento de Frequência."""
    limpar_tela()
    app.title("Professor - Lançar Frequência")
    ctk.CTkLabel(app, text="Lançar Frequência", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Nome do Aluno", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Frequência (P/F)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkButton(app, text="Lançar", font=fonte_botoes, width=250).pack(pady=15)
    
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
    
def tela_chat_alunos_prof():
    """Desenha a tela de chat para o Professor interagir com os Alunos."""
    limpar_tela()
    app.title("Professor - Chat com Alunos")
    ctk.CTkLabel(app, text="Chat com Alunos", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a interface de chat para comunicação com os alunos.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)


# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - MÓDULO ALUNO
# =========================================================

def tela_acessar_diario():
    """Desenha a tela para acesso ao Diário Eletrônico."""
    limpar_tela()
    app.title("Aluno - Diário Eletrônico")
    ctk.CTkLabel(app, text="Diário Eletrônico", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Visualização de comunicados, eventos e tarefas.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_aulas():
    """Desenha a tela de verificação de Horário de Aulas."""
    limpar_tela()
    app.title("Aluno - Horário de Aulas")
    ctk.CTkLabel(app, text="Horário de Aulas", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria o calendário semanal de aulas.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_atividades_aluno():
    """Desenha a tela de verificação de Atividades."""
    limpar_tela()
    app.title("Aluno - Minhas Atividades")
    ctk.CTkLabel(app, text="Minhas Atividades", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Lista de atividades pendentes e concluídas.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_desempenho():
    """Desenha a tela de verificação de Desempenho (Notas/Progresso)."""
    limpar_tela()
    app.title("Aluno - Desempenho")
    ctk.CTkLabel(app, text="Meu Desempenho", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Gráficos e relatórios de notas e progresso.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_verificar_frequencia_aluno():
    """Desenha a tela de verificação de Frequência."""
    limpar_tela()
    app.title("Aluno - Minha Frequência")
    ctk.CTkLabel(app, text="Minha Frequência", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Visualização das faltas por disciplina.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)

def tela_chat_professores_aluno():
    """Desenha a tela de chat para o Aluno interagir com os Professores."""
    limpar_tela()
    app.title("Aluno - Chat com Professores")
    ctk.CTkLabel(app, text="Chat com Professores", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a interface de chat para comunicação com os professores.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=voltar_ao_menu_principal).pack(pady=30)


# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - MENUS PRINCIPAIS DOS PERFIS
# =========================================================

def tela_coordenador():
    """Monta a tela de menu principal do perfil Coordenador."""
    limpar_tela()
    app.title("Portal Educa - Coordenador")

    ctk.CTkLabel(app, text="Bem-vindo, Coordenador!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma opção do menu para continuar.", font=fonte_campos).pack(pady=5)

    # Botões de navegação para cadastros
    ctk.CTkButton(app, text="Cadastrar Professor", font=fonte_botoes, width=250, command=tela_cadastrar_professor).pack(pady=10) 
    ctk.CTkButton(app, text="Cadastrar Aluno", font=fonte_botoes, width=250, command=tela_cadastrar_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Cadastrar Curso", font=fonte_botoes, width=250, command=tela_cadastrar_curso).pack(pady=10)
    ctk.CTkButton(app, text="Cadastrar Turma", font=fonte_botoes, width=250, command=tela_cadastrar_turma).pack(pady=10)

    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=250, command=reiniciar_login).pack(pady=20)


def tela_professor():
    """Monta a tela de menu principal do perfil Professor."""
    limpar_tela()
    app.title("Portal Educa - Professor")

    ctk.CTkLabel(app, text="Bem-vindo, Professor!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma opção do menu para continuar.", font=fonte_campos).pack(pady=5)

    # Botões de navegação para funcionalidades
    ctk.CTkButton(app, text="Adicionar Aluno à Turma", font=fonte_botoes, width=250, command=tela_adicionar_aluno_turma).pack(pady=5)
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


def tela_aluno():
    """Monta a tela de menu principal do perfil Aluno."""
    limpar_tela()
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
# REGIÃO: FUNÇÕES DE FLUXO - LOGIN E REINICIALIZAÇÃO
# =========================================================

def Tentar_Login(event=None):
    """Verifica a senha e, em caso de sucesso, chama a tela de menu correta."""
    global perfil_logado 
    
    # Necessário limpar o foco do Entry antes de verificar, para garantir que o valor está atualizado
    app.focus() 
    
    senha_digitada = senha_entry.get()
    senha_correta = None
    
    # 1. Mapeia a senha correta baseada no e-mail validado
    if email_validado == login_coordenador:
        senha_correta = senha_coordenador
        perfil_logado = "Coordenador"
    elif email_validado == login_professor:
        senha_correta = senha_professor
        perfil_logado = "Professor"
    elif email_validado == login_aluno:
        senha_correta = senha_aluno
        perfil_logado = "Aluno"
    else:
        # Erro de estado, deve ser tratado
        resultado_label.configure(text="Erro de estado de login.", text_color="orange")
        return

    # 2. Validação da senha
    if senha_digitada == senha_correta:
        
        # MUDANÇA: Maximiza a janela ao efetuar login com sucesso
        app.state('zoomed')

        # SUCESSO: Redireciona para o menu principal do perfil
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
    """Valida o e-mail digitado e faz a transição para a etapa de senha ou exibe o erro."""
    global email_validado
    
    # Necessário limpar o foco do Entry antes de verificar, para garantir que o valor está atualizado
    app.focus() 
    
    email_digitado = email_entry.get().lower()
    
    # Verifica se o e-mail corresponde a qualquer um dos cadastros
    if email_digitado == login_coordenador or \
       email_digitado == login_professor or \
       email_digitado == login_aluno:
        
        # --- E-MAIL VÁLIDO: PREPARA PARA A SENHA ---
        email_validado = email_digitado 
        perfil = Verificar_Perfil(email_validado)
        
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
        senha_entry.focus_set() # Move o foco para o campo de senha

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
    
    # Reseta o estado
    email_validado = None
    perfil_logado = None
    
    limpar_tela() # Limpa o menu atual (se houver)
    app.title("Portal Educa")

    # MUDANÇA: Retorna a janela ao tamanho e posição original (pequeno e centralizado)
    center_window(app, JANELA_WIDTH, JANELA_HEIGHT)
    app.state('normal') # Garante que não está maximizada antes de centralizar

    # Remove o bind de Enter, caso estivesse ativo no campo de senha (importante)
    senha_entry.unbind("<Return>")
    
    # Monta os widgets da Fase 1 (E-mail)
    
    # 1. Título e Instrução
    label_bem_vindo.pack(pady=20)
    resultado_label.configure(
        text="Digite seu e-mail para continuar:", 
        font=fonte_campos,
        text_color=TEMA_TEXT_COLOR
    )
    resultado_label.pack(pady=10)
    
    # 2. Campos de E-mail
    email_entry.delete(0, 'end')
    email_entry.pack(pady=10)
    button_email.pack(pady=10)
    
    # ATIVANDO O BIND DO ENTER PARA O E-MAIL
    email_entry.bind("<Return>", Validar_Email)
    email_entry.focus_set() # Define o foco no campo de e-mail
    
    # 3. Limpa o Entry de senha
    senha_entry.delete(0, 'end')
    
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

# Botão de Tema (Dark/Light) - Persistente
BTN_SIZE = 40
btn_mode_toggle = ctk.CTkButton(
    app,
    text="🌙", # Ícone inicial para modo Dark (default)
    width=BTN_SIZE,
    height=BTN_SIZE,
    corner_radius=BTN_SIZE, 
    font=("Arial", 18, "bold"),
    fg_color="#303030", 
    hover_color="#404040",
    text_color="white",
    command=toggle_appearance_mode
)
# Posicionamento fixo no canto inferior direito usando coordenadas relativas
btn_mode_toggle.place(relx=1.0, rely=1.0, x=-15, y=-15, anchor="se") 


# =========================================================
# REGIÃO: INICIALIZAÇÃO DO FLUXO
# =========================================================

# Inicia a aplicação na tela de login
reiniciar_login()
app.mainloop()