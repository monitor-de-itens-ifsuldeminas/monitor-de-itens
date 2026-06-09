"""
Serviço de Notificações Push via OneSignal.
Gerencia o disparo de alertas globais para os usuários conectados ao aplicativo.
"""

import os
import requests

ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY")

# FUNÇÃO: Enviar Notificação Global
def enviar_notificacao(titulo: str, mensagem: str) -> None:
    # Validação de Credenciais do Sistema
    if not ONESIGNAL_APP_ID or not ONESIGNAL_API_KEY:
        print(f"[OneSignal] Credenciais não configuradas.")
        print(f"[OneSignal] Título: {titulo}")
        print(f"[OneSignal] Mensagem: {mensagem}")
        return

    # Montagem do Payload para Segmento Global
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "headings": {"pt": titulo, "en": titulo},
        "contents": {"pt": mensagem, "en": mensagem},
    }

    # Cabeçalhos de Autenticação da API Externa
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Key {ONESIGNAL_API_KEY}",
    }

    try:
        # Disparo de Requisição POST com Limite de Tempo de Resposta
        response = requests.post(
            "https://onesignal.com/api/v1/notifications",
            json=payload,
            headers=headers,
            timeout=5,
        )
        # Intercepção de Erros de Status HTTP
        response.raise_for_status()
        print(f"[OneSignal] Notificação enviada: {response.json()}")

    # Tratamento de Exceções de Rede e Integração
    except requests.RequestException as e:
        print(f"[OneSignal] Erro ao enviar notificação: {e}")