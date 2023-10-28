import json
import os


def load_user_info():
    """Charge les informations de l'utilisateur à partir de config.json."""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def is_authenticated():
    """Vérifie si l'utilisateur est authentifié."""
    return bool(load_user_info())


# Fonction pour vérifier si l'utilisateur a le rôle 'Commercial'
def is_commercial():
    user = load_user_info()
    return is_authenticated() and user.get('role') == 'COMMERCIAL'


# Fonction pour vérifier si l'utilisateur a le rôle 'Administration'
def is_administration():
    user = load_user_info()
    return is_authenticated() and user.get('role') == 'ADMINISTRATION'


# Fonction pour vérifier si l'utilisateur a le rôle 'Support'
def is_support():
    user = load_user_info()
    return is_authenticated() and user.get('role') == 'SUPPORT'
