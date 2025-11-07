import customtkinter as ctk

# / / - DECLARAÇÃO DE VARIÁVEIS DE AUTENTICAÇÃO - / /

# Credenciais Fictícias
login_coordenador = "teste@coordenador.educa"
senha_coordenador = "123456"

login_professor = "teste@professor.educa"
senha_professor = "123456"

login_aluno = "teste@aluno.educa"
senha_aluno = "123456"

# Variáveis de Estado
email_validado = None
perfil_logado = None

JANELA_WIDTH = 500
JANELA_HEIGHT = 500 # Aumentada para caber os menus

# Tema de Cores Padrão (Light, Dark) - CORREÇÃO FINAL
# TEMA_TEXT_COLOR = ("white", "black")  <-- ANTERIOR (ERRADO)
TEMA_TEXT_COLOR = ("black", "white") # CORRIGIDO: Preto para Light, Branco para Dark

# / / - FUNÇÕES UTILITÁRIAS E DE LÓGICA - / /

def center_window(app, width, height):
    """Calcula e aplica a geometria para centralizar a janela na tela."""
    app.update_idletasks()
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()

    x = int((largura_tela / 2) - (width / 2))
    y = int((altura_tela / 2) - (height / 2))

    app.geometry(f"{width}x{height}+{x}+{y}")

def Verificar_Perfil(email):
    """Retorna o nome do perfil (string) baseado no e-mail."""
    email_minusculo = email.lower()
    if email_minusculo.endswith("@coordenador.educa"):
        return "Coordenador"
    elif email_minusculo.endswith("@professor.educa"):
        return "Professor"
    elif email_minusculo.endswith("@aluno.educa"):
        return "Aluno"
    return "Desconhecido"

def limpar_tela():
    """Remove todos os widgets empacotados da tela principal."""
    # Nota: O botão btn_mode_toggle usa place() e não é removido.
    for widget in app.winfo_children():
        widget.pack_forget()
        
def toggle_appearance_mode():
    """Alterna entre o modo 'Light' e 'Dark' e atualiza o ícone do botão."""
    current_mode = ctk.get_appearance_mode()
    
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")
        # Configuração para tema Light: Ícone Sol
        btn_mode_toggle.configure(text="☀️", text_color="#202020", fg_color="#F9F9FA", hover_color="#EEEEEE") 
    else:
        ctk.set_appearance_mode("Dark")
        # Configuração para tema Dark: Ícone Lua
        btn_mode_toggle.configure(text="🌙", text_color="white", fg_color="#303030", hover_color="#404040")

# / / - FUNÇÕES DE TELAS (TELAS DE MENU) - / /

def tela_coordenador():
    """Cria e exibe a tela de menu do Coordenador."""
    limpar_tela()
    app.title("Portal Educa - Coordenador")

    ctk.CTkLabel(app, text="Bem-vindo, Coordenador!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma opção do menu para continuar.", font=fonte_campos).pack(pady=5)

    # Botões do Menu
    ctk.CTkButton(app, text="Professores", font=fonte_botoes, width=250).pack(pady=10)
    ctk.CTkButton(app, text="Alunos", font=fonte_botoes, width=250).pack(pady=10)
    ctk.CTkButton(app, text="Cursos", font=fonte_botoes, width=250).pack(pady=10)
    ctk.CTkButton(app, text="Turmas", font=fonte_botoes, width=250).pack(pady=10)

    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=250, command=reiniciar_login).pack(pady=20)


def tela_professor():
    """Cria e exibe a tela de menu do Professor."""
    limpar_tela()
    app.title("Portal Educa - Professor")

    ctk.CTkLabel(app, text="Bem-vindo, Professor!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma opção do menu para continuar.", font=fonte_campos).pack(pady=5)

    # Botões do Menu
    ctk.CTkButton(app, text="Escolher Turma", font=fonte_botoes, width=250).pack(pady=10)
    ctk.CTkButton(app, text="Acessar Calendário", font=fonte_botoes, width=250).pack(pady=10)

    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=250, command=reiniciar_login).pack(pady=20)


