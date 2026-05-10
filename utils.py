

# This file contains "helper functions"

import os
import platform
import subprocess
import json
from fpdf import FPDF
from datetime import datetime



def clear_terminal():
    """
    EN: Clear the console
    CZ: Vymaže konzoli
    """
    os.system("cls" if os.name == "nt" else "clear")
    
    
def continue_prompt():
    """
    EN: Prompt the user to continue
    CZ: Výzva uživatele k pokračování
    """
    input("Stiskni Enter pro pokračování...")
    
    


class AppSession:
    def __init__(self):
        self.current_user = None
        
    def is_logged_in(self):
        """
        EN: Returns True if the user is logged in, otherwise prints an error.
        CZ: Vrátí True, pokud je uživatel přihlášen, jinak vypíše chybu.
        """
        if self.current_user is not None:
            return True
        
        print("\n[!] CHYBA: Tato akce vyžaduje přihlášení.")
        input("Stiskni Enter pro návrat na přihlášení...")
        return False

    def header(self, title):
        """
        EN: Display a formatted header with user information.
        CZ: Zobrazí formátovaný záhlaví s informacemi o uživateli.
        """
        clear_terminal()
        name = self.current_user['name'] if self.current_user else "GUEST"
        role = self.current_user['role'] if self.current_user else "NONE"
        
        print(f"=== {title.upper()} ===")
        print(f"Uživatel: {name} | Role: {role}")
        print("-" * 40 + "\n")

# EN: We create a single global instance of session that we will use throughout the application
# CZ: Vytvoříme jednu globální instanci session, kterou budeme používat v celé aplikaci
session = AppSession()  


def load_json(file_path, default_value=None):
    """
    EN: Load a JSON file. If it doesn't exist or is corrupted, return the provided default value.
    CZ: Načte JSON soubor. Pokud neexistuje nebo je poškozený,
    vrátí zadanou výchozí hodnotu (default_value).
    """
    if default_value is None:
        default_value = []

    try:
        if not os.path.exists(file_path):
            # EN: If the file doesn't exist, we create it immediately with the default value
            # CZ: Pokud soubor neexistuje, rovnou ho vytvoříme s výchozí hodnotou
            save_json(file_path, default_value)
            return default_value
            
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # EN: If there's an error, we return the default value
        # CZ: V případě chyby vracíme přesně to, co zbytek kódu očekává
        return default_value


def get_valid_rate(prompt_text):
        while True:
            value = input(prompt_text).strip().replace(",", ".")
            try:
                return float(value)
            except ValueError:
                print("Chyba: Zadej platné číslo.")


