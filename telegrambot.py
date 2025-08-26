# telegram_bot_logic.py
import telegram

# --- Configurazione Bot ---
BOT_TOKEN = 'non ti droppo la mia api key così dumbass'
CHAT_ID = ''

def notify_user(grade):
    """Invia una notifica Telegram con il voto."""
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        message = f"Nuovo voto disponibile: {grade}!"
        bot.send_message(chat_id=CHAT_ID, text=message)
        print("Notifica Telegram inviata con successo!")
    except Exception as e:
        print(f"Errore nell'invio della notifica: {e}")