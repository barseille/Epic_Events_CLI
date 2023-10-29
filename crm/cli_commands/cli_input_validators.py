import re
import typer
from crm.models.models import USER_ROLES
from datetime import datetime



def is_valid_email(email: str) -> bool:
    """Vérifie si l'email est valide."""
    regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w+$'
    return bool(re.search(regex, email))


def is_strong_password(password: str) -> bool:
    """Vérifie si le mot de passe a au moins 8 caractères."""
    return len(password) >= 8


def is_valid_phone(phone: str) -> bool:
    return len(phone) >= 10


def is_valid_date(date_str: str, format="%Y-%m-%d") -> bool:
    """Vérifie si la date est valide selon le format donné."""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False



def get_username():
    """Obtenir un nom d'utilisateur valide."""
    while True:
        username = typer.prompt("Nom d'utilisateur")
        if username:
            return username
        else:
            typer.echo("Le nom d'utilisateur ne peut pas être vide.")


def get_email():
    """Obtenir un email valide."""
    while True:
        email = typer.prompt("Email")
        if is_valid_email(email):
            return email
        else:
            typer.echo("L'e-mail n'est pas valide.")


def get_password():
    """Obtenir un mot de passe valide."""
    while True:
        password = typer.prompt("Mot de passe")
        if is_strong_password(password):
            return password
        else:
            typer.echo("Le mot de passe doit avoir au moins 8 caractères.")


def get_role():
    """Obtenir un rôle valide."""
    while True:
        role = typer.prompt("Rôle")
        if role.upper() in USER_ROLES:
            return role.upper()
        else:
            typer.echo("Le rôle spécifié n'est pas valide.")

           
def get_phone():
        phone = typer.prompt("Numéro de téléphone du client")
        if is_valid_phone(phone):
            return phone
        else:
            typer.echo("Le numéro de téléphone doit avoir au moins 10 chiffres.")