def save_json(file_path, data):
    """
    EN: Saves data to a JSON file.
    CZ: Uloží data do JSON souboru.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Chyba při ukládání souboru {file_path}: {e}")
        print(f"Data nebyla uložena !!!")
        
        
def add_transaction_log(t_type, amount, currency, balance_after, user_name):
    file_path = "cash_register_transactions.json"
    
    # EN: Load existing history (if file does not exist, load_json returns [])
    # CZ: Načte existující historii (pokud soubor neexistuje, load_json vrací [])
    history = load_json(file_path)
    
    # EN: Create a new record
    # CZ: Vytvoříme nový záznam
    new_record = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": t_type,
        "amount": amount,
        "currency": currency,
        "balance_after": balance_after,
        "user": user_name
    }
    
    # EN: Adding to the list
    # CZ: Přidání do seznamu
    history.append(new_record)
    
    # EN: Save back to the file
    # CZ: Uložení zpět do souboru
    save_json(file_path, history)
    

def add_system_log(action, user_name):
    """
    EN: Logs system events (login, logout, password change).
    CZ: Loguje systémové události (login, logout, změna hesla).
    """
    file_path = "system_log.json"
    logs = load_json(file_path)
    
    new_entry = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_name,
        "action": action
    }
    
    logs.append(new_entry)
    save_json(file_path, logs)
    
    
def export_to_pdf(data, title="DOKLAD"):
    """
    EN: Univerzální funkce pro export dat do PDF a jeho otevření.
    CZ: Univerzální funkce pro export dat do PDF a jeho otevření.
    """
    if data is None:
        print("Žádná data pro export do PDF.")
        return None
    
    # EN: Create a PDF instance
    # CZ: Vytvoření instance PDF
    pdf = FPDF()
    pdf.add_page()
    
    # EN: 1. Header
    # CZ: 1. HLAVIČKA
    pdf.set_font("Helvetica", "B", 16) # Helvetica je bezpečnější pro PDF
    pdf.cell(0, 15, title, ln=True, align="C")
    pdf.ln(5)
    
    # EN: 2. TRANSACTION DATA
    # CZ: 2. ÚDAJE O TRANSAKCI
    pdf.set_font("Helvetica", "", 12)
    
    # EN: List of fields we want to display in the PDF with nice labels
    # CZ: Seznam polí, která chceme v PDF prioritně a pod hezkými názvy
    mapping = {
        "id": "ID dokladu",
        "timestamp": "Datum a cas",
        "pokladnik": "Pokladnik",
        "mnozstvi_z": "Klient dal",
        "mena_z": "Mena (Z)",
        "mnozstvi_do": "Klient dostal",
        "mena_do": "Mena (DO)",
        "kurz": "Smenny kurz"
    }

    for key, label in mapping.items():
        if key in data:
            val = data[key]
            # Formátování čísel pro PDF
            if isinstance(val, float): val = f"{val:.2f}"
            pdf.cell(0, 8, f"{label}: {val}", ln=True)

    # EN: 3. AML DATA (if present)
    # CZ: 3. AML ÚDAJE (pokud jsou přítomny)
    if data.get("zakaznik"):
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "IDENTIFIKACE KLIENTA (AML):", ln=True)
        pdf.set_font("Helvetica", "", 11)
        c = data["zakaznik"]
        # EN: We remove diacritics for PDF (if you don't have .ttf font)
        # CZ: Odstraníme diakritiku pro PDF (pokud nemáš .ttf font)
        pdf.cell(0, 8, f"Jmeno: {c['jmeno']} {c['prijmeni']}", ln=True)
        pdf.cell(0, 8, f"Doklad: {c['doklad']} | Narodnost: {c['narodnost']}", ln=True)

    # EN: 4. FOOTER
    # CZ: 4. PATIČKA
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 10, "Dekujeme za navstevu - Smenarna Terminal", ln=True, align="C")
    pdf.cell(0, 8, f"Vytisknuto: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", ln=True, align="C")

    # EN: 5. SAVE
    # CZ: 5. ULOŽENÍ
    if not os.path.exists("receipts_pdf"):
        os.makedirs("receipts_pdf")
    file_path = f"receipts_pdf/posledni_transakce.pdf"
    #file_path = f"receipts_pdf/receipt_{data['id']}.pdf"
    pdf.output(file_path)
    
    # EN: 6. OPEN AUTOMATICALLY (if the system allows it)
    # CZ: 6. OTEVŘENÍ AUTOMATICKY (pokud to systém umožňuje)
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", file_path])
        else:
            subprocess.call(["xdg-open", file_path])
    except:
        print(f"[i] PDF uloženo: {file_path}")

    return file_path


def run_dynamic_menu(title, menu_list):
    """
    EN: Universal function for displaying and controlling any menu.
    CZ: Univerzální funkce pro zobrazení a ovládání jakéhokoliv menu.
    """
    from permissions import has_permissions
    role = session.current_user["role"]
    
    while True:
        clear_terminal()
        session.header(title)
        
        # EN: Filter based on permissions: we only show menu items that the user's role allows
        # CZ: Filtrujeme podle oprávnění: zobrazujeme pouze položky menu, které role uživatele umožňuje
        available = [item for item in menu_list if has_permissions(role, item["perm"])]
        
        if not available:
            print("[!] Nemáte oprávnění pro žádnou akci v této sekci.")
        else:
            for i, item in enumerate(available, 1):
                print(f"{i} - {item['label']}")
        
        print("q - Zpět")
        
        volba = input("\nVaše volba: ").strip().lower()
        if volba == 'q':
            break
            
        try:
            idx = int(volba) - 1
            if 0 <= idx < len(available):
                available[idx]["func"]()
            else:
                raise ValueError
        except (ValueError, IndexError):
            print("\n[!] Neplatná volba.")
            continue_prompt()