from exchange_money import exchange_money
from submenu_currency import submenu_currency
from Cash_desk.cash_desk_managment import show_balance
from Currency.course_list_currency import course_list_currency
from submenu_cash_desk import submenu_cash_desk
from submenu_user import submenu_user
from last_10_view import reprint_receipt
from audit_log import show_audit_logs
from Users.add_user import add_user
from Users.users_change_password import users_change_password
from Users.edit_permissions import edit_permissions
from Currency.add_currency import add_currency
from Currency.change_of_course import change_of_course
from Cash_desk.add_money import add_money
from Cash_desk.withdraw_money import withdraw_money
from Users.view_permissions import print_permission_matrix

# EN: Main menu definitions
# CZ: Hlavní menu definice
MENU_DEFINITIONS = [
    {"label": "Převod měn", "perm": "exchange_currency", "func": exchange_money},
    {"label": "Správa měn", "perm": "manage_currency", "func": submenu_currency},
    {"label": "Pokladna", "perm": "cash_desk", "func": show_balance},
    {"label": "Kurzovní lístek", "perm": "course_list", "func": course_list_currency},
    {"label": "Správa pokladny", "perm": "manage_cash_desk", "func": submenu_cash_desk},
    {"label": "Správa uživatelů", "perm": "manage_user", "func": submenu_user},
    {"label": "Posledních 10 transakcí", "perm": "last_10_transactions", "func": reprint_receipt},
    {"label": "Audit Log", "perm": "audit_log", "func": show_audit_logs},
 
]


# EN: Sub-menu for cash desk
# CZ: Sub-menu pro pokladnu
CASH_DESK_MENU = [
    {"label": "Příjem do pokladny", "perm": "add_money", "func": add_money},
    {"label": "Výdej z pokladny", "perm": "withdraw_money", "func": withdraw_money},
]

# EN: Sub-menu for currencies
# CZ: Sub-menu pro měny
CURRENCY_MENU = [
    {"label": "Změna kurzu", "perm": "change_of_course", "func": change_of_course},
    {"label": "Přidání měny", "perm": "add_currency", "func": add_currency},
    {"label": "Seznam kurzů měn", "perm": "course_list", "func": course_list_currency},
]

# EN: Sub-menu for users
# CZ: Sub-menu pro uživatele
USER_MENU = [
    {"label": "Změna hesla", "perm": "change_password", "func": users_change_password},
    {"label": "Přidání uživatele", "perm": "add_user", "func": add_user},
    {"label": "Úprava práv", "perm": "edit_permissions", "func": edit_permissions},
    {"label": "Zobrazení práv", "perm": "view_permissions", "func": print_permission_matrix},
]

# EN: Combine all menus into one list for easy searching
# CZ: Spojíme všechna menu do jednoho seznamu pro snadné vyhledávání
ALL_MENUS = MENU_DEFINITIONS + CASH_DESK_MENU + CURRENCY_MENU + USER_MENU

# EN: Create a dictionary { "perm_key": "Human-readable label" }
# CZ: Vytvoříme slovník { "perm_key": "Lidský štítek" }
PERM_LABELS = {item["perm"]: item["label"] for item in ALL_MENUS}

 