import json
import os

CHAT_FILE = "chat_history.json"

def load_chat_history():
    """Carrega o histórico do chat do arquivo."""
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")
        return []

def save_chat_history(messages):
    """Salva o histórico do chat no arquivo."""
    try:
        with open(CHAT_FILE, 'w', encoding='utf-8') as file:
            json.dump(messages, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar histórico: {e}")