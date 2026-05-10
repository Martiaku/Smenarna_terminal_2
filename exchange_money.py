from utils import load_json, save_json, continue_prompt, session, get_valid_rate, add_system_log
from printing import process_transaction_archive

# =================================================================
# EN: Clean logic (testable with pytest)
# CZ: ČISTÁ LOGIKA (TESTOVATELNÉ POMOCÍ PYTEST)
# =================================================================

def calculate_cross_exchange(amount_from, buy_rate_from, sell_rate_to, target_currency_name):
    """
        EN: Calculates the final amount of currency and rounds it according to the currency.
        CZ: Vypočítá výslednou částku směny a zaokrouhlí ji podle měny.
    """
    if amount_from <= 0:
        raise ValueError("Částka musí být kladná.")

    val_in_czk = amount_from * buy_rate_from
    exact_amount_to = val_in_czk / sell_rate_to
    
    if target_currency_name == "CZK":
        return float(int(exact_amount_to+ 0.5))  # EN Rounding to the nearest whole CZK. CZ: Zaokrouhlení na celé koruny (haléřové vyrovnání)
    return round(exact_amount_to, 2)

def check_aml_limit(amount_from, buy_rate_from, rates):
    """
    EN: Returns True if the currency value exceeds 1000 EUR.
    CZ: Vrací True, pokud hodnota směny přesahuje 1000 EUR.
    """
    val_in_czk = amount_from * buy_rate_from
    
    # EN: Look for EUR rate to convert the value to EUR for AML check
    # CZ: Najdeme kurz EUR pro převod hodnoty na EUR pro AML kontrolu
    eur_data = next((r for r in rates if r['name'] == "EUR"), None)
    eur_rate = eur_data['sell_rate'] if eur_data else 25.0
    
    val_in_eur = val_in_czk / eur_rate
    return val_in_eur >= 1000

# =================================================================
# EN: Main function (user interaction)
# CZ: HLAVNÍ FUNKCE (INTERAKCE S UŽIVATELEM)
# =================================================================

