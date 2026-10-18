import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        "url": "https://cardmarket.com"
    }
]

def estrai_prezzo_con_browser(url):
    # Configuriaramo Google Chrome in modalità invisibile (headless) per il server di GitHub
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Impronta digitale umana per aggirare Cloudflare
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Attendiamo 5 secondi per dare il tempo a Cloudflare di approvare la connessione e caricare i prezzi
        time.sleep(5)
        
        # Catturiamo il codice della pagina caricata dal browser
        html_pagina = driver.page_source
        soup = BeautifulSoup(html_pagina, 'html.parser')
        
        # Cerchiamo il primo prezzo reale della tabella dei venditori
        blocco_prezzo = soup.find("span", {"class": "font-bold text-nowrap"})
        if blocco_prezzo:
            return blocco_prezzo.text.strip()
            
        # Alternativa nel caso in cui legga prima i dati statistici della colonna destra
        prezzo_statistico = soup.find("span", {"class": "color-primary"})
        if prezzo_statistico:
            return prezzo_statistico.text.strip()
            
        return "Prezzo non trovato nella pagina"
        
    except Exception as e:
        return f"Errore simulazione browser: {str(e)}"
    finally:
        if driver:
            driver.quit()

def main():
    risultati = {}
    for carta in CARTE_POKEMON:
        print(f"Apertura browser simulato per: {carta['nome']}...")
        prezzo = estrai_prezzo_con_browser(carta["url"])
        risultati[carta["id"]] = {
            "nome": carta["nome"],
            "prezzo_ita_nm": prezzo
        }
    
    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("Scraping con browser completato con successo!")

if __name__ == "__main__":
    main()
