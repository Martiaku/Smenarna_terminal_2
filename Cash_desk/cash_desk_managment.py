from utils import session, load_json, continue_prompt
from tabulate import tabulate

def show_balance():
    session.header("Stav pokladny")
    balances = load_json("balances.json")
    
    if not balances:
        print("[!] Pokladna je prázdná nebo soubor neexistuje.")
        continue_prompt()
        return

    # EN: Prepare data for tabulate (convert dictionary to list of lists)
    # CZ: Připravíme data pro tabulate (převod ze slovníku na seznam seznamů)
    table_data = [[currency, amount] for currency, amount in balances.items()]
    
    print(tabulate(
        table_data, 
        headers=["Měna", "Zůstatek"], 
        tablefmt="fancy_grid", 
        floatfmt=".2f",
        numalign="right"
    ))
    continue_prompt()