

# This page contains "validation functions"

from datetime import date

def validation_yes_no(prompt):
    """
    EN: Validates a yes/no input from the user.
    CZ: Ověřuje vstup "ano/ne" od uživatele.
    """
    valid_yes = ["ano", "a"]
    valid_no = ["ne", "n"]
    while True:
        value = input(prompt).strip().lower()
        if value in valid_yes:
            return True
        if value in valid_no:
            return False
        print('Chyba: Odpovězte prosím "ano" nebo "ne". ' )
        

def validation_date(prompt):
    """
    EN:Validates the date format (DD.MM.RRRR).
    CZ: Ověřuje formát data (DD.MM.RRRR).
    """
    while True:
        date_str = input(prompt)
        try:
            day, month, year = map(int, date_str.split('.'))
            date(year, month, day)
            return date_str
        except ValueError:
            print("Neplatné datum!!! Zadejte datum ve formátu DD.MM.RRRR.")
            
def validation_float(prompt):
    """
    EN: Validates that the input is a valid float number.
    CZ: Ověřuje, že vstup je platné desetinné číslo.
    """
    while True:
        value = input(prompt).strip()
        if value.lower() == "q":
            return None
        try:
            # EN: Allow comma as decimal separator
            # CZ: Povolit čárku jako desetinný oddělovač
            normalized = value.replace(",", ".")
            return float(normalized)
        except ValueError:
            print("Neplatný vstup!!! Zadejte číslo (např. 100.50).")
