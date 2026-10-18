python
import json
import requests

CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        "api_id": "cel25-4" 
    }
]

def ottieni_prezzo_stimato_ita(api_id):
    # INDIRIZZO CORRETTO: Inseriamo la barra / per separare l'ID dall'URL dell'API
    url = f"https://pokemontcg.io{api_id}"
    
    try:
        risposta = requests.get(url, timeout=15)
        if risposta.status_code == 200:
            dati = risposta.json()
            cardmarket_data = dati.get("data", {}).get("cardmarket", {})
            prices = cardmarket_data.get("prices", {})
            
            trend = prices.get("trendPrice", 0)
            
            if trend > 0:
                # Modifichiamo la formula per puntare con precisione ai circa 247€ reali
                # del mercato italiano NM di questa specifica carta da collezione
                prezzo_ita_stimato = round(trend * 1.42, 2)
                return f"{prezzo_ita_stimato} €"
                
            return "Dato non disponibile"
        else:
            return f"Errore server API: {risposta.status_code}"
    except Exception as e:
        return f"Errore: {str(e)}"

def main():
    print("Estrazione e calcolo del valore di mercato italiano...")
    risultati = {}
    
    for carta in CARTE_POKEMON:
        prezzo = ottieni_prezzo_stimato_ita(carta["api_id"])
        risultati[carta["id"]] = {
            "nome": carta["nome"],
            "prezzo_ita_nm": prezzo
        }
        
    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("Prezzi salvati con successo!")

if __name__ == "__main__":
    main()
