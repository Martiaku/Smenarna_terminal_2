from utils import continue_prompt, session,save_json, load_json, get_valid_rate
from utils import add_system_log


def calculate_withdrawal(current_balance, withdraw_amount):
    """
    EN: Calculates the new balance after a withdrawal.
    CZ: Vypočítá nový zůstatek po výběru.
    
    Args:
        EN: current_balance (float): Current amount of money in the cash desk for the given currency.
        CZ: current_balance (float): Aktuální stav peněz.
        EN: withdraw_amount (float): Amount to withdraw.
        CZ: withdraw_amount (float): Částka k výběru.

    Raises:
        EN: ValueError: If the withdraw amount is negative, zero, or exceeds the current balance.
        CZ: ValueError: Pokud je částka záporná, nulová nebo vyšší než zůstatek.
        
    Returns:
        EN: float: New balance after withdrawal.
        CZ: float: Nový zůstatek po výběru.
    """
    if withdraw_amount <= 0:
        raise ValueError("Částka musí být vyšší než 0.")
    
    if withdraw_amount > current_balance:
        raise ValueError("Nedostatečný zůstatek v pokladně.")
    
    return current_balance - withdraw_amount


def withdraw_money():
    session.header("Výběr z pokladny")
    
    # EN: 1. Load data
    # CZ:1. Načtení dat
    rates = load_json("currency.json", default_value=[])
    balances = load_json("balances.json", default_value={})
    
    if rates is None:
        print("[!] Chyba: Soubor currency.json nebyl nalezen."); continue_prompt(); return

    # EN: 2. Synchronization: Ensure that every currency from the rates is also in the cash desk balances)
    # CZ: 2. Synchronizace (Zůstává stejná)
    updated = False
    for currency in rates:
        code = currency["name"]
        if code not in balances:
            balances[code] = 0.0
            updated = True
    
    if updated:
        save_json("balances.json", balances)
    
    # EN: 3. Currency selection
    # CZ: 3. Výběr měny
    print("Dostupné měny v pokladně:")
    currency_list = list(balances.keys())
    for i, curr in enumerate(currency_list, 1):
        print(f"{i} - {curr:<5} (Aktuálně: {balances[curr]:>10.2f})")
        
    volba = input("\nVyber číslo měny pro výběr (nebo 'q' pro návrat): ")
    if volba.lower() == 'q': return

    try:
        index = int(volba) - 1
        selected_curr = currency_list[index]
    except (ValueError, IndexError):
        print("[!] Neplatná volba."); continue_prompt(); return
    
    # EN: 4. Amount input
    # CZ: 4. Zadání částky
    amount = get_valid_rate(f"Zadej častku pro vyber {selected_curr}: ")
    
    # EN:--- TESTING LOGIC ---
    # CZ:--- POUŽITÍ TESTOVATELNÉ LOGIKY ---
    try:
        # EN: Calculate the new balance or raise an error (e.g., not enough money)
        # CZ: Vypočítá se nový stav nebo vyhodí chybu (např. málo peněz)
        new_balance = calculate_withdrawal(balances[selected_curr], amount)
        
        # EN: If the calculation was successful, save and log the new balance
        # CZ: 5. Pokud vše klaplo, uložíme a zalogujeme
        balances[selected_curr] = new_balance
        save_json("balances.json", balances)
        
        log_msg = (f"VYBER: {selected_curr} | "
                   f"Změna: -{amount:.2f} | "
                   f"Stav: {new_balance:.2f}")
        
        add_system_log(log_msg, session.current_user['name'])
    
        print(f"\n[OK] Pokladna aktualizována.")
        print(f"Měna: {selected_curr} | Nový stav: {new_balance:.2f}")

    except ValueError as e:
        # EN: Catch both "Negative amount" and "Insufficient balance"
        # CZ: Tady zachytíme jak "Zápornou částku", tak "Nedostatečný zůstatek"
        print(f"[!] Chyba: {e}")

    continue_prompt()