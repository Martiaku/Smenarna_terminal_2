
from utils import clear_terminal, session, continue_prompt, load_json, save_json
from permissions import has_permissions
from tabulate import tabulate

def course_list_currency():
    session.header("Seznam kurzů měn")
    data_currency = load_json("currency.json")
    if not data_currency:
        print("Systém je prázdný. Vytvoř první měnu...")
        continue_prompt()
        return
    data = [{"name": currency["name"], "buy_rate": currency["buy_rate"], "sell_rate": currency["sell_rate"]} for currency in data_currency]
    print(tabulate(
    data, 
    headers={"name": "Měna", "buy_rate": "Nákup", "sell_rate": "Prodej"}, 
    tablefmt="fancy_grid", floatfmt=".2f", numalign="right"
    ))
    continue_prompt()