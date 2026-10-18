import json
import requests

# Database centralizzato con URL fissi e formule matematiche dedicate per il mercato italiano NM
CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        "url_api": "https://pokemontcg.io",
        "moltiplicatore": 1.42,
        "prezzo_fisso_errore": "247.00 €"
    },
    {
        "id": "30th-149",
        "nome": "Lugia (30C AQ 149)",
        "url_api": "https://pokemontcg.io",
        "moltiplicatore": 1.10,
        "prezzo_fisso_errore": "215.00 €"
    }
]

def main():
    print("Avvio elaborazione prezzi...")
    risultati = {}
    
    for carta in CARTE_POKEMON:
        try:
            risposta = requests.get(carta["url_api"], timeout=15)
            if risposta.status_code == 200:
                dati = risposta.json()
                prices = dati.get("data", {}).get("cardmarket", {}).get("prices", {})
                trend = prices.get("trendPrice", 0)
                
                if trend > 0:
                    prezzo_calcolato = round(trend * carta["moltiplicatore"], 2)
                    prezzo_finale = f"{prezzo_calcolato} €"
                else:
                    prezzo_finale = carta["prezzo_fisso_errore"]
            else:
                prezzo_finale = carta["prezzo_fisso_errore"]
        except:
            prezzo_finale = carta["prezzo_fisso_errore"]
            
        risultati[carta["id"]] = {
            "nome": carta["nome"],
            "prezzo_ita_nm": prezzo_finale
        }
        print(f"{carta['nome']} impostato a: {prezzo_finale}")

    # Aggiorniamo il file finale
    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("Operazione completata con successo!")

if __name__ == "__main__":
    main()
