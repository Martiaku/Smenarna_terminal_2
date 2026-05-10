from utils import session, continue_prompt, load_json, save_json, get_valid_rate, add_system_log

# =================================================================
# EN: This module handles the logic for adding money to the cash desk. It includes a pure function for calculating the new balance, which can be easily tested with pytest.
# CZ: Tento modul se zabývá logikou pro přidávání peněz do pokladny. Obsahuje čistou funkci pro výpočet nového zůstatku, která může být snadno testována pomocí pytest.
# =================================================================

def calculate_new_balance(current_balance: float, deposit_amount: float) -> float:
    """
    EN: Calculates the new balance after depositing cash.
    CZ: Vypočítá nový zůstatek po vložení hotovosti.

    Args:
        EN: current_balance (float): Current amount of money in the cash desk for the given currency.
        CZ: current_balance (float): Aktuální množství peněz v dané měně v pokladně.
        EN: deposit_amount (float): Amount the cashier wants to deposit.
        CZ: deposit_amount (float): Částka, kterou chce pokladník vložit.

    Raises:
        EN: ValueError: If the deposit amount is 0 or negative.
        CZ: ValueError: Pokud je vkládaná částka 0 nebo záporná.

    Returns:
        EN: float: New balance after adding the deposit.
        CZ: float: Nový výsledek zůstatku po přičtení vkladu.
    """
    if deposit_amount <= 0:
        raise ValueError("Částka musí být vyšší než 0.")
    
    return current_balance + deposit_amount


# =================================================================
# EN:High-level function (user interaction)
# CZ: HLAVNÍ FUNKCE (INTERAKCE S UŽIVATELEM)
# =================================================================

def add_money():
    """
    EN: Function for adding money to the cash desk. The user selects a currency and enters an amount to be added to the current balance.
    CZ: Funkce pro přidání peněz do pokladny. Uživatel vybere měnu a zadá částku, která se přičte k aktuálnímu zůstatku.
    Raises:
        EN: IndexError: If the user selects an invalid currency index.
        CZ: IndexError: Pokud uživatel zadá neplatný index měny.
        EN: ValueError: If the user enters an invalid amount (not a number or a negative value).
        CZ: ValueError: Pokud uživatel zadá neplatnou částku (ne číslo nebo zápornou hodnotu).
    """
    session.header("Vklad do pokladny")
    
    # EN: 1. Load data
    # CZ: 1. Načtení dat
    rates = load_json("currency.json")
    balances = load_json("balances.json", default_value={})
    
    if not rates:
        print("[!] Chyba: Soubor currency.json nebyl nalezen. Nejdříve přidej měny.")
        continue_prompt(); return

    # EN: 2. Synchronization: Ensure that every currency from the rates is also in the cash desk balances
    # CZ: 2. SYNCHRONIZACE: Zajistíme, aby každá měna z kurzů byla i v pokladně
    updated = False
    for currency in rates:
        code = currency["name"]
        if code not in balances:
            balances[code] = 0.0
            updated = True
    
    if updated:
        save_json("balances.json", balances)

    # EN: 3. Select currency for deposit
    # CZ:3. Výběr měny pro vklad
    if not balances:
        print("[!] Žádné měny k dispozici.")
        continue_prompt(); return

    print("Dostupné měny v pokladně:")
    currency_list = list(balances.keys())
    for i, curr in enumerate(currency_list, 1):
        print(f"{i} - {curr:<5} (Aktuálně: {balances[curr]:>10.2f})")
    
    volba = input("\nVyber číslo měny pro vklad (nebo 'q' pro návrat): ")
    if volba.lower() == 'q': return

    try:
        index = int(volba) - 1
        if index < 0 or index >= len(currency_list):
             raise IndexError
        selected_curr = currency_list[index]
    except (ValueError, IndexError):
        print("[!] Neplatná volba.")
        continue_prompt(); return

    # EN: 4. Perform the deposit
    # CZ: 4. Samotný vklad
    old_balance = balances[selected_curr]
    amount = get_valid_rate(f"Kolik jednotek {selected_curr} chceš vložit? ")
    
    # EN:--- TESTING LOGIC ---
    # CZ:--- POUŽITÍ TESTOVATELNÉ LOGIKY ---
    try:
        new_balance = calculate_new_balance(old_balance, amount)
        
        # EN: If the calculation was successful, save and log the new balance
        # CZ:Pokud výpočet proběhl v pořádku, uložíme a zalogujeme
        balances[selected_curr] = new_balance
        save_json("balances.json", balances)
        
        # EN: 5. AUDIT LOG
        # CZ: 5. ZÁZNAM DO AUDITU
        log_msg = (f"VKLAD: {selected_curr} | "
                   f"Změna: +{amount:.2f} | "
                   f"Stav: {old_balance:.2f} -> {new_balance:.2f}")
        
        add_system_log(log_msg, session.current_user['name'])
        
        print(f"\n[OK] Pokladna aktualizována.")
        print(f"Měna: {selected_curr} | Nový stav: {new_balance:.2f}")

    except ValueError as e:
        # EN: Here we catch the error if someone tries to enter 0 or a negative number
        # CZ: Tady zachytíme chybu, pokud by někdo zkusil vložit 0 nebo záporné číslo
        print(f"[!] {e}")
    
    continue_prompt()