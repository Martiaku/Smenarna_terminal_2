import os
import datetime
from utils import load_json, save_json, export_to_pdf

def process_transaction_archive(data):
    """
    EN: This function handles the entire process of saving a transaction to the archive, generating a PDF receipt, and printing a formatted output to the console.
    CZ: Zastřešuje uložení do DB, generování PDF a výpis do konzole.
    """
    # EN: Load the archive (or initialize if it doesn't exist)
    # CZ: Načtení archivu (nebo inicializace, pokud neexistuje)
    archive = load_json("receipts.json") or []
    
    # EN: Generate metadata (if it doesn't already exist from the previous step)
    # CZ: Generování metadat (pokud už neexistují z předchozího kroku)
    if "id" not in data:
        data["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if "timestamp" not in data:
        data["timestamp"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    # EN: --- 1. Save to JSON ---
    # CZ: --- 1. Uložení do JSONu ---
    archive.append(data)
    save_json("receipts.json", archive)
    
    # EN: --- 2. Export to PDF ---
    # CZ: --- 2. Export do PDF ---
    export_to_pdf(data, title="OFICIALNI DOKLAD O SMENE")
    
    # EN: --- 3. Formatted output to console ---
    # CZ: --- 3. Formátovaný výstup do konzole ---
    print("\n" + "="*40)
    print("         OFICIÁLNÍ DOKLAD O SMĚNĚ")
    print("="*40)
    print(f"ID: {data['id']} | Datum: {data['timestamp']}")
    print(f"Pokladník: {data['pokladnik']}")
    print("-" * 40)
    print(f"KLIENT DAL:    {data['mnozstvi_z']:.2f} {data['mena_z']}")
    print(f"KLIENT DOSTAL: {data['mnozstvi_do']:.2f} {data['mena_do']}")
    print(f"KURZ:          {data['kurz']:.4f}")
    
    if data.get("zakaznik"):
        print("-" * 40)
        c = data["zakaznik"]
        print(f"AML KLIENT:    {c['jmeno']} {c['prijmeni']} ({c['doklad']})")
    
    print("="*40)
    print("       Doklad byl odeslán do PDF")
    print("="*40 + "\n")