def tela_aluno():
    """Cria e exibe a tela de menu do Aluno."""
    limpar_tela()
    app.title("Portal Educa - Aluno")

    ctk.CTkLabel(app, text="Bem-vindo, Aluno!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha uma opção do menu para continuar.", font=fonte_campos).pack(pady=5)
    
    # Botões do Menu
    ctk.CTkButton(app, text="Material Didático", font=fonte_botoes, width=250).pack(pady=5)
    ctk.CTkButton(app, text="Consultar Notas", font=fonte_botoes, width=250).pack(pady=5)
    ctk.CTkButton(app, text="Consultar Atividades", font=fonte_botoes, width=250).pack(pady=5)
    ctk.CTkButton(app, text="Consultar Desempenho", font=fonte_botoes, width=250).pack(pady=5)
    ctk.CTkButton(app, text="Consultar Frequência", font=fonte_botoes, width=250).pack(pady=5)
    ctk.CTkButton(app, text="Chat com Professores", font=fonte_botoes, width=250).pack(pady=5)
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=250, command=reiniciar_login).pack(pady=15)

# / / - FUNÇÕES DE FLUXO DE LOGIN (VALIDAÇÃO) - / /

def Tentar_Login():
    """Verifica a senha e, em caso de sucesso, chama a tela de menu correta."""
    global perfil_logado 
    
    senha_digitada = senha_entry.get()
    senha_correta = None
    
    # 1. Descobre qual senha correta usar
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
        resultado_label.configure(text="Erro de estado de login.", text_color="orange")
        return

    # 2. Valida a senha
    if senha_digitada == senha_correta:
        # SUCESSO NO LOGIN - CHAMA A FUNÇÃO DE TELA
        if perfil_logado == "Coordenador":
            tela_coordenador()
        elif perfil_logado == "Professor":
            tela_professor()
        elif perfil_logado == "Aluno":
            tela_aluno()
    else:
        # FALHA NO LOGIN
        resultado_label.configure(
            text="SENHA INCORRETA. Tente novamente.",
            text_color="red"
        )
        senha_entry.delete(0, 'end')

def Validar_Email():
    """Valida o e-mail e faz a transição para a etapa de senha ou erro."""
    global email_validado
    
    email_digitado = email_entry.get().lower()
    
    if email_digitado == login_coordenador or \
       email_digitado == login_professor or \
       email_digitado == login_aluno:
        
        # --- SUCESSO NA VALIDAÇÃO DO E-MAIL ---
        email_validado = email_digitado 
        perfil = Verificar_Perfil(email_validado)
        
        # Oculta elementos da tela de e-mail
        label_bem_vindo.pack_forget()
        email_entry.pack_forget()
        button_email.pack_forget()
        
        # Atualiza o rótulo principal para instrução de senha
        resultado_label.configure(
            text=f"Perfil encontrado: {perfil}\nDigite sua senha:", 
            text_color=TEMA_TEXT_COLOR, # Usa a tupla de cores corrigida
            font=fonte_subtitulo
        )
        
        # Exibe o campo de senha e o botão de login
        senha_entry.pack(pady=10)
        button_login.pack(pady=10)

    else:
        # --- FALHA NA VALIDAÇÃO DO E-MAIL ---
        resultado_label.configure(
            text="E-mail inválido. Tente novamente.",
            text_color="red"
        )
        email_entry.delete(0, 'end')

def reiniciar_login():
    """Reinicializa a aplicação para a tela de login inicial."""
    global email_validado, perfil_logado
    
    # Resetar variáveis de estado
    email_validado = None
    perfil_logado = None
    
    limpar_tela() # Limpa o menu atual
    app.title("Portal Educa")

    # Recria os widgets de login (usando as variáveis globais que já existem)
    
    # 1. Título e Instrução
    label_bem_vindo.pack(pady=20)
    resultado_label.configure(
        text="Digite seu e-mail para continuar:", 
        font=fonte_campos,
        text_color=TEMA_TEXT_COLOR # Usa a tupla de cores corrigida
    )
    resultado_label.pack(pady=10)
    
    # 2. Campos
    email_entry.delete(0, 'end')
    email_entry.pack(pady=10)
    button_email.pack(pady=10)
    
    # 3. Limpa a senha, caso exista algo no Entry
    senha_entry.delete(0, 'end')
    
