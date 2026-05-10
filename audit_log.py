from utils import load_json, session, continue_prompt
from tabulate import tabulate

def show_audit_logs():
    session.header("Auditní logy - Vyhledávání")
    logs = load_json("system_log.json")
    
    if not logs:
        print("Žádné záznamy v logu.")
        continue_prompt()
        return

    print("Filtry (nechte prázdné pro přeskočení):")
    filter_user = input("Uživatel: ").strip().lower()
    filter_date = input("Datum (RRRR-MM-DD): ").strip()
    filter_action = input("Akce (např. VKLAD, Přihlášení): ").strip().lower()

    filtered_logs = []
    for entry in logs:
        # EN: Check user
        # CZ: Kontrola uživatele
        if filter_user and filter_user != entry['user'].lower():
            continue
        
        # EN: Check date (ts starts with the date, so we only need to compare the beginning of the string)
        # CZ: Kontrola data (ts začíná datem, tak stačí porovnat začátek řetězce)
        if filter_date and not entry['ts'].startswith(filter_date):
            continue
            
        # EN: Check action (we search for the text anywhere in the action description)
        # CZ: Kontrola akce (hledáme, jestli se text vyskytuje kdekoli v popisu akce)
        if filter_action and filter_action not in entry['action'].lower():
            continue
            
        filtered_logs.append(entry)
    filtered_logs.reverse()
    
    # EN: Display results
    # CZ: Výpis výsledků
    if not filtered_logs:
        print("\n[!] Žádné záznamy neodpovídají filtrům.")
    else:
        
        print(f"\nNalezeno {len(filtered_logs)} záznamů:\n")
        print(tabulate(
            filtered_logs, 
            headers={"ts": "Čas", "user": "Uživatel", "action": "Akce"}, 
            tablefmt="fancy_grid"
        ))

    continue_prompt()