import os
import requests

DEFAULT_SENDER = {"name": "David Botcholi", "email": "david.botcholi@gmail.com"}
ADMIN_EMAIL = 'davidbotcholi2003@gmail.com'

def send_notification(subject, message, recipient):
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
    if not BREVO_API_KEY:
        print("⚠️ Clé API Brevo non trouvée ! Vérifie Render")
        return

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

    response = requests.post(url, json=data, headers=headers)
    if response.status_code not in (200, 201):
        print("Erreur envoi email:", response.text)
    return response.json()
