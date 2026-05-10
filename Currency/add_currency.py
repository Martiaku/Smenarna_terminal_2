from utils import clear_terminal, session, continue_prompt, load_json, save_json, get_valid_rate

def add_currency():  # Opraven překlep
    session.header("Přidání měny")
    data_currency = load_json("currency.json")
    
    # EN: If load_json returns None, we will treat it as an empty list
    # CZ: Pokud load_json vrátí None, uděláme z toho prázdný seznam
    if data_currency is None:
        data_currency = []

    name = input("Zadej název měny (např. USD): ").strip().upper()
    if not name:
        print("[!] Název měny nesmí být prázdný.")
        continue_prompt(); return
    
    # EN: Check if the currency already exists
    # CZ: Kontrola existence
    if any(c["name"] == name for c in data_currency):
        print(f"\n[!] Chyba: Měna {name} již v systému existuje.")
        continue_prompt()
        return

    buy_rate = get_valid_rate("Zadej nákupní kurz: ")
    sell_rate = get_valid_rate("Zadej prodejní kurz: ")

    new_currency = {
        "name": name, 
        "buy_rate": buy_rate, 
        "sell_rate": sell_rate
    }
    
    data_currency.append(new_currency)
    save_json("currency.json", data_currency)
    
    # EN: --- SYNCHRONIZATION OF BALANCES ---
    # CZ: --- SYNCHRONIZACE BALANCES ---
    balances = load_json("balances.json")
    if balances is None or isinstance(balances, list):
        balances = {}
    
    if name not in balances:
        balances[name] = 0.0
        save_json("balances.json", balances)
    
    print("-" * 30)
    print(f"[OK] Měna {name} byla uložena a zinicializována v pokladně.")
    continue_prompt()