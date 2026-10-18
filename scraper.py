import requests
from bs4 import BeautifulSoup
import json
import re

CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        # URL specifico ottimizzato per la ricerca
        "url": "https://cardmarket.com"
    }
]

def estrai_prezzo_reale(url):
    # Usiamo un'intestazione (Header) molto più dettagliata per imitare Chrome reale
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        # Avviamo una sessione per mantenere i cookie come un vero visitatore
        sessione = requests.Session()
        risposta = sessione.get(url, headers=headers, timeout=15)
        
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            
            # Strategia 1: Cerchiamo direttamente nella tabella delle offerte caricate
            # Cardmarket usa classi specifiche per i prezzi dei venditori privati
            prezzi = soup.find_all("span", class_=re.compile(colfor=r"font-bold text-nowrap|color-primary"))
            for p in prezzi:
                testo = p.text.strip()
                if "€" in testo:
                    return testo # Restituisce il primo prezzo reale della lista filtrata!

            # Strategia 2: Se la tabella è protetta, cerchiamo nei dati statistici della pagina
            dd_elements = soup.find_all("dd")
            for dd in dd_elements:
                span = dd.find("span", class_="color-primary")
                if span and "€" in span.text:
                    # Se non trova il primo venditore, estrae il trend fedele
                    return span.text.strip()
            
            # Strategia 3: Tentativo disperato nel testo grezzo della tabella
            prezzo_generico = soup.find("div", class_="price-container")
            if prezzo_generico:
                return prezzo_generico.text.strip()
                
            return "Struttura Pagina Variata"
        elif risposta.status_code == 403:
            return "Blocco Cloudflare (403)"
        else:
            return f"Errore Server: {risposta.status_code}"
            
    except Exception as e:
        return f"Errore Connessione: {str(e)}"

def main():
    risultati = {}
    for carta in CARTE_POKEMON:
        print(f"Scansione prezzo in corso per: {carta['nome']}...")
        prezzo = estrai_prezzo_reale(carta["url"])
        risultati[carta["id"]] = {
            "nome": carta["nome"],
            "prezzo_ita_nm": prezzo
        }
    
    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("Scraping completato!")

if __name__ == "__main__":
    main()
