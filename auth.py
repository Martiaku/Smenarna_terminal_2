import bcrypt
from utils import load_json, save_json


def hash_password(password):
    """
    EN: Creates a hash with a random salt.
    CZ: Vytvoří hash s náhodnou solí.
    EN: Bcrypt automatically includes the salt in the resulting string.
    CZ: Bcrypt automaticky přidá sůl přímo do výsledného řetězce.
    """
    # EN: Generate salt and hash the password
    # CZ: Generujeme sůl a hashujeme heslo
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(plain_text_password, hashed_password):
    """
    EN: Checks if the provided password matches the stored hash.
    CZ: Zkontroluje, zda zadané heslo odpovídá uloženému hashi.
    """
    return bcrypt.checkpw(
        plain_text_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )


def patch_user_password(username, old_password, new_password):
    users = load_json("users.json")
    success = False
    
    for user in users:
        if user["name"] == username:
            # EN: Use check_password instead of direct comparison
            # CZ: Použijeme check_password místo přímého porovnání
            if check_password(old_password, user["password"]):
                user["password"] = hash_password(new_password)
                success = True
                break
    
    if success:
        save_json("users.json", users)
        return True
    return False