"""
Módulo para gerenciar usuários logados de forma persistente
Permite que múltiplas instâncias do programa compartilhem os mesmos dados
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

LOGGED_USERS_FILE = "logged_users.json"

def load_logged_users() -> List[Dict]:
    """
    Carrega a lista de usuários logados do arquivo.
    
    Returns:
        Lista de dicionários com informações dos usuários logados
    """
    try:
        if os.path.exists(LOGGED_USERS_FILE):
            with open(LOGGED_USERS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Converte timestamps de string para datetime se necessário
                for usuario in data:
                    if isinstance(usuario.get('timestamp'), str):
                        try:
                            usuario['timestamp'] = datetime.fromisoformat(usuario['timestamp'])
                        except:
                            pass
                return data
        return []
    except Exception as e:
        print(f"Erro ao carregar usuários logados: {e}")
        return []


def save_logged_users(usuarios: List[Dict]):
    """
    Salva a lista de usuários logados no arquivo.
    
    Args:
        usuarios: Lista de dicionários com informações dos usuários logados
    """
    try:
        # Converte datetime para string para serialização JSON
        usuarios_serializados = []
        for usuario in usuarios:
            usuario_copy = usuario.copy()
            if isinstance(usuario_copy.get('timestamp'), datetime):
                usuario_copy['timestamp'] = usuario_copy['timestamp'].isoformat()
            usuarios_serializados.append(usuario_copy)
        
        with open(LOGGED_USERS_FILE, 'w', encoding='utf-8') as file:
            json.dump(usuarios_serializados, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar usuários logados: {e}")


def add_logged_user(email: str, perfil: str) -> Dict:
    """
    Adiciona ou atualiza um usuário logado.
    
    Args:
        email: E-mail do usuário
        perfil: Perfil do usuário (Coordenador, Professor, Aluno)
        
    Returns:
        Dicionário com informações do usuário logado
    """
    usuarios = load_logged_users()
    agora = datetime.now()
    
    usuario_logado = {
        "email": email,
        "perfil": perfil,
        "data_login": agora.strftime("%d/%m/%Y"),
        "hora_login": agora.strftime("%H:%M:%S"),
        "timestamp": agora
    }
    
    # Verifica se o usuário já está logado
    usuario_existente = None
    for i, usuario in enumerate(usuarios):
        if usuario["email"] == email:
            usuario_existente = i
            break
    
    if usuario_existente is not None:
        # Atualiza o login existente
        usuarios[usuario_existente] = usuario_logado
    else:
        # Adiciona novo usuário logado
        usuarios.append(usuario_logado)
    
    save_logged_users(usuarios)
    return usuario_logado


def remove_logged_user(email: str):
    """
    Remove um usuário da lista de logados.
    
    Args:
        email: E-mail do usuário a ser removido
    """
    usuarios = load_logged_users()
    usuarios = [u for u in usuarios if u["email"] != email]
    save_logged_users(usuarios)


def get_logged_users() -> List[Dict]:
    """
    Retorna a lista atual de usuários logados.
    
    Returns:
        Lista de dicionários com informações dos usuários logados
    """
    return load_logged_users()


def clear_logged_users():
    """
    Limpa todos os usuários logados (útil para testes ou reset).
    """
    save_logged_users([])