def exchange_money():
    session.header("Přímý převod měn (Cross Exchange)")
    
    rates = load_json("currency.json")
    balances = load_json("balances.json")
    
    if not rates or not balances:
        print("[!] Chyba v datech.")
        continue_prompt(); return

    # EN: 1. & 2. CURRENCY SELECTION
    # CZ: 1. & 2. VÝBĚR MĚN
    
    try:
        print("Měna, kterou klient odevzdá:")
        for i, r in enumerate(rates, 1):
            print(f"{i} - {r['name']} (V pokladně: {balances.get(r['name'], 0):.2f})")
        
        idx_from = int(input("\nVyber měnu (Od klienta): ")) - 1
        curr_from = rates[idx_from]
        
        print(f"\nMěna, kterou klient dostane (výměnou za {curr_from['name']}):")
        target_rates = [r for r in rates if r['name'] != curr_from['name']]
        for i, r in enumerate(target_rates, 1):
            print(f"{i} - {r['name']} (V pokladně: {balances.get(r['name'], 0):.2f})")
        
        idx_to = int(input("\nVyber měnu (Pro klienta): ")) - 1
        curr_to = target_rates[idx_to]
    except (ValueError, IndexError):
        print("[!] Neplatná volba.")
        continue_prompt(); return

    # EN: 3. AMOUNT INPUT
    # CZ: 3. ZADÁNÍ ČÁSTKY
    amount_from = get_valid_rate(f"Kolik {curr_from['name']} klient dává? ")
    
    # EN: Call the testable logic for calculation
    # CZ: Voláme testovatelnou logiku pro výpočet
    try:
        final_amount_to = calculate_cross_exchange(
            amount_from, 
            curr_from['buy_rate'], 
            curr_to['sell_rate'], 
            curr_to['name']
        )
    except ValueError as e:
        print(f"[!] {e}")
        continue_prompt(); return

    # EN: Helper values for recap
    # CZ: Pomocné hodnoty pro rekapitulaci
    val_in_czk = amount_from * curr_from['buy_rate']
    exact_amount_to = val_in_czk / curr_to['sell_rate']
    rounding_diff = exact_amount_to - final_amount_to
    cross_rate = exact_amount_to / amount_from

    # EN: --- AML CHECK ---
    # CZ: --- AML KONTROLA ---
    client_data = None
    if check_aml_limit(amount_from, curr_from['buy_rate'], rates):
        print("\n" + "!"*50)
        print(" !!! LIMIT 1000 EUR PŘEKROČEN - VYŽADOVÁNO AML !!!")
        print(" Zadejte povinné údaje o klientovi:")
        print("!"*50)
        client_data = {
            "jmeno": input("Jméno: ").strip(),
            "prijmeni": input("Příjmení: ").strip(),
            "identifikace": input("Rodné číslo / Datum narození: ").strip(),
            "doklad": input("Číslo dokladu: ").strip(),
            "narodnost": input("Národnost: ").strip()
        }
        if not all(client_data.values()):
            print("\n[!] Chyba: Všechny AML údaje musí být vyplněny!")
            continue_prompt(); return

    # EN: 4. CASHIER CHECK
    # CZ: 4. KONTROLA POKLADNY
    if balances.get(curr_to['name'], 0) < final_amount_to:
        print(f"[!] CHYBA: V pokladně není dostatek {curr_to['name']} (Chybí {(final_amount_to - balances[curr_to['name']]):.2f})")
        continue_prompt(); return

    # EN: 5. RECAPITULATION
    # CZ: 5. REKAPITULACE
    print(f"\n" + "-"*40)
    print(f"REKAPITULACE SMĚNY:")
    print(f"Klient dává:     {amount_from:.2f} {curr_from['name']}")
    print(f"Klient dostane: {final_amount_to:.2f} {curr_to['name']}")
    print(f"Efektivní kurz: 1 {curr_from['name']} = {cross_rate:.4f} {curr_to['name']}")
    
    if abs(rounding_diff) > 0.001:
        print(f"\n[i] UPOZORNĚNÍ: Došlo k haléřovému vyrovnání.")
        print(f"    Rozdíl (zaokr.):    {-rounding_diff:.2f} {curr_to['name']}")
    print("-"*40)
    
    while True:
        potvrzeni = input("\nProvést směnu a archivovat? (a/n): ").lower().strip()
        if potvrzeni in ['a', 'n']: break
        print("[!] Neplatná volba.")

    if potvrzeni == 'a':
        # EN: 6. UPDATE BALANCES
        # CZ: 6. AKTUALIZACE BALANCES
        balances[curr_from['name']] += amount_from
        balances[curr_to['name']] -= final_amount_to
        save_json("balances.json", balances)
        
        # EN: COMPILE DATA FOR ARCHIVING
        # CZ: KOMPILACE DAT PRO ARCHIVACI
        transaction_info = {
            "pokladnik": session.current_user['name'],
            "mnozstvi_z": amount_from,
            "mena_z": curr_from['name'],
            "mnozstvi_do": final_amount_to,
            "mena_do": curr_to['name'],
            "kurz": cross_rate,
            "zakaznik": client_data
        }

        process_transaction_archive(transaction_info)
        
        log_msg = (f"Výměna: {curr_from['name']} -> {curr_to['name']} | "
                   f"Dáno: {amount_from:.2f} | Vydáno: {final_amount_to:.2f} | Kurz: {cross_rate:.2f}")
        if client_data:
            log_msg += f" | AML OK: {client_data['prijmeni']}"
            
        add_system_log(log_msg, session.current_user['name'])
        print(f"\n[OK] Směna byla úspěšně provedena.")
    else:
        print("\n[i] Stornováno.")
    
    continue_prompt()