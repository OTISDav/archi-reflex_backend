import os
import requests

DEFAULT_SENDER = {"name": "OTISDav", "email": "david.botcholi@davidbotcholi.online"}
ADMIN_EMAIL = 'davidbotcholi2003@gmail.com'

def send_notification(subject, message, recipient, **kwargs):
    """
    kwargs peut contenir d'autres informations si nécessaire
    """
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
    if not BREVO_API_KEY:
        print("Clé API Brevo introuvable !")
        return {"error": "Clé API introuvable"}

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": DEFAULT_SENDER,
        "to": [{"email": recipient}],
        "subject": subject,
        "htmlContent": message
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Email envoyé à {recipient}: {subject}")
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur envoi email à {recipient}: {e}")
        return {"error": str(e)}
