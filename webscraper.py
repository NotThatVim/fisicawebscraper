# scraper.py
import requests
from bs4 import BeautifulSoup
import telegrambot  # Importiamo l'altro file

# --- Configurazione ---
URL = 'https://fisica1ricco.unipr.it/risultati.html'
MATRICOLA = '371490'
FILE_VOTO_SALVATO = 'ultimo_voto.txt'

# --- Logica di scraping ---
def get_saved_grade():
    try:
        with open(FILE_VOTO_SALVATO, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_new_grade(grade):
    with open(FILE_VOTO_SALVATO, 'w') as file:
        file.write(grade)

def main_scraper():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        cella_matricola = soup.find(string=MATRICOLA)

        if cella_matricola:
            riga = cella_matricola.find_parent('tr')
            celle_dati = riga.find_all('td')
            
            if len(celle_dati) > 1:
                current_grade = celle_dati[1].text.strip()
                old_grade = get_saved_grade()
                
                if old_grade is None or current_grade != old_grade:
                    print(f"Novità rilevata! Voto: {current_grade}")
                    # Chiamiamo la funzione di notifica che si trova nell'altro file
                    telegrambot.notify_user(current_grade)
                    save_new_grade(current_grade)
                else:
                    print("Nessun nuovo risultato. Voto invariato.")
            else:
                print("Non è stato possibile trovare il voto.")
        else:
            print(f"Matricola '{MATRICOLA}' non presente. Nessun risultato.")
            
    except requests.exceptions.RequestException as e:
        print(f"Errore di connessione: {e}")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

if __name__ == "__main__":
    main_scraper()