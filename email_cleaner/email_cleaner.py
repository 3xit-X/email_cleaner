import os
import pickle
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Se modifichi questo SCOPES, elimina il file token.pickle.
SCOPES = ['https://mail.google.com/']

def get_gmail_service():
    creds = None

    # Elimina il file token.pickle per forzare una nuova autorizzazione
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')

    # Il file token.pickle memorizza le credenziali dell'utente.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Se non ci sono credenziali valide disponibili, richiedi all'utente di effettuare l'autenticazione.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva le credenziali per la successiva esecuzione.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def delete_emails_by_sender(service, sender):
    try:
        # Ottieni l'ID del messaggio per tutte le email del mittente specificato
        result = service.users().messages().list(userId='me', q=f'from:{sender}').execute()
        messages = result.get('messages', [])

        if not messages:
            print(f"Nessuna email trovata da {sender}.")
            return

        for message in messages:
            service.users().messages().delete(userId='me', id=message['id']).execute()
            print(f"Email con ID {message['id']} eliminata.")

        print(f"Tutte le email da {sender} sono state eliminate con successo.")
    except HttpError as error:
        print(f"Si è verificato un errore: {error}")

if __name__ == '__main__':
    import os

    # Sostituisci 'mittente@email.com' con l'indirizzo email del mittente da cancellare
    SENDERS_TO_DELETE = ['opinions@opinions.be','donotreply@indeed.com','no-reply@bruxellesformation.be', 'info@geeksacademy.it', 'no-reply@accounts.google.com',' info@hellodeevie.be', 'info@my.mediamarkt.be','personal@cercolavoro.com','no-reply@poppy.be','no-reply@m1.email.samsung.com', 'notifications@matteosnidero.it', 'stef.borremans@hoeilaart.be', 'noreply@booking.com','uber@uber.com','mail@misterhoreca.be', 'mail@invoice-orange.be', 'no_reply@communications.paypal.com', 'adecco@news-it.adecco.com','info@dailyplaylists.com', 'richieste@prestitionline.it','no-reply@orange.be', 'ads-noreply@google.com', 'ebay@reply.ebay.it', 'jobalerts-noreply@linkedin.com','dieteren@express.fra1.medallia.eu', 'team@vinted.it','richieste-prestiti@segugio.it','info@fgtbbruxelles.be','no-reply@actiris.be','do-not-reply@trello.com','updates-noreply@linkedin.com','feedback@slack.com', 'tim@sourcery.ai', 'carfreenews@car-free.it','info@visioneacademy.io', 'no-reply@account.heetch.com' , 'info@service-mail.zalando-prive.it', 'myebox.noreply@bosa.fgov.be','info@service-mail.zalando.be','selezione@car-free.it', 'jobalerts-noreply@linkedin.com','monster@notifications.monster.com','hello@askcodi.com','tim@2322774.m-sender-sib.com','google-account-noreply@google.com','allianz-careers@noreply12.jobs2web.com','no-reply@alerts.talent.com','info@goals.upskillist.com','service@paypal.be','noreply@subito.it','no-reply@hello.heetch.com','ebay@ebay.com','info@study.upskillist.com']

    # Ottieni il servizio Gmail
    gmail_service = get_gmail_service()

    # Elimina le email del mittente specificato
    for SENDER_TO_DELETE in SENDERS_TO_DELETE:
        delete_emails_by_sender(gmail_service, SENDER_TO_DELETE)