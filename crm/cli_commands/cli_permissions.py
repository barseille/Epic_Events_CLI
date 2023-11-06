import json


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


def check_role(role):
    """
    Vérifie si l'utilisateur authentifié a le rôle spécifié, insensible à la casse.
    """
    user_info = load_user_info()
    
    # Convertit les deux chaînes en minuscules avant de les comparer pour l'insensibilité à la casse.
    return is_authenticated() and user_info.get('role', '').lower() == role.lower()


def is_commercial():
    """
    Vérifie si l'utilisateur authentifié a le rôle 'Commercial'.
    """
    return check_role('COMMERCIAL')


def is_administration():
    """
    Vérifie si l'utilisateur authentifié a le rôle 'Administration'.
    """
    return check_role('ADMINISTRATION')


def is_support():
    """
    Vérifie si l'utilisateur authentifié a le rôle 'Support'.
    """
    return check_role('SUPPORT')