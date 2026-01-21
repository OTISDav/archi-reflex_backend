import os
import requests

DEFAULT_SENDER = {"name": "OTISDav", "email": "david.botcholi@davidbotcholi.online"}
ADMIN_EMAIL = 'davidbotcholi2003@gmail.com'

def send_notification(subject, message, recipient):

    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')

    if not BREVO_API_KEY:
        print("⚠️ Clé API Brevo introuvable ! Vérifie que la variable d'environnement est bien définie sur Render et que le service est redéployé.")
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
        if response.status_code not in (200, 201):
            print(f"❌ Erreur envoi email à {recipient}: {response.text}")
            return {"error": response.text, "status_code": response.status_code}
        else:
            print(f"✅ Email envoyé à {recipient}: {subject}")
            return response.json()
    except requests.RequestException as e:
        print(f"❌ Exception envoi email à {recipient}: {e}")
        return {"error": str(e)}

