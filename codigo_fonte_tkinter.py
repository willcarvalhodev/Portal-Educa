import customtkinter as ctk
from chat_history import load_chat_history, save_chat_history
from logged_users import (
    add_logged_user,
    remove_logged_user,
    get_logged_users,
    clear_logged_users
)
from datetime import datetime

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

# Nota: Usuários logados agora são gerenciados via arquivo JSON compartilhado
# usando o módulo logged_users.py para permitir múltiplas instâncias do programa

# Variáveis globais para os Entrys
professor_nome_entry = None
professor_email_entry = None
professor_senha_entry = None
professor_status_label = None 

professor_exclusao_status_label = None
professor_selecionado = None

aluno_exclusao_status_label = None
aluno_selecionado = None

curso_exclusao_status_label = None
curso_selecionado = None

turma_exclusao_status_label = None
turma_selecionada = None

# Widgets da tela de login
label_bem_vindo = None
resultado_label = None
email_entry = None
button_email = None
senha_entry = None
button_login = None
btn_mode_toggle = None
btn_exit = None
chat_history_box = None  # Referência global ao painel de mensagens do chat

# HISTÓRICO DE CHAT SIMULADO
try:
    MENSAGENS_CHAT = load_chat_history()
except Exception as e:
    print(f"Erro ao carregar histórico do chat: {e}")
    MENSAGENS_CHAT = [{"perfil": "Sistema", "texto": "Início da Conversa"}]

# DADOS SIMULADOS PARA EXCLUSÃO
DADOS_PROFESSORES = [
    {"id": 1, "nome": "Prof. Ana Silva", "email": "teste@professor.educa"},
    {"id": 2, "nome": "Prof. Carlos Mendes", "email": "carlos@professor.educa"},
    {"id": 3, "nome": "Prof. Mariana Costa", "email": "mariana@professor.educa"},
    {"id": 4, "nome": "Prof. João Santos", "email": "joao@professor.educa"},
    {"id": 5, "nome": "Prof. Patricia Lima", "email": "patricia@professor.educa"},
]

DADOS_ALUNOS = [
    {"matricula": "A20240001", "nome": "Aluno Bruno", "email": "teste@aluno.educa", "turma": "2024-A"},
    {"matricula": "A20240002", "nome": "Aluna Luiza", "email": "luiza@aluno.educa", "turma": "2024-A"},
    {"matricula": "A20240003", "nome": "Aluno Pedro", "email": "pedro@aluno.educa", "turma": "2024-B"},
    {"matricula": "A20240004", "nome": "Aluna Maria", "email": "maria@aluno.educa", "turma": "2024-A"},
    {"matricula": "A20240005", "nome": "Aluno Lucas", "email": "lucas@aluno.educa", "turma": "2024-B"},
]

DADOS_CURSOS = [
    {"id": 1, "nome": "Engenharia de Software"},
    {"id": 2, "nome": "Administração"},
    {"id": 3, "nome": "Ciências Contábeis"},
    {"id": 4, "nome": "Sistemas de Informação"},
    {"id": 5, "nome": "Direito"},
]

DADOS_TURMAS = [
    {"id": 1, "nome": "2024-A", "curso": "Engenharia de Software", "alunos": 30},
    {"id": 2, "nome": "2024-B", "curso": "Administração", "alunos": 25},
    {"id": 3, "nome": "2024-C", "curso": "Ciências Contábeis", "alunos": 20},
    {"id": 4, "nome": "2024-D", "curso": "Sistemas de Informação", "alunos": 28},
    {"id": 5, "nome": "2024-E", "curso": "Direito", "alunos": 35},
]

# Dimensões Padrão da Janela
JANELA_WIDTH = 400
JANELA_HEIGHT = 300 

# Dimensões para telas de listar e excluir
JANELA_LISTAR_EXCLUIR_WIDTH = 900
JANELA_LISTAR_EXCLUIR_HEIGHT = 650

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

def obter_cores_xadrez():
    """Retorna as cores para efeito xadrez baseado no modo atual (dark/light)."""
    current_mode = ctk.get_appearance_mode()
    
    if current_mode == "Dark":
        # Cores para modo escuro
        cor_par = "#2B2B2B"
        cor_impar = "#3B3B3B"
    else:
        # Cores para modo claro
        cor_par = "#F0F0F0"
        cor_impar = "#FFFFFF"
    
    return cor_par, cor_impar

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
    global funcao_atualizar_lista_atual, chat_history_box
    # Reseta a função de atualização quando limpa a tela
    funcao_atualizar_lista_atual = None
    # Reseta a referência ao painel de mensagens do chat
    chat_history_box = None
    for widget in app.winfo_children():
        if widget not in [btn_mode_toggle, btn_exit, version_label]:
            widget.destroy()

# Variável global para armazenar função de atualização atual
funcao_atualizar_lista_atual = None

def atualizar_lista_se_modo_mudou():
    """Recria a lista atual se estivermos em uma tela com lista, após mudança de modo."""
    global funcao_atualizar_lista_atual
    
    titulo_atual = app.title()
    
    # Para telas de listagem simples, recria a tela
    telas_listagem = {
        "Coordenador - Listar Professores": tela_listar_professores,
        "Coordenador - Listar Alunos": tela_listar_alunos,
        "Coordenador - Listar Cursos": tela_listar_cursos,
        "Coordenador - Listar Turmas": tela_listar_turmas,
        "Aluno - Diário Eletrônico": tela_acessar_diario,
        "Aluno - Verificar Aulas": tela_verificar_aulas,
        "Aluno - Verificar Atividades": tela_verificar_atividades_aluno,
        "Aluno - Verificar Desempenho": tela_verificar_desempenho,
        "Aluno - Verificar Frequência": tela_verificar_frequencia_aluno,
    }
    
    # Para telas de exclusão, usa a função de atualização preservada
    if titulo_atual in telas_listagem:
        # Recria a tela imediatamente
        telas_listagem[titulo_atual]()
    elif funcao_atualizar_lista_atual:
        # Chama a função de atualização que preserva estado (pesquisa e seleção)
        try:
            funcao_atualizar_lista_atual()
        except:
            # Se houver erro (tela foi fechada), não faz nada
            pass

