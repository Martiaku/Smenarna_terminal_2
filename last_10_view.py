from utils import load_json, session, continue_prompt, export_to_pdf
from printing import process_transaction_archive
from tabulate import tabulate
from datetime import datetime

def reprint_receipt():
    session.header("Kopie dokladu / Re-tisk")
    
    receipts = load_json("receipts.json")
    
    if not receipts:
        print("[!] Žádné vydané doklady nebyly nalezeny.")
        continue_prompt(); return

    # EN: 1. Show the last 10 transactions for quick selection
    # CZ: 1. Zobrazíme posledních 10 transakcí pro rychlý výběr
    # EN: Reverse to get the latest transactions first, then take the top 10
    # CZ: Otočíme, aby nejnovější byly nahoře
    latest_receipts = list(reversed(receipts))[:10]
    
    table_data = []
    for i, r in enumerate(latest_receipts, 1):
        # EN: Prepare data for the table
        # CZ: Připravíme data pro tabulku
        table_data.append([
            i, 
            r['id'], 
            r['timestamp'], 
            f"{r['mnozstvi_z']} {r['mena_z']}", 
            f"{r['mnozstvi_do']} {r['mena_do']}"
        ])

    print("Posledních 10 transakcí:")
    print(tabulate(table_data, headers=["Č.", "ID Dokladu", "Čas", "Dal", "Dostal"], tablefmt="fancy_grid"))
    
    print("\nq - Zpět | ID - Zadejte ID dokladu pro vyhledání")
    volba = input("\nVyberte číslo (1-10) nebo zadejte celé ID dokladu: ").strip()

    if volba.lower() == 'q':
        return

    selected_receipt = None

    # EN: 2. Selection logic
    # CZ: 2. Logika vyhledání
    try:
        if len(volba) <= 2: 
            idx = int(volba) - 1
            if 0 <= idx < len(latest_receipts):
                selected_receipt = latest_receipts[idx]
        else:
            selected_receipt = next((r for r in receipts if r['id'] == volba), None)
    except ValueError:
        print("[!] Neplatný vstup.")
        continue_prompt(); return

   # EN: 3. Display for copy
   # CZ: 3. Zobrazení kopie
    if selected_receipt:
        print("\n" + "!"*40)
        print("         DUPLIKÁT DOKLADU")
        print("!"*40)
        
        print(f"ID: {selected_receipt['id']}")
        print(f"Datum transakce: \n{selected_receipt['timestamp']}")
        print(f"Pokladník: {selected_receipt['pokladnik']}")
        print("-" * 40)
        print(f"KLIENT DAL:    {selected_receipt['mnozstvi_z']:.2f} {selected_receipt['mena_z']}")
        print(f"KLIENT DOSTAL: {selected_receipt['mnozstvi_do']:.2f} {selected_receipt['mena_do']}")
        print(f"KURZ:          {selected_receipt['kurz']:.4f}")
        
        if selected_receipt.get("zakaznik"):
            c = selected_receipt["zakaznik"]
            print("-" * 40)
            print("IDENTIFIKACE KLIENTA (AML):")
            print(f"Jméno: {c['jmeno']} {c['prijmeni']}")
            print(f"Doklad: {c['doklad']}")
            
        print("="*40)
        print(f"Vytisknuto: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print("="*40)

        # EN: 4. Export to PDF (only if we have data)
        # CZ: 4. Export do PDF (pouze pokud máme data)
        export_to_pdf(selected_receipt, title="DUPLIKÁT DOKLADU (KOPIE)")
        print("\n[OK] PDF kopie byla vygenerována.")

    else:
        # EN: If no receipt was found, show an error message
        # CZ: Pokud se nic nenašlo, vypíšeme chybu a export ignorujeme
        print("\n[!] Doklad s tímto ID nebyl nalezen. Export nelze provést.")

    continue_prompt()