# / / - CONFIGURAÇÃO DE APARENCIA - / /

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# / / - CONFIGURAÇÃO DA JANELA PRINCIPAL - / /

app = ctk.CTk()
app.title("Portal Educa")
center_window(app, JANELA_WIDTH, JANELA_HEIGHT)
app.resizable(False, False)

# Tratamento do ícone (mantido seu caminho local)
try:
    app.iconbitmap("C:\\Users\\willi\\OneDrive\\Documentos\\VS Code\\Portal Educa\\images\\icon.ico")
except Exception as e:
    print(f"Aviso: Não foi possível carregar o ícone. Verifique o caminho. {e}") 

# / / - CONFIGURAÇÃO DE FONTES - / /
# ESTE BLOCO FOI MOVIDO PARA CÁ PARA CORRIGIR O ERRO "Too early to use font"
fonte_titulo = ctk.CTkFont(family="Comic Sans MS", size=20, weight="bold")
fonte_subtitulo = ctk.CTkFont(family="Comic Sans MS", size=16, weight="bold")
fonte_campos = ctk.CTkFont(family="Comic Sans MS", size=12)
fonte_botoes = ctk.CTkFont(family="Comic Sans MS", size=12, weight="bold")


# / / - CRIAÇÃO DOS WIDGETS (VISÍVEIS INICIALMENTE) - / /

# Rótulo de Boas-vindas 
label_bem_vindo = ctk.CTkLabel(
    app, 
    text="Bem-vindo ao Portal Educa", 
    font=fonte_titulo
)

# 1. Rótulo de Resultado (Usado para status e instrução)
resultado_label = ctk.CTkLabel(
    app, 
    text="", 
    font=fonte_campos
    # A cor será definida dinamicamente
)

# 2. Entrada de E-mail
email_entry = ctk.CTkEntry(
    app, 
    placeholder_text="E-mail (ex: teste@coordenador.educa)", 
    font=fonte_campos, 
    justify="center", 
    width=350
)

# 3. Botão de Validação do E-mail
button_email = ctk.CTkButton(
    app, 
    text="Validar E-mail", 
    font=fonte_botoes, 
    width=100,
    command=Validar_Email
)

# / / - CRIAÇÃO DOS WIDGETS (OCULTOS INICIALMENTE) - / /

# 4. Entrada de Senha (Criado, mas não "packado")
senha_entry = ctk.CTkEntry(
    app, 
    placeholder_text="Digite sua senha", 
    font=fonte_campos, 
    justify="center", 
    show="*", # Esconde os caracteres da senha
    width=300
)

# 5. Botão de Login (Criado, mas não "packado")
button_login = ctk.CTkButton(
    app, 
    text="Login", 
    font=fonte_botoes, 
    width=100,
    command=Tentar_Login
)

# / / - CRIAÇÃO DO BOTÃO DE MODO (PERSISTENTE) - / /
BTN_SIZE = 40
btn_mode_toggle = ctk.CTkButton(
    app,
    text="🌙", # Ícone inicial para modo Dark (default)
    width=BTN_SIZE,
    height=BTN_SIZE,
    corner_radius=BTN_SIZE, # Cria um botão circular
    font=("Arial", 18, "bold"),
    fg_color="#303030", 
    hover_color="#404040",
    text_color="white",
    command=toggle_appearance_mode
)
# Posicionamento fixo no canto inferior direito
btn_mode_toggle.place(relx=1.0, rely=1.0, x=-15, y=-15, anchor="se") 


# / / - INICIA A TELA INICIAL DE LOGIN - / /
reiniciar_login()
app.mainloop()