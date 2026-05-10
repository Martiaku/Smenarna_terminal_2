# Směnárna – Terminálová aplikace

Tento projekt je jednoduchá terminálová aplikace pro správu směnárny. Umožňuje správu uživatelů, pokladny, měn a evidenci transakcí.

## Funkce
- Převod měn
- Správa měn a kurzů
- Správa pokladny (příjem/výdej peněz)
- Správa uživatelů a jejich oprávnění
- Audit log a historie transakcí
- Bezpečné ukládání hesel (bcrypt)
- Testy pomocí pytest

## Požadavky
- Python 3.8+
- Závislosti uvedené v `requirements.txt`

## Instalace
1. Naklonujte si repozitář nebo stáhněte projekt.
2. Vytvořte a aktivujte virtuální prostředí:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

## Spuštění
Spusťte hlavní soubor (např. `login.py` nebo `homepage.py`):
```bash
python login.py
```

## Spuštění testů
Testy spustíte příkazem:
```bash
pytest
```

## Struktura projektu
- `Users/` – správa uživatelů
- `Cash_desk/` – pokladna
- `Currency/` – měny a kurzy
- `tests/` – testy
- `utils.py` – pomocné funkce

## Autor
Martin Kučera

---

# Currency Exchange – Terminal Application

This project is a simple terminal application for managing a currency exchange office. It allows user, cash desk, and currency management, as well as transaction logging.

## Features
- Currency exchange
- Currency and rate management
- Cash desk management (deposit/withdrawal)
- User and permission management
- Audit log and transaction history
- Secure password storage (bcrypt)
- Tests using pytest

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation
1. Clone the repository or download the project.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running
Run the main file (e.g. `login.py` or `homepage.py`):
```bash
python login.py
```

## Running tests
Run tests with:
```bash
pytest
```

## Project structure
- `Users/` – user management
- `Cash_desk/` – cash desk
- `Currency/` – currencies and rates
- `tests/` – tests
- `utils.py` – utility functions

## Author
Martin Kučera

