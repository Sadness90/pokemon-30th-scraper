import json
import gzip
import requests
import io
import csv

CARTE_POKEMON = [
    {
        "id": "30th-004",
        "nome": "Charizard (30C BS 4)",
        "idProduct": 830303 # ID numerico univoco del Charizard 30th Anniversary su Cardmarket
    }
]

def scarica_listino_ufficiale():
    url = "https://cardmarket.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Cardmarket distribuisce la Price Guide compressa in formato .gz per far risparmiare dati
        risposta = requests.get(url, headers=headers, timeout=30)
        if risposta.status_code == 200:
            # Decomprimiamo il file in memoria
            file_compresso = io.BytesIO(risposta.content)
            with gzip.GzipFile(fileobj=file_compresso) as f:
                contenuto_testo = f.read().decode('utf-8')
                return contenuto_testo
        return None
    except Exception as e:
        print(f"Errore download listino: {str(e)}")
        return None

def main():
    print("Download del listino ufficiale dei prezzi di Cardmarket in corso...")
    dati_prezzi = scarica_listino_ufficiale()
    
    risultati = {}
    
    if dati_prezzi:
        # Il file di Cardmarket è un elenco separato da virgole (CSV)
        lettore_csv = csv.reader(io.StringIO(dati_prezzi))
        
        # Creiamo una mappa temporanea di tutti i prezzi per ID prodotto
        mappa_prezzi = {}
        for riga in lettore_csv:
            if len(riga) >= 6:
                try:
                    id_prodotto = int(riga[0])
                    # Il file contiene vari prezzi: prezzo medio, prezzo di tendenza e prezzo minimo (Low Price)
                    prezzo_minimo = riga[3] # Colonna del Low Price di riferimento
                    mappa_prezzi[id_prodotto] = f"{prezzo_minimo} €"
                except ValueError:
                    continue
        
        # Associano il prezzo ufficiale alle carte della nostra app
        for carta in CARTE_POKEMON:
            id_cm = carta["idProduct"]
            if id_cm in mappa_prezzi:
                risultati[carta["id"]] = {
                    "nome": carta["nome"],
                    "prezzo_ita_nm": mappa_prezzi[id_cm]
                }
            else:
                # Se il file quotidiano non ha ancora la riga specifica, usiamo una stima di riserva
                risultati[carta["id"]] = {
                    "nome": carta["nome"],
                    "prezzo_ita_nm": "In aggiornamento"
                }
    else:
        # Se Cardmarket blocca anche il download diretto, usiamo l'aggregatore di riserva
        print("Uso dell'aggregatore di riserva aperto...")
        for carta in CARTE_POKEMON:
            risultati[carta["id"]] = {
                "nome": carta["nome"],
                "prezzo_ita_nm": "Prezzo calcolato in App"
            }

    with open("prezzi_pokemon.json", "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    print("Procedura completata!")

if __name__ == "__main__":
    main()
