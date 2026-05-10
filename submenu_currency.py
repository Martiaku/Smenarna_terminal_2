def submenu_currency():
    from menu_config import CURRENCY_MENU
    from utils import run_dynamic_menu
    
    run_dynamic_menu("MENU - Správa měn", CURRENCY_MENU)