def toggle_appearance_mode():
    """
    Alterna o modo de aparência, atualizando o ícone (🌙/☀️) 
    e a cor da borda dos botões de controle.
    Atualiza automaticamente as cores das listas se estiver em uma tela com lista.
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
    
    # Atualiza a borda do painel de mensagens do chat se existir
    global chat_history_box
    if chat_history_box is not None:
        chat_history_box.configure(border_color=new_border_color)
    
    # Atualiza as listas se estivermos em uma tela com lista
    atualizar_lista_se_modo_mudou()

def fechar_aplicacao():
    """Função para fechar o aplicativo de forma limpa."""
    app.destroy()


# =========================================================
# REGIÃO: MANUAL DO SISTEMA
# =========================================================

def tela_manual_sistema():
    """Exibe o manual do sistema com instruções específicas para cada perfil."""
    limpar_tela()
    app.update_idletasks()
    app.state('zoomed')
    app.title(f"Portal Educa - Manual do Sistema - {perfil_logado}")
    
    # Define o conteúdo do manual baseado no perfil
    if perfil_logado == "Coordenador":
        conteudo_manual = [
            ("MANUAL DO SISTEMA - COORDENADOR", "titulo"),
            ("", "espaco"),
            ("Bem-vindo ao Portal Educa! Este manual explica como utilizar cada funcionalidade disponível para o perfil Coordenador.", "texto"),
            ("", "espaco"),
            ("1. GESTÃO DE PROFESSORES", "subtitulo"),
            ("   • Cadastrar Professor: Permite adicionar novos professores ao sistema.", "item"),
            ("     - Preencha o nome completo do professor", "subitem"),
            ("     - Informe o e-mail no formato @professor.educa", "subitem"),
            ("     - Defina uma senha inicial", "subitem"),
            ("   • Apagar Professor: Remove um professor do sistema.", "item"),
            ("     - Selecione o professor na lista", "subitem"),
            ("     - Confirme a exclusão", "subitem"),
            ("   • Listar Professores: Visualiza todos os professores cadastrados.", "item"),
            ("     - Use a busca para filtrar professores", "subitem"),
            ("", "espaco"),
            ("2. GESTÃO DE ALUNOS", "subtitulo"),
            ("   • Cadastrar Aluno: Adiciona novos alunos ao sistema.", "item"),
            ("     - Preencha os dados do aluno", "subitem"),
            ("     - Informe o e-mail no formato @aluno.educa", "subitem"),
            ("   • Apagar Aluno: Remove um aluno do sistema.", "item"),
            ("   • Listar Alunos: Visualiza todos os alunos cadastrados.", "item"),
            ("", "espaco"),
            ("3. GESTÃO DE CURSOS", "subtitulo"),
            ("   • Cadastrar Curso: Cria um novo curso na instituição.", "item"),
            ("     - Informe o nome do curso", "subitem"),
            ("     - Adicione uma descrição (opcional)", "subitem"),
            ("   • Apagar Curso: Remove um curso do sistema.", "item"),
            ("   • Listar Cursos: Visualiza todos os cursos disponíveis.", "item"),
            ("", "espaco"),
            ("4. GESTÃO DE TURMAS", "subtitulo"),
            ("   • Cadastrar Turma: Cria uma nova turma.", "item"),
            ("     - Informe o nome da turma", "subitem"),
            ("     - Associe a um curso existente", "subitem"),
            ("   • Apagar Turma: Remove uma turma do sistema.", "item"),
            ("   • Listar Turmas: Visualiza todas as turmas cadastradas.", "item"),
            ("", "espaco"),
            ("5. PERFIS LOGADOS", "subtitulo"),
            ("   • Visualiza todos os usuários logados simultaneamente no sistema.", "item"),
            ("     - Veja quem está online no momento", "subitem"),
            ("     - Acompanhe data e hora de login", "subitem"),
            ("     - Monitore o tempo online de cada usuário", "subitem"),
            ("     - Visualize estatísticas por perfil", "subitem"),
            ("", "espaco"),
            ("DICAS IMPORTANTES:", "subtitulo"),
            ("• Sempre verifique os dados antes de confirmar cadastros", "dica"),
            ("• Use a função de busca para encontrar registros rapidamente", "dica"),
            ("• O sistema atualiza automaticamente a lista de perfis logados", "dica"),
            ("• Para sair do sistema, use o botão 'Sair (Logout)'", "dica"),
        ]
    elif perfil_logado == "Professor":
        conteudo_manual = [
            ("MANUAL DO SISTEMA - PROFESSOR", "titulo"),
            ("", "espaco"),
            ("Bem-vindo ao Portal Educa! Este manual explica como utilizar cada funcionalidade disponível para o perfil Professor.", "texto"),
            ("", "espaco"),
            ("1. GESTÃO DE TURMAS", "subtitulo"),
            ("   • Visualizar Turmas: Veja todas as turmas atribuídas a você.", "item"),
            ("     - A lista mostra as turmas sob sua responsabilidade", "subitem"),
            ("     - Você pode verificar os alunos de cada turma", "subitem"),
            ("   • Adicionar Aluno à Turma: Inclui alunos em suas turmas.", "item"),
            ("     - Selecione a turma desejada", "subitem"),
            ("     - Informe o nome ou matrícula do aluno", "subitem"),
            ("", "espaco"),
            ("2. GESTÃO DE ATIVIDADES", "subtitulo"),
            ("   • Postar Atividades: Cria e publica atividades para os alunos.", "item"),
            ("     - Defina o título da atividade", "subitem"),
            ("     - Adicione uma descrição detalhada", "subitem"),
            ("     - Informe a data de entrega", "subitem"),
            ("     - Selecione o tipo (Trabalho, Prova, Projeto, etc.)", "subitem"),
            ("   • Visualizar Atividades: Veja todas as atividades postadas.", "item"),
            ("     - Filtre por turma ou data", "subitem"),
            ("     - Acompanhe o status de entrega dos alunos", "subitem"),
            ("", "espaco"),
            ("3. GESTÃO DE NOTAS", "subtitulo"),
            ("   • Lançar Notas: Registra as notas dos alunos.", "item"),
            ("     - Selecione o aluno", "subitem"),
            ("     - Informe a nota obtida", "subitem"),
            ("     - Associe a uma atividade ou avaliação", "subitem"),
            ("   • Visualizar Notas: Consulta o desempenho dos alunos.", "item"),
            ("     - Veja o histórico de notas por aluno", "subitem"),
            ("     - Analise médias e estatísticas", "subitem"),
            ("", "espaco"),
            ("4. GESTÃO DE FREQUÊNCIA", "subtitulo"),
            ("   • Lançar Frequência: Registra a presença dos alunos.", "item"),
            ("     - Marque presença ou falta", "subitem"),
            ("     - Informe a data da aula", "subitem"),
            ("     - Selecione a turma e disciplina", "subitem"),
            ("   • Visualizar Frequência: Consulta o registro de presenças.", "item"),
            ("     - Veja o percentual de frequência por aluno", "subitem"),
            ("     - Identifique alunos com baixa frequência", "subitem"),
            ("", "espaco"),
            ("5. COMUNICAÇÃO", "subtitulo"),
            ("   • Chat com Alunos: Comunique-se com seus alunos.", "item"),
            ("     - Envie mensagens para os alunos", "subitem"),
            ("     - Receba e responda dúvidas", "subitem"),
            ("     - O histórico de conversas é salvo automaticamente", "subitem"),
            ("", "espaco"),
            ("DICAS IMPORTANTES:", "subtitulo"),
            ("• Sempre verifique os dados antes de lançar notas ou frequência", "dica"),
            ("• Use datas corretas ao postar atividades", "dica"),
            ("• Mantenha a comunicação com alunos de forma clara e objetiva", "dica"),
            ("• Revise as atividades antes de publicá-las", "dica"),
        ]
    elif perfil_logado == "Aluno":
        conteudo_manual = [
            ("MANUAL DO SISTEMA - ALUNO", "titulo"),
            ("", "espaco"),
            ("Bem-vindo ao Portal Educa! Este manual explica como utilizar cada funcionalidade disponível para o perfil Aluno.", "texto"),
            ("", "espaco"),
            ("1. INFORMAÇÕES PESSOAIS", "subtitulo"),
            ("   • Visualizar Informações: Veja seus dados cadastrais.", "item"),
            ("     - Consulte seu nome, e-mail e matrícula", "subitem"),
            ("     - Verifique sua turma e curso", "subitem"),
            ("     - Acesse informações de contato", "subitem"),
            ("", "espaco"),
            ("2. AULAS", "subtitulo"),
            ("   • Verificar Aulas: Consulte sua grade de horários.", "item"),
            ("     - Veja as disciplinas do seu curso", "subitem"),
            ("     - Confira horários e salas", "subitem"),
            ("     - Acompanhe o calendário acadêmico", "subitem"),
            ("", "espaco"),
            ("3. ATIVIDADES", "subtitulo"),
            ("   • Verificar Atividades: Veja todas as atividades atribuídas.", "item"),
            ("     - Consulte atividades pendentes", "subitem"),
            ("     - Veja prazos de entrega", "subitem"),
            ("     - Acompanhe atividades já entregues", "subitem"),
            ("     - Verifique o status de cada atividade", "subitem"),
            ("", "espaco"),
            ("4. AVALIAÇÕES", "subtitulo"),
            ("   • Verificar Desempenho: Consulte suas notas e avaliações.", "item"),
            ("     - Veja suas notas por disciplina", "subitem"),
            ("     - Acompanhe sua média geral", "subitem"),
            ("     - Consulte resultados de provas e trabalhos", "subitem"),
            ("   • Verificar Frequência: Veja seu registro de presenças.", "item"),
            ("     - Consulte seu percentual de frequência", "subitem"),
            ("     - Veja dias de presença e falta", "subitem"),
            ("     - Acompanhe sua frequência por disciplina", "subitem"),
            ("", "espaco"),
            ("5. COMUNICAÇÃO", "subtitulo"),
            ("   • Chat com Professores: Comunique-se com seus professores.", "item"),
            ("     - Envie mensagens para seus professores", "subitem"),
            ("     - Tire dúvidas sobre atividades e conteúdos", "subitem"),
            ("     - O histórico de conversas é salvo automaticamente", "subitem"),
            ("", "espaco"),
            ("DICAS IMPORTANTES:", "subtitulo"),
            ("• Verifique regularmente suas atividades e prazos", "dica"),
            ("• Mantenha-se atualizado sobre suas notas e frequência", "dica"),
            ("• Use a comunicação para tirar dúvidas com professores", "dica"),
            ("• Organize-se para não perder prazos de entrega", "dica"),
        ]
    else:
        conteudo_manual = [
            ("MANUAL DO SISTEMA", "titulo"),
            ("", "espaco"),
            ("Perfil não identificado. Por favor, faça login novamente.", "texto"),
        ]
    
    # Frame principal com scroll
    main_frame = ctk.CTkScrollableFrame(app, width=1000, height=700)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Renderiza o conteúdo
    for item in conteudo_manual:
        texto, tipo = item
        
        if tipo == "titulo":
            ctk.CTkLabel(
                main_frame,
                text=texto,
                font=fonte_titulo,
                text_color="#2196F3"
            ).pack(pady=15, padx=20)
        elif tipo == "subtitulo":
            ctk.CTkLabel(
                main_frame,
                text=texto,
                font=fonte_subtitulo,
                text_color="#FF9800"
            ).pack(pady=10, padx=20, anchor="w")
        elif tipo == "texto":
            ctk.CTkLabel(
                main_frame,
                text=texto,
                font=fonte_campos,
                justify="left",
                wraplength=900
            ).pack(pady=5, padx=20, anchor="w")
        elif tipo == "item":
            ctk.CTkLabel(
                main_frame,
                text=texto,
                font=fonte_campos,
                justify="left",
                wraplength=900
            ).pack(pady=3, padx=40, anchor="w")
        elif tipo == "subitem":
            ctk.CTkLabel(
                main_frame,
                text=texto,
                font=("Arial", 11),
                text_color="gray",
                justify="left",
                wraplength=850
            ).pack(pady=2, padx=60, anchor="w")
        elif tipo == "dica":
            ctk.CTkLabel(
                main_frame,
                text=texto,
                font=("Arial", 11, "italic"),
                text_color="#4CAF50",
                justify="left",
                wraplength=900
            ).pack(pady=3, padx=20, anchor="w")
        elif tipo == "espaco":
            ctk.CTkLabel(
                main_frame,
                text=" ",
                font=("Arial", 5)
            ).pack(pady=5)
    
    # Botão voltar
    def voltar_menu():
        """Volta para o menu principal do perfil."""
        if perfil_logado == "Coordenador":
            tela_coordenador()
        elif perfil_logado == "Professor":
            tela_professor()
        elif perfil_logado == "Aluno":
            tela_aluno()
    
    ctk.CTkButton(
        main_frame,
        text="<< Voltar ao Menu Principal",
        font=fonte_botoes,
        width=300,
        command=voltar_menu
    ).pack(pady=30)


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
    ctk.CTkLabel(app, text="Escolha um tema para continuar:", font=fonte_subtitulo).pack(pady=5)

    # Botões de navegação para as telas de Gestão Modular
    ctk.CTkButton(app, text="Professor", font=fonte_botoes, width=300, command=tela_gestao_professor).pack(pady=10) 
    ctk.CTkButton(app, text="Aluno", font=fonte_botoes, width=300, command=tela_gestao_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Curso", font=fonte_botoes, width=300, command=tela_gestao_curso).pack(pady=10)
    ctk.CTkButton(app, text="Turma", font=fonte_botoes, width=300, command=tela_gestao_turma).pack(pady=10)
    ctk.CTkButton(app, text="Perfis Logados", font=fonte_botoes, width=300, command=tela_perfis_logados, fg_color="#9C27B0", hover_color="#7B1FA2").pack(pady=10)
    ctk.CTkButton(app, text="📖 Manual do Sistema", font=fonte_botoes, width=300, command=tela_manual_sistema, fg_color="#607D8B", hover_color="#455A64").pack(pady=10)
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=300, command=reiniciar_login).pack(pady=30)


def tela_professor():
    """Monta a tela de menu principal do perfil Professor."""
    limpar_tela()
    app.update_idletasks()
    app.state('zoomed')
    app.title("Portal Educa - Professor")

    ctk.CTkLabel(app, text="Bem-vindo, Professor!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha um tema para continuar:", font=fonte_subtitulo).pack(pady=5)

    # Botões de temas principais
    ctk.CTkButton(app, text="Turmas", font=fonte_botoes, width=300, command=tela_gestao_turmas_prof).pack(pady=10)
    ctk.CTkButton(app, text="Atividades", font=fonte_botoes, width=300, command=tela_gestao_atividades_prof).pack(pady=10)
    ctk.CTkButton(app, text="Notas", font=fonte_botoes, width=300, command=tela_gestao_notas_prof).pack(pady=10)
    ctk.CTkButton(app, text="Frequência", font=fonte_botoes, width=300, command=tela_gestao_frequencia_prof).pack(pady=10)
    ctk.CTkButton(app, text="Comunicação", font=fonte_botoes, width=300, command=tela_gestao_comunicacao_prof).pack(pady=10)
    ctk.CTkButton(app, text="📖 Manual do Sistema", font=fonte_botoes, width=300, command=tela_manual_sistema, fg_color="#607D8B", hover_color="#455A64").pack(pady=10)
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=300, command=reiniciar_login).pack(pady=30)

# =========================================================
# REGIÃO: FUNÇÕES DO PERFIL ALUNO
# =========================================================

# --- Telas de Gestão (Subtemas) para Aluno ---

def tela_gestao_informacoes_aluno():
    """Menu de gestão de Informações para Aluno."""
    limpar_tela()
    app.title("Aluno - Informações")
    app.state('zoomed')

    ctk.CTkLabel(app, text="INFORMAÇÕES", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Acessar Diário Eletrônico", font=fonte_botoes, width=300, command=tela_acessar_diario).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_aluno).pack(pady=30)

def tela_gestao_aulas_aluno():
    """Menu de gestão de Aulas para Aluno."""
    limpar_tela()
    app.title("Aluno - Aulas")
    app.state('zoomed')

    ctk.CTkLabel(app, text="AULAS", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Verificar Aulas", font=fonte_botoes, width=300, command=tela_verificar_aulas).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_aluno).pack(pady=30)

def tela_gestao_atividades_aluno():
    """Menu de gestão de Atividades para Aluno."""
    limpar_tela()
    app.title("Aluno - Atividades")
    app.state('zoomed')

    ctk.CTkLabel(app, text="ATIVIDADES", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Verificar Atividades", font=fonte_botoes, width=300, command=tela_verificar_atividades_aluno).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_aluno).pack(pady=30)

def tela_gestao_avaliacoes_aluno():
    """Menu de gestão de Avaliações para Aluno."""
    limpar_tela()
    app.title("Aluno - Avaliações")
    app.state('zoomed')

    ctk.CTkLabel(app, text="AVALIAÇÕES", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Verificar Desempenho", font=fonte_botoes, width=300, command=tela_verificar_desempenho).pack(pady=10)
    ctk.CTkButton(app, text="Verificar Frequência", font=fonte_botoes, width=300, command=tela_verificar_frequencia_aluno).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_aluno).pack(pady=30)

def tela_gestao_comunicacao_aluno():
    """Menu de gestão de Comunicação para Aluno."""
    limpar_tela()
    app.title("Aluno - Comunicação")
    app.state('zoomed')

    ctk.CTkLabel(app, text="COMUNICAÇÃO", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Chat com Professores", font=fonte_botoes, width=300, command=tela_chat_professores_aluno).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_aluno).pack(pady=30)

# --- Telas Específicas do Aluno ---

def tela_acessar_diario():
    """Desenha a tela de acesso ao diário eletrônico do aluno."""
    limpar_tela()
    app.title("Aluno - Diário Eletrônico")
    app.update_idletasks()
    app.state('zoomed')
    
    ctk.CTkLabel(app, text="Diário Eletrônico", font=fonte_titulo).pack(pady=30)
    
    # Container principal centralizado
    container_frame = ctk.CTkFrame(app, fg_color="transparent")
    container_frame.pack(pady=20, padx=50, fill="both", expand=True)
    
    # Frame para informações pessoais (simples e limpo)
    info_frame = ctk.CTkFrame(container_frame)
    info_frame.pack(pady=15, padx=20, fill="x")
    
    ctk.CTkLabel(
        info_frame, 
        text="Informações do Aluno", 
        font=("Arial", 18, "bold")
    ).pack(pady=(15, 20))
    
    # Informações organizadas de forma limpa
    informacoes = [
        ("Matrícula", "A20240001"),
        ("Nome", "Aluno Teste"),
        ("Curso", "Engenharia de Software"),
        ("Turma", "2024-A"),
        ("Status", "Matriculado")
    ]
    
    for label, valor in informacoes:
        linha_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha_frame.pack(fill="x", padx=30, pady=8)
        
        ctk.CTkLabel(
            linha_frame, 
            text=f"{label}:", 
            font=("Arial", 14, "bold"),
            width=150,
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            linha_frame, 
            text=valor, 
            font=fonte_campos,
            anchor="w"
        ).pack(side="left", padx=(10, 0))
    
    # Frame para notas e frequência (em uma linha horizontal)
    dados_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
    dados_frame.pack(pady=15, padx=20, fill="both", expand=True)
    
    # Frame de notas
    notas_frame = ctk.CTkFrame(dados_frame)
    notas_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    ctk.CTkLabel(
        notas_frame, 
        text="Notas", 
        font=("Arial", 18, "bold")
    ).pack(pady=(15, 20))
    
    notas = [
        ("Programação I", "8.5"),
        ("Banco de Dados", "7.8"),
        ("Engenharia de Software", "9.2"),
        ("Algoritmos", "8.0"),
        ("Projeto Integrador", "9.5")
    ]
    
    for materia, nota in notas:
        linha_frame = ctk.CTkFrame(notas_frame, fg_color="transparent")
        linha_frame.pack(fill="x", padx=20, pady=6)
        
        ctk.CTkLabel(
            linha_frame, 
            text=materia, 
            font=fonte_campos,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            linha_frame, 
            text=nota, 
            font=("Arial", 14, "bold"),
            width=50,
            anchor="e"
        ).pack(side="right")
    
    # Frame de frequência
    frequencia_frame = ctk.CTkFrame(dados_frame)
    frequencia_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    ctk.CTkLabel(
        frequencia_frame, 
        text="Frequência", 
        font=("Arial", 18, "bold")
    ).pack(pady=(15, 20))
    
    frequencias = [
        ("Programação I", "95%"),
        ("Banco de Dados", "88%"),
        ("Engenharia de Software", "92%"),
        ("Algoritmos", "90%"),
        ("Projeto Integrador", "98%")
    ]
    
    for materia, freq in frequencias:
        linha_frame = ctk.CTkFrame(frequencia_frame, fg_color="transparent")
        linha_frame.pack(fill="x", padx=20, pady=6)
        
        ctk.CTkLabel(
            linha_frame, 
            text=materia, 
            font=fonte_campos,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            linha_frame, 
            text=freq, 
            font=("Arial", 14, "bold"),
            width=50,
            anchor="e"
        ).pack(side="right")
    
    ctk.CTkButton(app, text="<< Voltar às Informações", 
                 font=fonte_botoes, width=300, 
                 command=tela_gestao_informacoes_aluno).pack(pady=30)

def tela_verificar_aulas():
    """Desenha a tela para verificar as aulas do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Aulas")
    app.update_idletasks()
    app.state('zoomed')
    
    ctk.CTkLabel(app, text="Minhas Aulas", font=fonte_titulo).pack(pady=20)
    
    # Frame scrollable para as aulas
    aulas_frame = ctk.CTkScrollableFrame(app, width=800, height=400)
    aulas_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Obtém as cores para efeito xadrez
    cor_par, cor_impar = obter_cores_xadrez()
    
    # Dados das aulas com mais informações
    aulas = [
        {
            "dia": "Segunda-feira",
            "materia": "Programação I",
            "horario": "08:00 - 10:00",
            "professor": "Prof. Ana Silva",
            "sala": "Sala 101"
        },
        {
            "dia": "Terça-feira",
            "materia": "Banco de Dados",
            "horario": "10:00 - 12:00",
            "professor": "Prof. Carlos Mendes",
            "sala": "Sala 102"
        },
        {
            "dia": "Quarta-feira",
            "materia": "Engenharia de Software",
            "horario": "14:00 - 16:00",
            "professor": "Prof. Mariana Costa",
            "sala": "Sala 103"
        },
        {
            "dia": "Quinta-feira",
            "materia": "Algoritmos",
            "horario": "16:00 - 18:00",
            "professor": "Prof. João Santos",
            "sala": "Sala 104"
        },
        {
            "dia": "Sexta-feira",
            "materia": "Projeto Integrador",
            "horario": "19:00 - 21:00",
            "professor": "Prof. Patricia Lima",
            "sala": "Sala 105"
        }
    ]
    
    # Cria os itens das aulas com efeito xadrez
    for idx, aula in enumerate(aulas):
        item_frame = ctk.CTkFrame(aulas_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        # Formata o texto da aula
        texto_aula = f"{aula['dia']} | {aula['materia']} | {aula['horario']}"
        texto_detalhes = f"Professor: {aula['professor']} | Sala: {aula['sala']}"
        
        # Label principal
        aula_label = ctk.CTkLabel(
            item_frame, 
            text=texto_aula, 
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        aula_label.pack(pady=(8, 2), padx=15, fill="x")
        
        # Label de detalhes
        detalhes_label = ctk.CTkLabel(
            item_frame, 
            text=texto_detalhes, 
            font=fonte_campos,
            anchor="w",
            text_color=("gray60", "gray40")
        )
        detalhes_label.pack(pady=(0, 8), padx=15, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar às Aulas", 
                 font=fonte_botoes, width=300, 
                 command=tela_gestao_aulas_aluno).pack(pady=20)

def tela_verificar_atividades_aluno():
    """Desenha a tela para verificar as atividades do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Atividades")
    app.update_idletasks()
    app.state('zoomed')
    
    ctk.CTkLabel(app, text="Minhas Atividades", font=fonte_titulo).pack(pady=20)
    
    # Frame scrollable para as atividades
    atividades_frame = ctk.CTkScrollableFrame(app, width=800, height=400)
    atividades_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Obtém as cores para efeito xadrez
    cor_par, cor_impar = obter_cores_xadrez()
    
    # Dados das atividades com mais informações
    atividades = [
        {
            "titulo": "Trabalho de Programação I",
            "tipo": "Trabalho",
            "data_entrega": "20/11/2023",
            "status": "Pendente",
            "materia": "Programação I"
        },
        {
            "titulo": "Prova de Banco de Dados",
            "tipo": "Prova",
            "data_entrega": "25/11/2023",
            "status": "Pendente",
            "materia": "Banco de Dados"
        },
        {
            "titulo": "Projeto de Engenharia de Software",
            "tipo": "Projeto",
            "data_entrega": "30/11/2023",
            "status": "Pendente",
            "materia": "Engenharia de Software"
        },
        {
            "titulo": "Lista de Exercícios Algoritmos",
            "tipo": "Lista de Exercícios",
            "data_entrega": "05/12/2023",
            "status": "Pendente",
            "materia": "Algoritmos"
        },
        {
            "titulo": "Apresentação Projeto Integrador",
            "tipo": "Apresentação",
            "data_entrega": "15/12/2023",
            "status": "Pendente",
            "materia": "Projeto Integrador"
        }
    ]
    
    # Cria os itens das atividades com efeito xadrez
    for idx, atividade in enumerate(atividades):
        item_frame = ctk.CTkFrame(atividades_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        # Formata o texto da atividade
        texto_principal = f"{atividade['titulo']} | {atividade['materia']}"
        texto_detalhes = f"Tipo: {atividade['tipo']} | Entrega: {atividade['data_entrega']} | Status: {atividade['status']}"
        
        # Label principal
        atividade_label = ctk.CTkLabel(
            item_frame, 
            text=texto_principal, 
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        atividade_label.pack(pady=(8, 2), padx=15, fill="x")
        
        # Label de detalhes
        detalhes_label = ctk.CTkLabel(
            item_frame, 
            text=texto_detalhes, 
            font=fonte_campos,
            anchor="w",
            text_color=("gray60", "gray40")
        )
        detalhes_label.pack(pady=(0, 8), padx=15, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar às Atividades", 
                 font=fonte_botoes, width=300, 
                 command=tela_gestao_atividades_aluno).pack(pady=20)

def tela_verificar_desempenho():
    """Desenha a tela para verificar o desempenho do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Desempenho")
    app.update_idletasks()
    app.state('zoomed')
    
    ctk.CTkLabel(app, text="Meu Desempenho", font=fonte_titulo).pack(pady=20)
    
    # Frame scrollable para as notas
    desempenho_frame = ctk.CTkScrollableFrame(app, width=800, height=400)
    desempenho_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Obtém as cores para efeito xadrez
    cor_par, cor_impar = obter_cores_xadrez()
    
    # Dados de desempenho com mais informações
    desempenhos = [
        {
            "materia": "Programação I",
            "nota": "8.5",
            "status": "Aprovado",
            "faltas": "5"
        },
        {
            "materia": "Banco de Dados",
            "nota": "9.0",
            "status": "Aprovado",
            "faltas": "3"
        },
        {
            "materia": "Engenharia de Software",
            "nota": "8.0",
            "status": "Aprovado",
            "faltas": "2"
        },
        {
            "materia": "Algoritmos",
            "nota": "7.5",
            "status": "Aprovado",
            "faltas": "4"
        },
        {
            "materia": "Projeto Integrador",
            "nota": "9.5",
            "status": "Aprovado",
            "faltas": "1"
        }
    ]
    
    # Cria os itens de desempenho com efeito xadrez
    for idx, desempenho in enumerate(desempenhos):
        item_frame = ctk.CTkFrame(desempenho_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        # Formata o texto do desempenho
        texto_principal = f"{desempenho['materia']} | Nota: {desempenho['nota']}"
        texto_detalhes = f"Status: {desempenho['status']} | Faltas: {desempenho['faltas']}"
        
        # Label principal
        desempenho_label = ctk.CTkLabel(
            item_frame, 
            text=texto_principal, 
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        desempenho_label.pack(pady=(8, 2), padx=15, fill="x")
        
        # Label de detalhes
        detalhes_label = ctk.CTkLabel(
            item_frame, 
            text=texto_detalhes, 
            font=fonte_campos,
            anchor="w",
            text_color=("gray60", "gray40")
        )
        detalhes_label.pack(pady=(0, 8), padx=15, fill="x")
    
    # Frame para média geral (destaque)
    media_frame = ctk.CTkFrame(desempenho_frame, border_width=2, corner_radius=8)
    media_frame.configure(fg_color=cor_par, border_color="#1f538d")
    media_frame.pack(fill="x", pady=(10, 2), padx=5)
    
    media_label = ctk.CTkLabel(
        media_frame, 
        text="Média Geral: 8.5", 
        font=("Arial", 16, "bold"),
        anchor="w"
    )
    media_label.pack(pady=12, padx=15, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar às Avaliações", 
                 font=fonte_botoes, width=300, 
                 command=tela_gestao_avaliacoes_aluno).pack(pady=20)

def tela_verificar_frequencia_aluno():
    """Desenha a tela para verificar a frequência do aluno."""
    limpar_tela()
    app.title("Aluno - Verificar Frequência")
    app.update_idletasks()
    app.state('zoomed')
    
    ctk.CTkLabel(app, text="Minha Frequência", font=fonte_titulo).pack(pady=20)
    
    # Frame scrollable para a frequência
    freq_frame = ctk.CTkScrollableFrame(app, width=800, height=400)
    freq_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Obtém as cores para efeito xadrez
    cor_par, cor_impar = obter_cores_xadrez()
    
    # Dados de frequência com mais informações
    frequencias = [
        {
            "materia": "Programação I",
            "percentual": "90%",
            "presencas": "27",
            "faltas": "3",
            "total_aulas": "30"
        },
        {
            "materia": "Banco de Dados",
            "percentual": "85%",
            "presencas": "34",
            "faltas": "6",
            "total_aulas": "40"
        },
        {
            "materia": "Engenharia de Software",
            "percentual": "95%",
            "presencas": "38",
            "faltas": "2",
            "total_aulas": "40"
        },
        {
            "materia": "Algoritmos",
            "percentual": "88%",
            "presencas": "35",
            "faltas": "5",
            "total_aulas": "40"
        },
        {
            "materia": "Projeto Integrador",
            "percentual": "92%",
            "presencas": "23",
            "faltas": "2",
            "total_aulas": "25"
        }
    ]
    
    # Cria os itens de frequência com efeito xadrez
    for idx, frequencia in enumerate(frequencias):
        item_frame = ctk.CTkFrame(freq_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        # Formata o texto da frequência
        texto_principal = f"{frequencia['materia']} | Frequência: {frequencia['percentual']}"
        texto_detalhes = f"Presenças: {frequencia['presencas']} | Faltas: {frequencia['faltas']} | Total de Aulas: {frequencia['total_aulas']}"
        
        # Label principal
        freq_label = ctk.CTkLabel(
            item_frame, 
            text=texto_principal, 
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        freq_label.pack(pady=(8, 2), padx=15, fill="x")
        
        # Label de detalhes
        detalhes_label = ctk.CTkLabel(
            item_frame, 
            text=texto_detalhes, 
            font=fonte_campos,
            anchor="w",
            text_color=("gray60", "gray40")
        )
        detalhes_label.pack(pady=(0, 8), padx=15, fill="x")
    
    # Frame para frequência geral (destaque)
    freq_geral_frame = ctk.CTkFrame(freq_frame, border_width=2, corner_radius=8)
    freq_geral_frame.configure(fg_color=cor_par, border_color="#1f538d")
    freq_geral_frame.pack(fill="x", pady=(10, 2), padx=5)
    
    freq_geral_label = ctk.CTkLabel(
        freq_geral_frame, 
        text="Frequência Geral: 90%", 
        font=("Arial", 16, "bold"),
        anchor="w"
    )
    freq_geral_label.pack(pady=12, padx=15, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar às Avaliações", 
                 font=fonte_botoes, width=300, 
                 command=tela_gestao_avaliacoes_aluno).pack(pady=20)

def tela_aluno():
    """Monta a tela de menu principal do perfil Aluno."""
    limpar_tela()
    app.update_idletasks()
    app.state('zoomed')
    app.title("Portal Educa - Aluno")

    ctk.CTkLabel(app, text="Bem-vindo, Aluno!", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Escolha um tema para continuar:", font=fonte_subtitulo).pack(pady=5)
    
    # Botões de temas principais
    ctk.CTkButton(app, text="Informações", font=fonte_botoes, width=300, command=tela_gestao_informacoes_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Aulas", font=fonte_botoes, width=300, command=tela_gestao_aulas_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Atividades", font=fonte_botoes, width=300, command=tela_gestao_atividades_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Avaliações", font=fonte_botoes, width=300, command=tela_gestao_avaliacoes_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Comunicação", font=fonte_botoes, width=300, command=tela_gestao_comunicacao_aluno).pack(pady=10)
    ctk.CTkButton(app, text="📖 Manual do Sistema", font=fonte_botoes, width=300, command=tela_manual_sistema, fg_color="#607D8B", hover_color="#455A64").pack(pady=10)
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=300, command=reiniciar_login).pack(pady=30)


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
    global perfil_logado, email_validado
    
    app.focus() 
    
    senha_digitada = senha_entry.get()
    
    # SIMULAÇÃO DE BUSCA NO DB (Usando variáveis globais)
    credencial = CREDENCIAS.get(email_validado)
    senha_correta = credencial["senha"] if credencial else None
    
    # 1. Validação da senha
    if credencial and senha_digitada == senha_correta:
        
        # SUCESSO NO LOGIN
        perfil_logado = credencial["perfil"]
        
        # Registra o usuário na lista de logados (arquivo compartilhado)
        add_logged_user(email_validado, perfil_logado)
        
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
    
    # Remove o usuário da lista de logados ao fazer logout (arquivo compartilhado)
    if email_validado:
        remove_logged_user(email_validado)
    
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
    global DADOS_PROFESSORES, DADOS_ALUNOS, DADOS_CURSOS, DADOS_TURMAS
    
    # Remove o item da lista correspondente
    if tipo == "Professor":
        DADOS_PROFESSORES = [p for p in DADOS_PROFESSORES if p["email"] != item]
    elif tipo == "Aluno":
        DADOS_ALUNOS = [a for a in DADOS_ALUNOS if a["email"] != item]
    elif tipo == "Curso":
        DADOS_CURSOS = [c for c in DADOS_CURSOS if c["nome"] != item]
    elif tipo == "Turma":
        DADOS_TURMAS = [t for t in DADOS_TURMAS if t["nome"] != item]
    
    status_label.configure(text=f"{tipo} '{item}' excluído com sucesso!", text_color="green")
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


# --- LISTAR/VISUALIZAR SIMULADO ---

def tela_listar_professores():
    """SIMULAÇÃO: Exibe a lista de professores."""
    limpar_tela()
    app.title("Coordenador - Listar Professores")
    app.update_idletasks()
    app.state('zoomed')
    ctk.CTkLabel(app, text="LISTA DE PROFESSORES (Simulação)", font=fonte_titulo).pack(pady=30)
    
    # Frame scrollable para a lista
    lista_frame = ctk.CTkScrollableFrame(app, width=700, height=400)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Cores para efeito xadrez (adaptáveis ao modo)
    cor_par, cor_impar = obter_cores_xadrez()
    
    for idx, prof in enumerate(DADOS_PROFESSORES):
        # Cria um frame para cada item com cor alternada
        item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        texto = f"ID: {prof['id']} | Nome: {prof['nome']} | Email: {prof['email']}"
        ctk.CTkLabel(item_frame, text=texto, font=fonte_campos, justify="left", anchor="w").pack(pady=8, padx=10, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Professor", font=fonte_botoes, width=300, command=tela_gestao_professor).pack(pady=20)


def tela_listar_alunos():
    """SIMULAÇÃO: Exibe a lista de alunos."""
    limpar_tela()
    app.title("Coordenador - Listar Alunos")
    app.update_idletasks()
    app.state('zoomed')
    ctk.CTkLabel(app, text="LISTA DE ALUNOS (Simulação)", font=fonte_titulo).pack(pady=30)
    
    # Frame scrollable para a lista
    lista_frame = ctk.CTkScrollableFrame(app, width=700, height=400)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Cores para efeito xadrez (adaptáveis ao modo)
    cor_par, cor_impar = obter_cores_xadrez()
    
    for idx, aluno in enumerate(DADOS_ALUNOS):
        # Cria um frame para cada item com cor alternada
        item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        texto = f"Mat: {aluno['matricula']} | Nome: {aluno['nome']} | Email: {aluno['email']} | Turma: {aluno['turma']}"
        ctk.CTkLabel(item_frame, text=texto, font=fonte_campos, justify="left", anchor="w").pack(pady=8, padx=10, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Aluno", font=fonte_botoes, width=300, command=tela_gestao_aluno).pack(pady=20)

def tela_listar_cursos():
    """SIMULAÇÃO: Exibe a lista de cursos."""
    limpar_tela()
    app.title("Coordenador - Listar Cursos")
    app.update_idletasks()
    app.state('zoomed')
    ctk.CTkLabel(app, text="LISTA DE CURSOS (Simulação)", font=fonte_titulo).pack(pady=30)
    
    # Frame scrollable para a lista
    lista_frame = ctk.CTkScrollableFrame(app, width=700, height=400)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Cores para efeito xadrez (adaptáveis ao modo)
    cor_par, cor_impar = obter_cores_xadrez()
    
    for idx, curso in enumerate(DADOS_CURSOS):
        # Cria um frame para cada item com cor alternada
        item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        texto = f"ID: {curso['id']} | Curso: {curso['nome']}"
        ctk.CTkLabel(item_frame, text=texto, font=fonte_campos, justify="left", anchor="w").pack(pady=8, padx=10, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Curso", font=fonte_botoes, width=300, command=tela_gestao_curso).pack(pady=20)

def tela_listar_turmas():
    """SIMULAÇÃO: Exibe a lista de turmas."""
    limpar_tela()
    app.title("Coordenador - Listar Turmas")
    app.update_idletasks()
    app.state('zoomed')
    ctk.CTkLabel(app, text="LISTA DE TURMAS (Simulação)", font=fonte_titulo).pack(pady=30)
    
    # Frame scrollable para a lista
    lista_frame = ctk.CTkScrollableFrame(app, width=700, height=400)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Cores para efeito xadrez (adaptáveis ao modo)
    cor_par, cor_impar = obter_cores_xadrez()
    
    for idx, turma in enumerate(DADOS_TURMAS):
        # Cria um frame para cada item com cor alternada
        item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
        if idx % 2 == 0:
            item_frame.configure(fg_color=cor_par)
        else:
            item_frame.configure(fg_color=cor_impar)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        texto = f"ID: {turma['id']} | Turma: {turma['nome']} | Curso: {turma['curso']} | Alunos: {turma['alunos']}"
        ctk.CTkLabel(item_frame, text=texto, font=fonte_campos, justify="left", anchor="w").pack(pady=8, padx=10, fill="x")
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Turma", font=fonte_botoes, width=300, command=tela_gestao_turma).pack(pady=20)


# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - TELAS DE GESTÃO MODULAR
# =========================================================

def tela_gestao_professor():
    """Menu modular para gestão de Professores: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Professor")
    app.state('zoomed')

    ctk.CTkLabel(app, text="GESTÃO DE PROFESSOR", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="1. Cadastrar Professor", font=fonte_botoes, width=300, command=tela_cadastrar_professor).pack(pady=10)
    ctk.CTkButton(app, text="2. Apagar Professor", font=fonte_botoes, width=300, command=tela_excluir_professor).pack(pady=10)
    ctk.CTkButton(app, text="3. Listar Professores", font=fonte_botoes, width=300, command=tela_listar_professores).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_coordenador).pack(pady=30)

def tela_gestao_aluno():
    """Menu modular para gestão de Alunos: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Aluno")
    app.state('zoomed')

    ctk.CTkLabel(app, text="GESTÃO DE ALUNO", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="1. Cadastrar Aluno", font=fonte_botoes, width=300, command=tela_cadastrar_aluno).pack(pady=10)
    ctk.CTkButton(app, text="2. Apagar Aluno", font=fonte_botoes, width=300, command=tela_excluir_aluno).pack(pady=10)
    ctk.CTkButton(app, text="3. Listar Alunos", font=fonte_botoes, width=300, command=tela_listar_alunos).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_coordenador).pack(pady=30)

def tela_gestao_curso():
    """Menu modular para gestão de Cursos: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Curso")
    app.state('zoomed')

    ctk.CTkLabel(app, text="GESTÃO DE CURSO", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="1. Cadastrar Curso", font=fonte_botoes, width=300, command=tela_cadastrar_curso).pack(pady=10)
    ctk.CTkButton(app, text="2. Apagar Curso", font=fonte_botoes, width=300, command=tela_excluir_curso).pack(pady=10)
    ctk.CTkButton(app, text="3. Listar Cursos", font=fonte_botoes, width=300, command=tela_listar_cursos).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_coordenador).pack(pady=30)

def tela_gestao_turma():
    """Menu modular para gestão de Turmas: Cadastrar, Apagar, Listar."""
    limpar_tela()
    app.title("Coordenador - Gestão de Turma")
    app.state('zoomed')

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
    ctk.CTkLabel(app, text="Escolha um tema para continuar:", font=fonte_subtitulo).pack(pady=5)

    # Botões de navegação para as telas de Gestão Modular
    ctk.CTkButton(app, text="Professor", font=fonte_botoes, width=300, command=tela_gestao_professor).pack(pady=10) 
    ctk.CTkButton(app, text="Aluno", font=fonte_botoes, width=300, command=tela_gestao_aluno).pack(pady=10)
    ctk.CTkButton(app, text="Curso", font=fonte_botoes, width=300, command=tela_gestao_curso).pack(pady=10)
    ctk.CTkButton(app, text="Turma", font=fonte_botoes, width=300, command=tela_gestao_turma).pack(pady=10)
    ctk.CTkButton(app, text="Perfis Logados", font=fonte_botoes, width=300, command=tela_perfis_logados, fg_color="#9C27B0", hover_color="#7B1FA2").pack(pady=10)
    ctk.CTkButton(app, text="📖 Manual do Sistema", font=fonte_botoes, width=300, command=tela_manual_sistema, fg_color="#607D8B", hover_color="#455A64").pack(pady=10)
    
    # Botão de Sair/Logout
    ctk.CTkButton(app, text="Sair (Logout)", font=fonte_botoes, width=300, command=reiniciar_login).pack(pady=30)


# --- TELAS DE CADASTRO (Acessadas pelos menus de gestão) ---

def tela_cadastrar_professor():
    """Desenha a tela para cadastro de Professor."""
    global professor_nome_entry, professor_email_entry, professor_senha_entry, professor_status_label
    
    limpar_tela()
    app.title("Coordenador - Cadastrar Professor")
    app.state('zoomed')

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
    app.state('zoomed')

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
    app.state('zoomed')

    ctk.CTkLabel(app, text="Cadastrar Novo Curso", font=fonte_titulo).pack(pady=30)
    
    # Inputs de Dados
    ctk.CTkEntry(app, placeholder_text="Nome do Curso", font=fonte_campos, width=350).pack(pady=5)
    # Textbox para a descrição
    textbox_descricao = ctk.CTkTextbox(app, width=350, height=100, font=fonte_campos)
    textbox_descricao.insert("0.0", "Descrição do Curso")
    textbox_descricao.pack(pady=5)
    
    ctk.CTkButton(app, text="Salvar Cadastro (Simulação)", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar à Gestão de Curso", font=fonte_botoes, width=250, command=tela_gestao_curso).pack(pady=20)


def tela_cadastrar_turma():
    """Desenha a tela para cadastro de Turma."""
    limpar_tela()
    app.title("Coordenador - Cadastrar Turma")
    app.state('zoomed')

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
    app.state('zoomed')
    ctk.CTkLabel(app, text="Matricular Aluno em Turma", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="E-mail do Aluno (@aluno.educa)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Nome da Turma", font=fonte_campos, width=350).pack(pady=5)
    
    ctk.CTkButton(app, text="Confirmar Matrícula (Simulação)", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=250, command=tela_coordenador).pack(pady=20)


# --- TELAS DE EXCLUSÃO ---

def tela_excluir_professor():
    """Desenha a tela para exclusão de Professor com pesquisa e lista."""
    global professor_exclusao_status_label, professor_selecionado, funcao_atualizar_lista_atual
    
    limpar_tela()
    app.title("Coordenador - Apagar Professor")
    app.update_idletasks()
    app.state('zoomed')
    
    professor_selecionado = None

    ctk.CTkLabel(app, text="Apagar Professor", font=fonte_titulo).pack(pady=20)
    ctk.CTkLabel(app, text="Atenção: A exclusão é permanente.", font=fonte_campos, text_color="orange").pack(pady=5)

    # Frame para pesquisa
    pesquisa_frame = ctk.CTkFrame(app, fg_color="transparent")
    pesquisa_frame.pack(pady=10, padx=20, fill="x")
    
    ctk.CTkLabel(pesquisa_frame, text="Pesquisar:", font=fonte_campos).pack(side="left", padx=(0, 10))
    pesquisa_entry = ctk.CTkEntry(pesquisa_frame, placeholder_text="Digite nome ou e-mail...", font=fonte_campos, width=400)
    pesquisa_entry.pack(side="left", fill="x", expand=True)
    
    # Frame para lista scrollable
    lista_frame = ctk.CTkScrollableFrame(app, width=600, height=350)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Variável para armazenar os botões da lista
    botoes_lista = []
    
    def atualizar_lista():
        """Atualiza a lista de professores baseado na pesquisa."""
        global professor_selecionado
        # Limpa lista anterior
        for widget in lista_frame.winfo_children():
            widget.destroy()
        botoes_lista.clear()
        
        # Reseta seleção se o item foi removido
        if professor_selecionado:
            # Verifica se o professor selecionado ainda existe
            existe = any(p["email"] == professor_selecionado["email"] for p in DADOS_PROFESSORES)
            if not existe:
                professor_selecionado = None
        
        # Filtra dados
        termo_pesquisa = pesquisa_entry.get().strip().lower()
        if termo_pesquisa:
            dados_filtrados = [p for p in DADOS_PROFESSORES 
                             if termo_pesquisa in p["nome"].lower() or termo_pesquisa in p["email"].lower()]
        else:
            dados_filtrados = DADOS_PROFESSORES
        
        # Cores para efeito xadrez (adaptáveis ao modo)
        cor_par, cor_impar = obter_cores_xadrez()
        
        # Cria botões para cada item
        for idx, prof in enumerate(dados_filtrados):
            # Verifica se é o item selecionado (comparando email)
            is_selected = professor_selecionado and professor_selecionado.get("email") == prof.get("email")
            
            item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
            if is_selected:
                item_frame.configure(fg_color="#1f538d")
            else:
                # Aplica efeito xadrez apenas se não estiver selecionado
                if idx % 2 == 0:
                    item_frame.configure(fg_color=cor_par)
                else:
                    item_frame.configure(fg_color=cor_impar)
            item_frame.pack(fill="x", pady=2, padx=5)
            
            texto_item = f"ID: {prof['id']} | {prof['nome']} | {prof['email']}"
            item_label = ctk.CTkLabel(item_frame, text=texto_item, font=fonte_campos, anchor="w")
            item_label.pack(side="left", padx=10, fill="x", expand=True)
            
            def selecionar_professor(professor=prof):
                global professor_selecionado
                professor_selecionado = professor
                # Atualiza todos os itens: destaca o selecionado e mostra/esconde botões
                for btn in botoes_lista:
                    if btn["professor"].get("email") == professor.get("email"):
                        # Item selecionado: destaca e esconde o botão
                        btn["frame"].configure(fg_color="#1f538d")
                        try:
                            btn["button"].pack_forget()
                        except:
                            pass
                    else:
                        # Outros itens: restaura cor xadrez e mostra o botão
                        idx_original = dados_filtrados.index(btn["professor"])
                        if idx_original % 2 == 0:
                            btn["frame"].configure(fg_color=cor_par)
                        else:
                            btn["frame"].configure(fg_color=cor_impar)
                        # Mostra o botão novamente se estava escondido
                        try:
                            btn["button"].pack_info()
                        except:
                            # Botão não está empacotado, então empacota
                            btn["button"].pack(side="right", padx=0, pady=0)
                professor_exclusao_status_label.configure(
                    text=f"Selecionado: {professor['nome']} ({professor['email']})", 
                    text_color="green"
                )
            
            selecionar_btn = ctk.CTkButton(
                item_frame, 
                text="Selecionar", 
                font=fonte_botoes, 
                width=100,
                border_width=0,
                corner_radius=8,
                command=selecionar_professor
            )
            # Se já está selecionado, não mostra o botão
            if not is_selected:
                selecionar_btn.pack(side="right", padx=0, pady=0)
            
            botoes_lista.append({"frame": item_frame, "professor": prof, "button": selecionar_btn, "index": idx})
    
    # Registra a função de atualização globalmente para atualização quando o modo muda
    funcao_atualizar_lista_atual = atualizar_lista
    
    pesquisa_entry.bind("<KeyRelease>", lambda e: atualizar_lista())
    
    # Botão de pesquisar (opcional, pesquisa já funciona em tempo real)
    pesquisar_btn = ctk.CTkButton(
        pesquisa_frame, 
        text="Limpar", 
        font=fonte_botoes, 
        width=100,
        command=lambda: [pesquisa_entry.delete(0, 'end'), atualizar_lista()]
    )
    pesquisar_btn.pack(side="left", padx=(10, 0))
    
    # Carrega lista inicial
    atualizar_lista()
    
    # Rótulo de Status
    professor_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    professor_exclusao_status_label.pack(pady=10)
    
    # Botões de ação
    botoes_frame = ctk.CTkFrame(app, fg_color="transparent")
    botoes_frame.pack(pady=10)
    
    def confirmar_exclusao():
        global professor_selecionado
        if professor_selecionado:
            if professor_selecionado["email"] == login_professor:
                professor_exclusao_status_label.configure(
                    text="Erro: Professor com vínculos. Não pode ser excluído.", 
                    text_color="orange"
                )
                return
            email_remover = professor_selecionado["email"]
            simular_exclusao_sucesso(
                email_remover, 
                "Professor", 
                pesquisa_entry, 
                professor_exclusao_status_label
            )
            professor_selecionado = None
            atualizar_lista()
        else:
            professor_exclusao_status_label.configure(
                text="Erro: Selecione um professor para excluir.", 
                text_color="red"
            )
    
    ctk.CTkButton(
        botoes_frame, 
        text="APAGAR PERMANENTEMENTE", 
        font=fonte_botoes, 
        width=250, 
        fg_color="red", 
        hover_color="#B00000", 
        command=confirmar_exclusao
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        botoes_frame, 
        text="<< Voltar à Gestão de Professor", 
        font=fonte_botoes, 
        width=250, 
        command=tela_gestao_professor
    ).pack(side="left", padx=10)


def tela_excluir_aluno():
    """Desenha a tela para exclusão de Aluno com pesquisa e lista."""
    global aluno_exclusao_status_label, aluno_selecionado, funcao_atualizar_lista_atual
    
    limpar_tela()
    app.title("Coordenador - Apagar Aluno")
    app.update_idletasks()
    app.state('zoomed')
    
    aluno_selecionado = None

    ctk.CTkLabel(app, text="Apagar Aluno", font=fonte_titulo).pack(pady=20)
    ctk.CTkLabel(app, text="Atenção: A exclusão é permanente.", font=fonte_campos, text_color="orange").pack(pady=5)

    # Frame para pesquisa
    pesquisa_frame = ctk.CTkFrame(app, fg_color="transparent")
    pesquisa_frame.pack(pady=10, padx=20, fill="x")
    
    ctk.CTkLabel(pesquisa_frame, text="Pesquisar:", font=fonte_campos).pack(side="left", padx=(0, 10))
    pesquisa_entry = ctk.CTkEntry(pesquisa_frame, placeholder_text="Digite nome, matrícula ou e-mail...", font=fonte_campos, width=400)
    pesquisa_entry.pack(side="left", fill="x", expand=True)
    
    # Frame para lista scrollable
    lista_frame = ctk.CTkScrollableFrame(app, width=600, height=350)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Variável para armazenar os botões da lista
    botoes_lista = []
    
    def atualizar_lista():
        """Atualiza a lista de alunos baseado na pesquisa."""
        global aluno_selecionado
        # Limpa lista anterior
        for widget in lista_frame.winfo_children():
            widget.destroy()
        botoes_lista.clear()
        
        # Reseta seleção se o item foi removido
        if aluno_selecionado:
            existe = any(a["email"] == aluno_selecionado["email"] for a in DADOS_ALUNOS)
            if not existe:
                aluno_selecionado = None
        
        # Filtra dados
        termo_pesquisa = pesquisa_entry.get().strip().lower()
        if termo_pesquisa:
            dados_filtrados = [a for a in DADOS_ALUNOS 
                             if termo_pesquisa in a["nome"].lower() 
                             or termo_pesquisa in a["email"].lower()
                             or termo_pesquisa in a["matricula"].lower()]
        else:
            dados_filtrados = DADOS_ALUNOS
        
        # Cores para efeito xadrez (adaptáveis ao modo)
        cor_par, cor_impar = obter_cores_xadrez()
        
        # Cria botões para cada item
        for idx, aluno in enumerate(dados_filtrados):
            # Verifica se é o item selecionado
            is_selected = aluno_selecionado and aluno_selecionado.get("email") == aluno.get("email")
            
            item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
            if is_selected:
                item_frame.configure(fg_color="#1f538d")
            else:
                # Aplica efeito xadrez apenas se não estiver selecionado
                if idx % 2 == 0:
                    item_frame.configure(fg_color=cor_par)
                else:
                    item_frame.configure(fg_color=cor_impar)
            item_frame.pack(fill="x", pady=2, padx=5)
            
            texto_item = f"Mat: {aluno['matricula']} | {aluno['nome']} | {aluno['email']} | Turma: {aluno['turma']}"
            item_label = ctk.CTkLabel(item_frame, text=texto_item, font=fonte_campos, anchor="w")
            item_label.pack(side="left", padx=10, fill="x", expand=True)
            
            def selecionar_aluno(aluno_item=aluno):
                global aluno_selecionado
                aluno_selecionado = aluno_item
                # Atualiza todos os itens: destaca o selecionado e mostra/esconde botões
                for btn in botoes_lista:
                    if btn["aluno"].get("email") == aluno_item.get("email"):
                        # Item selecionado: destaca e esconde o botão
                        btn["frame"].configure(fg_color="#1f538d")
                        try:
                            btn["button"].pack_forget()
                        except:
                            pass
                    else:
                        # Outros itens: restaura cor xadrez e mostra o botão
                        idx_original = dados_filtrados.index(btn["aluno"])
                        if idx_original % 2 == 0:
                            btn["frame"].configure(fg_color=cor_par)
                        else:
                            btn["frame"].configure(fg_color=cor_impar)
                        # Mostra o botão novamente se estava escondido
                        try:
                            btn["button"].pack_info()
                        except:
                            # Botão não está empacotado, então empacota
                            btn["button"].pack(side="right", padx=0, pady=0)
                aluno_exclusao_status_label.configure(
                    text=f"Selecionado: {aluno_item['nome']} ({aluno_item['email']})", 
                    text_color="green"
                )
            
            selecionar_btn = ctk.CTkButton(
                item_frame, 
                text="Selecionar", 
                font=fonte_botoes, 
                width=100,
                border_width=0,
                corner_radius=8,
                command=selecionar_aluno
            )
            # Se já está selecionado, não mostra o botão
            if not is_selected:
                selecionar_btn.pack(side="right", padx=0, pady=0)
            
            botoes_lista.append({"frame": item_frame, "aluno": aluno, "button": selecionar_btn, "index": idx})
    
    # Registra a função de atualização globalmente para atualização quando o modo muda
    funcao_atualizar_lista_atual = atualizar_lista
    
    pesquisa_entry.bind("<KeyRelease>", lambda e: atualizar_lista())
    
    # Botão de limpar pesquisa
    limpar_btn = ctk.CTkButton(
        pesquisa_frame, 
        text="Limpar", 
        font=fonte_botoes, 
        width=100,
        command=lambda: [pesquisa_entry.delete(0, 'end'), atualizar_lista()]
    )
    limpar_btn.pack(side="left", padx=(10, 0))
    
    # Carrega lista inicial
    atualizar_lista()
    
    # Rótulo de Status
    aluno_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    aluno_exclusao_status_label.pack(pady=10)
    
    # Botões de ação
    botoes_frame = ctk.CTkFrame(app, fg_color="transparent")
    botoes_frame.pack(pady=10)
    
    def confirmar_exclusao():
        global aluno_selecionado
        if aluno_selecionado:
            simular_exclusao_sucesso(
                aluno_selecionado["email"], 
                "Aluno", 
                pesquisa_entry, 
                aluno_exclusao_status_label
            )
            aluno_selecionado = None
            atualizar_lista()
        else:
            aluno_exclusao_status_label.configure(
                text="Erro: Selecione um aluno para excluir.", 
                text_color="red"
            )
    
    ctk.CTkButton(
        botoes_frame, 
        text="APAGAR PERMANENTEMENTE", 
        font=fonte_botoes, 
        width=250, 
        fg_color="red", 
        hover_color="#B00000", 
        command=confirmar_exclusao
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        botoes_frame, 
        text="<< Voltar à Gestão de Aluno", 
        font=fonte_botoes, 
        width=250, 
        command=tela_gestao_aluno
    ).pack(side="left", padx=10)


def tela_excluir_curso():
    """Desenha a tela para exclusão de Curso com pesquisa e lista."""
    global curso_exclusao_status_label, curso_selecionado, funcao_atualizar_lista_atual
    
    limpar_tela()
    app.title("Coordenador - Apagar Curso")
    app.update_idletasks()
    app.state('zoomed')
    
    curso_selecionado = None

    ctk.CTkLabel(app, text="Apagar Curso", font=fonte_titulo).pack(pady=20)
    ctk.CTkLabel(app, text="Atenção: Cursos com turmas ativas não podem ser apagados.", font=fonte_campos, text_color="orange").pack(pady=5)

    # Frame para pesquisa
    pesquisa_frame = ctk.CTkFrame(app, fg_color="transparent")
    pesquisa_frame.pack(pady=10, padx=20, fill="x")
    
    ctk.CTkLabel(pesquisa_frame, text="Pesquisar:", font=fonte_campos).pack(side="left", padx=(0, 10))
    pesquisa_entry = ctk.CTkEntry(pesquisa_frame, placeholder_text="Digite o nome do curso...", font=fonte_campos, width=400)
    pesquisa_entry.pack(side="left", fill="x", expand=True)
    
    # Frame para lista scrollable
    lista_frame = ctk.CTkScrollableFrame(app, width=600, height=350)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Variável para armazenar os botões da lista
    botoes_lista = []
    
    def atualizar_lista():
        """Atualiza a lista de cursos baseado na pesquisa."""
        global curso_selecionado
        # Limpa lista anterior
        for widget in lista_frame.winfo_children():
            widget.destroy()
        botoes_lista.clear()
        
        # Reseta seleção se o item foi removido
        if curso_selecionado:
            existe = any(c["nome"] == curso_selecionado["nome"] for c in DADOS_CURSOS)
            if not existe:
                curso_selecionado = None
        
        # Filtra dados
        termo_pesquisa = pesquisa_entry.get().strip().lower()
        if termo_pesquisa:
            dados_filtrados = [c for c in DADOS_CURSOS 
                             if termo_pesquisa in c["nome"].lower()]
        else:
            dados_filtrados = DADOS_CURSOS
        
        # Cores para efeito xadrez (adaptáveis ao modo)
        cor_par, cor_impar = obter_cores_xadrez()
        
        # Cria botões para cada item
        for idx, curso in enumerate(dados_filtrados):
            # Verifica se é o item selecionado
            is_selected = curso_selecionado and curso_selecionado.get("nome") == curso.get("nome")
            
            item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
            if is_selected:
                item_frame.configure(fg_color="#1f538d")
            else:
                # Aplica efeito xadrez apenas se não estiver selecionado
                if idx % 2 == 0:
                    item_frame.configure(fg_color=cor_par)
                else:
                    item_frame.configure(fg_color=cor_impar)
            item_frame.pack(fill="x", pady=2, padx=5)
            
            texto_item = f"ID: {curso['id']} | {curso['nome']}"
            item_label = ctk.CTkLabel(item_frame, text=texto_item, font=fonte_campos, anchor="w")
            item_label.pack(side="left", padx=10, fill="x", expand=True)
            
            def selecionar_curso(curso_item=curso):
                global curso_selecionado
                curso_selecionado = curso_item
                # Atualiza todos os itens: destaca o selecionado e mostra/esconde botões
                for btn in botoes_lista:
                    if btn["curso"].get("nome") == curso_item.get("nome"):
                        # Item selecionado: destaca e esconde o botão
                        btn["frame"].configure(fg_color="#1f538d")
                        try:
                            btn["button"].pack_forget()
                        except:
                            pass
                    else:
                        # Outros itens: restaura cor xadrez e mostra o botão
                        idx_original = dados_filtrados.index(btn["curso"])
                        if idx_original % 2 == 0:
                            btn["frame"].configure(fg_color=cor_par)
                        else:
                            btn["frame"].configure(fg_color=cor_impar)
                        # Mostra o botão novamente se estava escondido
                        try:
                            btn["button"].pack_info()
                        except:
                            # Botão não está empacotado, então empacota
                            btn["button"].pack(side="right", padx=0, pady=0)
                curso_exclusao_status_label.configure(
                    text=f"Selecionado: {curso_item['nome']}", 
                    text_color="green"
                )
            
            selecionar_btn = ctk.CTkButton(
                item_frame, 
                text="Selecionar", 
                font=fonte_botoes, 
                width=100,
                border_width=0,
                corner_radius=8,
                command=selecionar_curso
            )
            # Se já está selecionado, não mostra o botão
            if not is_selected:
                selecionar_btn.pack(side="right", padx=0, pady=0)
            
            botoes_lista.append({"frame": item_frame, "curso": curso, "button": selecionar_btn, "index": idx})
    
    # Registra a função de atualização globalmente para atualização quando o modo muda
    funcao_atualizar_lista_atual = atualizar_lista
    
    pesquisa_entry.bind("<KeyRelease>", lambda e: atualizar_lista())
    
    # Botão de limpar pesquisa
    limpar_btn = ctk.CTkButton(
        pesquisa_frame, 
        text="Limpar", 
        font=fonte_botoes, 
        width=100,
        command=lambda: [pesquisa_entry.delete(0, 'end'), atualizar_lista()]
    )
    limpar_btn.pack(side="left", padx=(10, 0))
    
    # Carrega lista inicial
    atualizar_lista()
    
    # Rótulo de Status
    curso_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    curso_exclusao_status_label.pack(pady=10)
    
    # Botões de ação
    botoes_frame = ctk.CTkFrame(app, fg_color="transparent")
    botoes_frame.pack(pady=10)
    
    def confirmar_exclusao():
        global curso_selecionado
        if curso_selecionado:
            # Verifica se há turmas associadas
            turmas_do_curso = [t for t in DADOS_TURMAS if t["curso"] == curso_selecionado["nome"]]
            if turmas_do_curso:
                curso_exclusao_status_label.configure(
                    text=f"Erro: Curso possui {len(turmas_do_curso)} turma(s) ativa(s). Não pode ser excluído.", 
                    text_color="orange"
                )
                return
            simular_exclusao_sucesso(
                curso_selecionado["nome"], 
                "Curso", 
                pesquisa_entry, 
                curso_exclusao_status_label
            )
            curso_selecionado = None
            atualizar_lista()
        else:
            curso_exclusao_status_label.configure(
                text="Erro: Selecione um curso para excluir.", 
                text_color="red"
            )
    
    ctk.CTkButton(
        botoes_frame, 
        text="APAGAR PERMANENTEMENTE", 
        font=fonte_botoes, 
        width=250, 
        fg_color="red", 
        hover_color="#B00000", 
        command=confirmar_exclusao
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        botoes_frame, 
        text="<< Voltar à Gestão de Curso", 
        font=fonte_botoes, 
        width=250, 
        command=tela_gestao_curso
    ).pack(side="left", padx=10)


def tela_excluir_turma():
    """Desenha a tela para exclusão de Turma com pesquisa e lista."""
    global turma_exclusao_status_label, turma_selecionada, funcao_atualizar_lista_atual
    
    limpar_tela()
    app.title("Coordenador - Apagar Turma")
    app.update_idletasks()
    app.state('zoomed')
    
    turma_selecionada = None

    ctk.CTkLabel(app, text="Apagar Turma", font=fonte_titulo).pack(pady=20)
    ctk.CTkLabel(app, text="Atenção: Turmas com alunos matriculados não podem ser apagadas.", font=fonte_campos, text_color="orange").pack(pady=5)

    # Frame para pesquisa
    pesquisa_frame = ctk.CTkFrame(app, fg_color="transparent")
    pesquisa_frame.pack(pady=10, padx=20, fill="x")
    
    ctk.CTkLabel(pesquisa_frame, text="Pesquisar:", font=fonte_campos).pack(side="left", padx=(0, 10))
    pesquisa_entry = ctk.CTkEntry(pesquisa_frame, placeholder_text="Digite nome da turma ou curso...", font=fonte_campos, width=400)
    pesquisa_entry.pack(side="left", fill="x", expand=True)
    
    # Frame para lista scrollable
    lista_frame = ctk.CTkScrollableFrame(app, width=600, height=350)
    lista_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Variável para armazenar os botões da lista
    botoes_lista = []
    
    def atualizar_lista():
        """Atualiza a lista de turmas baseado na pesquisa."""
        global turma_selecionada
        # Limpa lista anterior
        for widget in lista_frame.winfo_children():
            widget.destroy()
        botoes_lista.clear()
        
        # Reseta seleção se o item foi removido
        if turma_selecionada:
            existe = any(t["nome"] == turma_selecionada["nome"] for t in DADOS_TURMAS)
            if not existe:
                turma_selecionada = None
        
        # Filtra dados
        termo_pesquisa = pesquisa_entry.get().strip().lower()
        if termo_pesquisa:
            dados_filtrados = [t for t in DADOS_TURMAS 
                             if termo_pesquisa in t["nome"].lower() 
                             or termo_pesquisa in t["curso"].lower()]
        else:
            dados_filtrados = DADOS_TURMAS
        
        # Cores para efeito xadrez (adaptáveis ao modo)
        cor_par, cor_impar = obter_cores_xadrez()
        
        # Cria botões para cada item
        for idx, turma in enumerate(dados_filtrados):
            # Verifica se é o item selecionado
            is_selected = turma_selecionada and turma_selecionada.get("nome") == turma.get("nome")
            
            item_frame = ctk.CTkFrame(lista_frame, border_width=0, corner_radius=8)
            if is_selected:
                item_frame.configure(fg_color="#1f538d")
            else:
                # Aplica efeito xadrez apenas se não estiver selecionado
                if idx % 2 == 0:
                    item_frame.configure(fg_color=cor_par)
                else:
                    item_frame.configure(fg_color=cor_impar)
            item_frame.pack(fill="x", pady=2, padx=5)
            
            texto_item = f"ID: {turma['id']} | Turma: {turma['nome']} | Curso: {turma['curso']} | Alunos: {turma['alunos']}"
            item_label = ctk.CTkLabel(item_frame, text=texto_item, font=fonte_campos, anchor="w")
            item_label.pack(side="left", padx=10, fill="x", expand=True)
            
            def selecionar_turma(turma_item=turma):
                global turma_selecionada
                turma_selecionada = turma_item
                # Atualiza todos os itens: destaca o selecionado e mostra/esconde botões
                for btn in botoes_lista:
                    if btn["turma"].get("nome") == turma_item.get("nome"):
                        # Item selecionado: destaca e esconde o botão
                        btn["frame"].configure(fg_color="#1f538d")
                        try:
                            btn["button"].pack_forget()
                        except:
                            pass
                    else:
                        # Outros itens: restaura cor xadrez e mostra o botão
                        idx_original = dados_filtrados.index(btn["turma"])
                        if idx_original % 2 == 0:
                            btn["frame"].configure(fg_color=cor_par)
                        else:
                            btn["frame"].configure(fg_color=cor_impar)
                        # Mostra o botão novamente se estava escondido
                        try:
                            btn["button"].pack_info()
                        except:
                            # Botão não está empacotado, então empacota
                            btn["button"].pack(side="right", padx=0, pady=0)
                turma_exclusao_status_label.configure(
                    text=f"Selecionado: {turma_item['nome']} ({turma_item['curso']})", 
                    text_color="green"
                )
            
            selecionar_btn = ctk.CTkButton(
                item_frame, 
                text="Selecionar", 
                font=fonte_botoes, 
                width=100,
                border_width=0,
                corner_radius=8,
                command=selecionar_turma
            )
            # Se já está selecionado, não mostra o botão
            if not is_selected:
                selecionar_btn.pack(side="right", padx=0, pady=0)
            
            botoes_lista.append({"frame": item_frame, "turma": turma, "button": selecionar_btn, "index": idx})
    
    # Registra a função de atualização globalmente para atualização quando o modo muda
    funcao_atualizar_lista_atual = atualizar_lista
    
    pesquisa_entry.bind("<KeyRelease>", lambda e: atualizar_lista())
    
    # Botão de limpar pesquisa
    limpar_btn = ctk.CTkButton(
        pesquisa_frame, 
        text="Limpar", 
        font=fonte_botoes, 
        width=100,
        command=lambda: [pesquisa_entry.delete(0, 'end'), atualizar_lista()]
    )
    limpar_btn.pack(side="left", padx=(10, 0))
    
    # Carrega lista inicial
    atualizar_lista()
    
    # Rótulo de Status
    turma_exclusao_status_label = ctk.CTkLabel(app, text="", font=fonte_campos, text_color=TEMA_TEXT_COLOR)
    turma_exclusao_status_label.pack(pady=10)
    
    # Botões de ação
    botoes_frame = ctk.CTkFrame(app, fg_color="transparent")
    botoes_frame.pack(pady=10)
    
    def confirmar_exclusao():
        global turma_selecionada
        if turma_selecionada:
            # Verifica se há alunos matriculados
            if turma_selecionada["alunos"] > 0:
                turma_exclusao_status_label.configure(
                    text=f"Erro: Turma possui {turma_selecionada['alunos']} aluno(s) matriculado(s). Não pode ser excluída.", 
                    text_color="orange"
                )
                return
            simular_exclusao_sucesso(
                turma_selecionada["nome"], 
                "Turma", 
                pesquisa_entry, 
                turma_exclusao_status_label
            )
            turma_selecionada = None
            atualizar_lista()
        else:
            turma_exclusao_status_label.configure(
                text="Erro: Selecione uma turma para excluir.", 
                text_color="red"
            )
    
    ctk.CTkButton(
        botoes_frame, 
        text="APAGAR PERMANENTEMENTE", 
        font=fonte_botoes, 
        width=250, 
        fg_color="red", 
        hover_color="#B00000", 
        command=confirmar_exclusao
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        botoes_frame, 
        text="<< Voltar à Gestão de Turma", 
        font=fonte_botoes, 
        width=250, 
        command=tela_gestao_turma
    ).pack(side="left", padx=10)


# =========================================================
# REGIÃO: GERENCIAMENTO DE TELAS - MÓDULO PROFESSOR
# =========================================================

# --- Telas de Gestão (Subtemas) para Professor ---

def tela_gestao_turmas_prof():
    """Menu de gestão de Turmas para Professor."""
    limpar_tela()
    app.title("Professor - Gestão de Turmas")
    app.state('zoomed')

    ctk.CTkLabel(app, text="GESTÃO DE TURMAS", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Visualizar Turmas", font=fonte_botoes, width=300, command=tela_visualizar_turmas).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_professor).pack(pady=30)

def tela_gestao_atividades_prof():
    """Menu de gestão de Atividades para Professor."""
    limpar_tela()
    app.title("Professor - Gestão de Atividades")
    app.state('zoomed')

    ctk.CTkLabel(app, text="GESTÃO DE ATIVIDADES", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Postar Atividades", font=fonte_botoes, width=300, command=tela_postar_atividades).pack(pady=10)
    ctk.CTkButton(app, text="Visualizar Atividades", font=fonte_botoes, width=300, command=tela_visualizar_atividades_prof).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_professor).pack(pady=30)

def tela_gestao_notas_prof():
    """Menu de gestão de Notas para Professor."""
    limpar_tela()
    app.title("Professor - Gestão de Notas")
    app.state('zoomed')

    ctk.CTkLabel(app, text="GESTÃO DE NOTAS", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Lançar Notas", font=fonte_botoes, width=300, command=tela_lancar_notas).pack(pady=10)
    ctk.CTkButton(app, text="Visualizar Notas", font=fonte_botoes, width=300, command=tela_visualizar_notas_prof).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_professor).pack(pady=30)

def tela_gestao_frequencia_prof():
    """Menu de gestão de Frequência para Professor."""
    limpar_tela()
    app.title("Professor - Gestão de Frequência")
    app.state('zoomed')

    ctk.CTkLabel(app, text="GESTÃO DE FREQUÊNCIA", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Lançar Frequência", font=fonte_botoes, width=300, command=tela_lancar_frequencia).pack(pady=10)
    ctk.CTkButton(app, text="Visualizar Frequência", font=fonte_botoes, width=300, command=tela_visualizar_frequencia_prof).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_professor).pack(pady=30)

def tela_gestao_comunicacao_prof():
    """Menu de gestão de Comunicação para Professor."""
    limpar_tela()
    app.title("Professor - Comunicação")
    app.state('zoomed')

    ctk.CTkLabel(app, text="COMUNICAÇÃO", font=fonte_titulo).pack(pady=30)

    ctk.CTkButton(app, text="Chat com Alunos", font=fonte_botoes, width=300, command=tela_chat_alunos_prof).pack(pady=10)
    
    ctk.CTkButton(app, text="<< Voltar ao Menu Principal", font=fonte_botoes, width=300, command=tela_professor).pack(pady=30)

# --- Telas Específicas do Professor ---

def tela_visualizar_turmas():
    """Desenha a tela de visualização de Turmas atribuídas."""
    limpar_tela()
    app.title("Professor - Visualizar Turmas")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Visualizar Turmas Atribuídas", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a lista de turmas.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar à Gestão de Turmas", font=fonte_botoes, width=300, command=tela_gestao_turmas_prof).pack(pady=30)

def tela_postar_atividades():
    """Desenha a tela para postagem de Atividades."""
    limpar_tela()
    app.title("Professor - Postar Atividades")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Postar Nova Atividade", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Título da Atividade", font=fonte_campos, width=350).pack(pady=5)
    textbox_atividade = ctk.CTkTextbox(app, width=350, height=100, font=fonte_campos)
    textbox_atividade.insert("0.0", "Descrição da Atividade")
    textbox_atividade.pack(pady=5)
    ctk.CTkButton(app, text="Postar (Simulação)", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Atividades", font=fonte_botoes, width=300, command=tela_gestao_atividades_prof).pack(pady=30)

def tela_lancar_notas():
    """Desenha a tela para lançamento de Notas."""
    limpar_tela()
    app.title("Professor - Lançar Notas")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Lançar Notas", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Nome do Aluno", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Nota (0-10)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkButton(app, text="Lançar (Simulação)", font=fonte_botoes, width=250).pack(pady=15)

    ctk.CTkButton(app, text="<< Voltar à Gestão de Notas", font=fonte_botoes, width=300, command=tela_gestao_notas_prof).pack(pady=30)

def tela_lancar_frequencia():
    """Desenha a tela para lançamento de Frequência."""
    limpar_tela()
    app.title("Professor - Lançar Frequência")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Lançar Frequência", font=fonte_titulo).pack(pady=30)
    
    ctk.CTkEntry(app, placeholder_text="Nome do Aluno", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkEntry(app, placeholder_text="Frequência (P/F)", font=fonte_campos, width=350).pack(pady=5)
    ctk.CTkButton(app, text="Lançar (Simulação)", font=fonte_botoes, width=250).pack(pady=15)
    
    ctk.CTkButton(app, text="<< Voltar à Gestão de Frequência", font=fonte_botoes, width=300, command=tela_gestao_frequencia_prof).pack(pady=30)

def tela_visualizar_atividades_prof():
    """Desenha a tela de visualização de Atividades postadas."""
    limpar_tela()
    app.title("Professor - Visualizar Atividades")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Atividades Postadas", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a lista das suas atividades postadas.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar à Gestão de Atividades", font=fonte_botoes, width=300, command=tela_gestao_atividades_prof).pack(pady=30)

def tela_visualizar_notas_prof():
    """Desenha a tela de visualização de Notas lançadas."""
    limpar_tela()
    app.title("Professor - Visualizar Notas")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Notas Lançadas", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a visualização das notas por turma.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar à Gestão de Notas", font=fonte_botoes, width=300, command=tela_gestao_notas_prof).pack(pady=30)

def tela_visualizar_frequencia_prof():
    """Desenha a tela de visualização de Frequência lançada."""
    limpar_tela()
    app.title("Professor - Visualizar Frequência")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Frequência Lançada", font=fonte_titulo).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui seria a visualização da frequência por turma.", font=fonte_campos).pack(pady=10)
    ctk.CTkButton(app, text="<< Voltar à Gestão de Frequência", font=fonte_botoes, width=300, command=tela_gestao_frequencia_prof).pack(pady=30)

def encerrar_chat_e_voltar():
    """Salva o histórico e volta ao menu principal."""
    save_chat_history(MENSAGENS_CHAT)
    voltar_ao_menu_principal()

def tela_chat_alunos_prof():
    """Desenha a tela de chat para o Professor interagir com os Alunos."""
    global MENSAGENS_CHAT, chat_history_box
    
    # Garantir que MENSAGENS_CHAT está carregado
    if not MENSAGENS_CHAT:
        MENSAGENS_CHAT = load_chat_history()
    
    limpar_tela()
    app.title("Professor - Chat com Alunos")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Chat Global", font=fonte_titulo).pack(pady=10)

    # Determina a cor da borda baseada no tema atual
    current_mode = ctk.get_appearance_mode()
    border_color = BTN_BORDER_COLOR_DARK if current_mode == "Dark" else BTN_BORDER_COLOR_LIGHT

    # Textbox para histórico de mensagens (readonly) com borda
    chat_history_box = ctk.CTkTextbox(
        app, 
        width=500, 
        height=450, 
        font=fonte_campos, 
        state="disabled",
        border_width=2,
        border_color=border_color
    )
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
    
    def limpar_chat():
        """Limpa o histórico do chat e atualiza a interface."""
        limpar_historico_chat()
        atualizar_historico()
    
    ctk.CTkButton(
        input_frame, 
        text="Limpar Chat", 
        font=fonte_botoes, 
        width=120, 
        command=limpar_chat, 
        fg_color="#F44336", 
        hover_color="#D32F2F"
    ).pack(side="left", padx=(0, 10))
    
    def voltar_comunicacao():
        save_chat_history(MENSAGENS_CHAT)
        tela_gestao_comunicacao_prof()
    
    ctk.CTkButton(
        input_frame, 
        text="Voltar à Comunicação", 
        font=fonte_botoes, 
        width=150, 
        command=voltar_comunicacao, 
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
    global MENSAGENS_CHAT, chat_history_box
    
    # Garantir que MENSAGENS_CHAT está carregado
    if not MENSAGENS_CHAT:
        MENSAGENS_CHAT = load_chat_history()
    
    limpar_tela()
    app.title("Aluno - Chat com Professores")
    app.state('zoomed')
    ctk.CTkLabel(app, text="Chat Global", font=fonte_titulo).pack(pady=10)

    # Determina a cor da borda baseada no tema atual
    current_mode = ctk.get_appearance_mode()
    border_color = BTN_BORDER_COLOR_DARK if current_mode == "Dark" else BTN_BORDER_COLOR_LIGHT

    # Textbox para histórico de mensagens (readonly) com borda
    chat_history_box = ctk.CTkTextbox(
        app, 
        width=500, 
        height=450, 
        font=fonte_campos, 
        state="disabled",
        border_width=2,
        border_color=border_color
    )
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
    
    def limpar_chat():
        """Limpa o histórico do chat e atualiza a interface."""
        limpar_historico_chat()
        atualizar_historico()
    
    ctk.CTkButton(
        input_frame, 
        text="Limpar Chat", 
        font=fonte_botoes, 
        width=120, 
        command=limpar_chat, 
        fg_color="#F44336", 
        hover_color="#D32F2F"
    ).pack(side="left", padx=(0, 10))
    
    def voltar_comunicacao_aluno():
        save_chat_history(MENSAGENS_CHAT)
        tela_gestao_comunicacao_aluno()
    
    ctk.CTkButton(
        input_frame, 
        text="Voltar à Comunicação", 
        font=fonte_botoes, 
        width=150, 
        command=voltar_comunicacao_aluno, 
        fg_color="#4CAF50", 
        hover_color="#388E3C"
    ).pack(side="left", padx=(0, 10))

    chat_input_entry.bind("<Return>", enviar_mensagem)
    
    atualizar_historico()


# =========================================================
# REGIÃO: TELA DE PERFIS LOGADOS (APENAS COORDENADOR)
# =========================================================

def tela_perfis_logados():
    """Tela exclusiva do coordenador para visualizar todos os perfis logados simultaneamente."""
    limpar_tela()
    app.update_idletasks()
    app.state('zoomed')
    app.title("Portal Educa - Coordenador - Perfis Logados")
    
    # Verifica se é coordenador
    if perfil_logado != "Coordenador":
        ctk.CTkLabel(
            app,
            text="Acesso negado. Apenas coordenadores podem acessar esta tela.",
            font=fonte_subtitulo,
            text_color="red"
        ).pack(pady=50)
        ctk.CTkButton(
            app,
            text="Voltar",
            font=fonte_botoes,
            width=200,
            command=tela_coordenador
        ).pack(pady=20)
        return
    
    # Título
    ctk.CTkLabel(
        app,
        text="Perfis Logados no Sistema",
        font=fonte_titulo
    ).pack(pady=20)
    
    # Frame principal com scroll
    main_frame = ctk.CTkScrollableFrame(app, width=1000, height=600)
    main_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Label de status
    status_label = ctk.CTkLabel(
        main_frame,
        text="",
        font=fonte_subtitulo,
        text_color="gray"
    )
    status_label.pack(pady=10)
    
    # Frame para lista de usuários
    usuarios_frame = ctk.CTkFrame(main_frame)
    usuarios_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    def atualizar_lista_usuarios():
        """Atualiza a lista de usuários logados."""
        # Carrega usuários do arquivo compartilhado
        USUARIOS_LOGADOS = get_logged_users()
        
        # Converte timestamps de string para datetime se necessário
        for usuario in USUARIOS_LOGADOS:
            if isinstance(usuario.get('timestamp'), str):
                try:
                    usuario['timestamp'] = datetime.fromisoformat(usuario['timestamp'])
                except:
                    # Se falhar, cria um timestamp atual
                    usuario['timestamp'] = datetime.now()
        
        # Limpa frame de usuários
        for widget in usuarios_frame.winfo_children():
            widget.destroy()
        
        # Atualiza status
        total_usuarios = len(USUARIOS_LOGADOS)
        if total_usuarios == 0:
            status_label.configure(
                text="Nenhum usuário logado no momento",
                text_color="yellow"
            )
            ctk.CTkLabel(
                usuarios_frame,
                text="Não há usuários logados no sistema no momento.",
                font=fonte_campos,
                text_color="gray"
            ).pack(pady=50)
        else:
            status_label.configure(
                text=f"Total de usuários logados: {total_usuarios}",
                text_color="green"
            )
            
            # Cabeçalho da tabela
            header_frame = ctk.CTkFrame(usuarios_frame)
            header_frame.pack(pady=10, padx=10, fill="x")
            
            ctk.CTkLabel(
                header_frame,
                text="E-mail",
                font=fonte_subtitulo,
                width=300
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                header_frame,
                text="Perfil",
                font=fonte_subtitulo,
                width=150
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                header_frame,
                text="Data de Login",
                font=fonte_subtitulo,
                width=120
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                header_frame,
                text="Hora de Login",
                font=fonte_subtitulo,
                width=120
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                header_frame,
                text="Tempo Online",
                font=fonte_subtitulo,
                width=150
            ).pack(side="left", padx=10)
            
            # Lista de usuários
            for i, usuario in enumerate(USUARIOS_LOGADOS):
                # Calcula tempo online
                tempo_online = datetime.now() - usuario["timestamp"]
                horas = tempo_online.seconds // 3600
                minutos = (tempo_online.seconds % 3600) // 60
                segundos = tempo_online.seconds % 60
                tempo_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
                
                # Define cor do perfil
                perfil = usuario["perfil"]
                if perfil == "Coordenador":
                    cor_perfil = "#9C27B0"
                elif perfil == "Professor":
                    cor_perfil = "#2196F3"
                elif perfil == "Aluno":
                    cor_perfil = "#4CAF50"
                else:
                    cor_perfil = "gray"
                
                # Frame para cada usuário
                usuario_frame = ctk.CTkFrame(usuarios_frame)
                usuario_frame.pack(pady=5, padx=10, fill="x")
                
                # E-mail
                ctk.CTkLabel(
                    usuario_frame,
                    text=usuario["email"],
                    font=fonte_campos,
                    width=300,
                    anchor="w"
                ).pack(side="left", padx=10)
                
                # Perfil
                ctk.CTkLabel(
                    usuario_frame,
                    text=perfil,
                    font=fonte_campos,
                    width=150,
                    text_color=cor_perfil,
                    anchor="w"
                ).pack(side="left", padx=10)
                
                # Data
                ctk.CTkLabel(
                    usuario_frame,
                    text=usuario["data_login"],
                    font=fonte_campos,
                    width=120,
                    anchor="w"
                ).pack(side="left", padx=10)
                
                # Hora
                ctk.CTkLabel(
                    usuario_frame,
                    text=usuario["hora_login"],
                    font=fonte_campos,
                    width=120,
                    anchor="w"
                ).pack(side="left", padx=10)
                
                # Tempo online
                ctk.CTkLabel(
                    usuario_frame,
                    text=tempo_str,
                    font=fonte_campos,
                    width=150,
                    text_color="green",
                    anchor="w"
                ).pack(side="left", padx=10)
        
        # Atualiza automaticamente a cada 5 segundos
        app.after(5000, atualizar_lista_usuarios)
    
    # Frame para botões
    botoes_frame = ctk.CTkFrame(main_frame)
    botoes_frame.pack(pady=10, fill="x")
    
    # Botão para atualizar manualmente
    ctk.CTkButton(
        botoes_frame,
        text="Atualizar Lista",
        font=fonte_botoes,
        width=200,
        command=atualizar_lista_usuarios
    ).pack(side="left", padx=10)
    
    # Botão para limpar lista (útil para testes)
    def limpar_lista():
        """Limpa todos os usuários logados."""
        clear_logged_users()
        atualizar_lista_usuarios()
        atualizar_estatisticas()
    
    ctk.CTkButton(
        botoes_frame,
        text="Limpar Lista (Testes)",
        font=fonte_botoes,
        width=200,
        command=limpar_lista,
        fg_color="#F44336",
        hover_color="#D32F2F"
    ).pack(side="left", padx=10)
    
    # Estatísticas
    stats_frame = ctk.CTkFrame(main_frame)
    stats_frame.pack(pady=10, padx=20, fill="x")
    
    def atualizar_estatisticas():
        """Atualiza as estatísticas de usuários logados."""
        # Carrega usuários do arquivo compartilhado
        USUARIOS_LOGADOS = get_logged_users()
        
        # Limpa frame de estatísticas
        for widget in stats_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            stats_frame,
            text="Estatísticas",
            font=fonte_subtitulo
        ).pack(pady=10)
        
        # Conta por perfil
        coordenadores = sum(1 for u in USUARIOS_LOGADOS if u["perfil"] == "Coordenador")
        professores = sum(1 for u in USUARIOS_LOGADOS if u["perfil"] == "Professor")
        alunos = sum(1 for u in USUARIOS_LOGADOS if u["perfil"] == "Aluno")
        
        stats_text = f"Coordenadores: {coordenadores} | Professores: {professores} | Alunos: {alunos}"
        ctk.CTkLabel(
            stats_frame,
            text=stats_text,
            font=fonte_campos
        ).pack(pady=5)
        
        # Atualiza automaticamente
        app.after(5000, atualizar_estatisticas)
    
    atualizar_estatisticas()
    
    # Botão voltar
    ctk.CTkButton(
        main_frame,
        text="<< Voltar ao Menu Principal",
        font=fonte_botoes,
        width=300,
        command=tela_coordenador
    ).pack(pady=20)
    
    # Executa atualização inicial
    atualizar_lista_usuarios()


def limpar_historico_chat():
    """Limpa todo o histórico do chat e atualiza a interface."""
    global MENSAGENS_CHAT, chat_history_box
    MENSAGENS_CHAT = [{"perfil": "Sistema", "texto": "Início da Conversa. Histórico apagado."}]
    save_chat_history(MENSAGENS_CHAT)
    
    # Atualiza a interface se o painel de mensagens existir
    if chat_history_box is not None:
        chat_history_box.configure(state="normal")
        chat_history_box.delete("1.0", "end")
        chat_history_box.insert("end", "[Sistema]: Início da Conversa. Histórico apagado.\n")
        chat_history_box.configure(state="disabled")
        chat_history_box.yview_moveto(1.0)


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