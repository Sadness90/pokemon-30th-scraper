import requests
from bs4 import BeautifulSoup
import json

# Definiamo la lista delle carte del 30° Anniversario da tracciare
# Inseriamo il Charizard del tuo test con il suo esatto URL finale di Cardmarket
CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        # L'URL include già i filtri: language=5 (Italiano) e condition=1 (Near Mint)
        "url": "https://cardmarket.com"
    }
]

def estrai_prezzo_reale(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        risposta = requests.get(url, headers=headers, timeout=15)
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            # Cerchiamo il blocco di testo del primo prezzo disponibile filtrato nella tabella
            blocco_prezzo = soup.find("span", {"class": "font-bold text-nowrap"})
            if blocco_prezzo:
                return blocco_prezzo.text.strip()
            
            # Alternativa se la struttura della tabella cambia leggermente
            prezzo_alternativo = soup.find("div", {"class": "price-container"})
            if prezzo_alternativo:
                return prezzo_alternativo.text.strip()
                
        return "Non trovato"
    except Exception as e:
        return f"Errore: {str(e)}"

def main():
    risultati = {}
    for carta in CARTE_POKEMON:
        print(f"Controllo prezzo per: {carta['nome']}...")
        prezzo = estrai_prezzo_reale(carta["url"])
        risultati[carta["id"]] = {
            "nome": carta["nome"],
            "prezzo_ita_nm": prezzo
        }
    
    # Salviamo i prezzi reali estratti in un file JSON che l'app leggerà gratis
    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("File prezzi_pokemon.json aggiornato con successo!")

if __name__ == "__main__":
    main()
