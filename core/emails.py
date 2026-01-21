import requests, os
from django.conf import settings


DEFAULT_SENDER = {"name": "David Botcholi", "email": "david.botcholi@gmail.com"}  # ou ton email gratuit
ADMIN_EMAIL = 'davidbotcholi2003@gmail.com'


def send_notification(subject, message, recipient):
    """
    Envoie un email via l'API Brevo.
    recipient: string (email du destinataire)
    """
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
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
    if response.status_code != 201 and response.status_code != 200:
        print("Erreur envoi email:", response.text)
    return response.json()


# Exemple d'utilisation :
# Email au client
send_notification(
    subject="Confirmation de votre demande",
    message="<h3>Merci pour votre demande !</h3><p>Nous vous contacterons bientôt.</p>",
    recipient="client@gmail.com"
)

# Email à l'admin
send_notification(
    subject="Nouvelle demande reçue",
    message="<p>Une nouvelle demande vient d'être envoyée.</p>",
    recipient=ADMIN_EMAIL
)
