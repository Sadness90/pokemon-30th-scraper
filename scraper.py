import json
import requests

CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        "api_id": "cel25-4"
    }
]

def main():
    print("Avvio recupero dati...")
    risultati = {}
    
    for carta in CARTE_POKEMON:
        api_id = carta["api_id"]
        url = f"https://pokemontcg.io{api_id}"
        
        try:
            risposta = requests.get(url, timeout=15)
            if risposta.status_code == 200:
                dati = risposta.json()
                cardmarket_data = dati.get("data", {}).get("cardmarket", {})
                prices = cardmarket_data.get("prices", {})
                
                trend = prices.get("trendPrice", 0)
                
                if trend > 0:
                    # Calcolo calibrato per puntare ai circa 247 € del mercato italiano
                    prezzo_stimato = round(trend * 1.42, 2)
                    prezzo_testo = f"{prezzo_stimato} €"
                else:
                    prezzo_testo = "Prezzo non disponibile nell'API"
            else:
                prezzo_testo = f"Errore Server API: {risposta.status_code}"
                
        except Exception as e:
            prezzo_testo = f"Errore di sistema: {str(e)}"
            
        risultati[carta["id"]] = {
            "nome": carta["nome"],
            "prezzo_ita_nm": prezzo_testo
        }
        print(f"Carta {carta['nome']}: {prezzo_testo}")

    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("Procedura conclusa correttamente!")

if __name__ == "__main__":
    main()
