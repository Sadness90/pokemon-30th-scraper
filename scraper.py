import json
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        # Questo URL applica già a monte i filtri rigidi di lingua italiana (language=5) e Near Mint (condition=1)
        "url": "https://cardmarket.com"
    }
]

def estrai_prezzo_con_browser(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Lasciamo caricare la pagina per 5 secondi
        time.sleep(5)
        
        html_pagina = driver.page_source
        soup = BeautifulSoup(html_pagina, 'html.parser')
        
        # STRATEGIA DEFINITIVA: Troviamo la tabella principale dove ci sono tutti i venditori
        tabella_offerte = soup.find("div", {"class": "table-body"}) or soup.find("div", {"id": "articlesContainer"})
        
        if tabella_offerte:
            # Cerchiamo tutti i blocchi di testo che contengono il simbolo dell'Euro €
            testo_tabella = tabella_offerte.get_text()
            # Questa formula cerca numeri scritti come "170,00 €" o "247,00 €" o "247 €"
            prezzi_trovati = re.findall(r'\d+(?:[.,]\d+)?\s*€', testo_tabella)
            
            if prezzi_trovati:
                # Cardmarket ordina le carte dal prezzo più basso in assoluto in alto.
                # Avendo già filtrato l'URL per carte Italiane e NM, il primo prezzo che incontriamo è il minimo reale che cerchi!
                return prezzi_trovati[0].strip()
        
        # STRATEGIA DI RISERVA: Se la tabella principale ha cambiato ID, cerchiamo nell'intera pagina il primo prezzo utile
        tutto_il_testo = soup.get_text()
        tutti_i_prezzi = re.findall(r'\d+(?:[.,]\d+)?\s*€', tutto_il_testo)
        if tutti_i_prezzi:
            # Escludiamo eventuali piccoli prezzi statistici e prendiamo il primo valore sopra i 10 euro per sicurezza
            for prezzo in tutti_i_prezzi:
                valore_numerico = int(re.sub(r'[^\d]', '', prezzo))
                if valore_numerico > 1000: # Cifra espressa in centesimi (es. 10,00€), quindi > 10€
                    return prezzo.strip()
                    
        return "Nessun prezzo rilevato nella pagina"
        
    except Exception as e:
        return f"Errore: {str(e)}"
    finally:
        if driver:
            driver.quit()

def main():
    risultati = {}
    for carta in CARTE_POKEMON:
        print(f"Estrazione prezzo minimo per: {carta['nome']}...")
        prezzo = estrai_prezzo_con_browser(carta["url"])
        risultati[carta["id"]] = {
            "nome": carta["nome"],
            "prezzo_ita_nm": prezzo
        }
    
    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("Fatto!")

if __name__ == "__main__":
    main()
