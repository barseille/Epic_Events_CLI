import typer
from crm.models.models import USER_ROLES
from datetime import datetime

from email_validator import validate_email, EmailNotValidError
from peewee import DoesNotExist, Model

def is_valid_email(email: str) -> bool:
    """Vérifie si l'email est valide."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_strong_password(password: str) -> bool:
    """Vérifie si le mot de passe a au moins 8 caractères."""
    return len(password) >= 8


def is_valid_phone(phone: str) -> bool:
    return len(phone) >= 10 and phone.isdigit()


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


def get_price():
    """Obtenir un prix valide."""
    while True:
        price_str = typer.prompt("Prix")
        try:
            price = int(price_str)
            if price >= 0:
                return price
            else:
                typer.echo("Le prix doit être un nombre entier positif.")
        except ValueError:
            typer.echo("Veuillez entrer un nombre valide.")



def is_valid_date(date_str: str, format="%Y-%m-%d") -> bool:
    """
    Vérifie si la date fournie sous forme de chaîne de caractères est valide selon le format donné.
    
    Utilise la fonction datetime.strptime pour tenter de convertir la chaîne de caractères en un objet datetime.
    - Si la conversion réussit, la chaîne est considérée comme une date valide et la fonction retourne True.
    - Si la conversion échoue (par exemple, si la chaîne n'est pas au format attendu), la fonction retourne False.
    
    Args:
    date_str (str): La date sous forme de chaîne de caractères à valider.
    format (str, optional): Le format de date attendu. Par défaut, il est fixé à "%Y-%m-%d" (année-mois-jour).
    
    Returns:
    bool: True si la date est valide, False sinon.
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def get_valid_date(prompt_message: str) -> str:
    """
    Demande à l'utilisateur de saisir une date et valide cette entrée.
    
    Paramètres:
    - prompt_message (str): Le message affiché à l'utilisateur pour lui demander de saisir une date.
    
    Retourne:
    - str: La date valide saisie par l'utilisateur au format 'YYYY-MM-DD'.
    
    Fonctionnement:
    1. Une boucle while continue de demander une date à l'utilisateur jusqu'à ce qu'une date valide soit saisie.
    2. Utilise la fonction is_valid_date pour vérifier si la date saisie est au bon format.
    3. Vérifie si la date saisie est égale ou postérieure à la date d'aujourd'hui.
    4. Si les deux conditions sont remplies, retourne la date saisie.
    5. Sinon, affiche un message d'erreur et recommence.
    """
    while True:
        date_str = typer.prompt(prompt_message)
        today = datetime.now().strftime('%Y-%m-%d')
        if is_valid_date(date_str) and date_str >= today:
            return date_str
        else:
            typer.echo("La date doit être au format YYYY-MM-DD et ne peut pas être antérieure à aujourd'hui.")


def get_start_date():
    """Obtenir une date de début valide."""
    return get_valid_date("Date de début (YYYY-MM-DD)")

def get_end_date(start_date=None):
    """Obtenir une date de fin valide."""
    while True:
        end_date = get_valid_date("Date de fin (YYYY-MM-DD)")
        if start_date and end_date <= start_date:
            typer.echo("La date de fin doit être postérieure à la date de début.")
        else:
            return end_date


def get_boolean_input(prompt: str):
    while True:
        response = typer.prompt(prompt)
        if response.lower() == "oui":
            return True
        elif response.lower() == "non":
            return False
        else:
            typer.echo("Réponse invalide. Répondez par 'Oui' ou 'Non'.")
            
            


def get_valid_id(model_type: type[Model], prompt_message: str, validation_function=None):
    """Obtenir un ID valide"""
    while True:
        user_input = typer.prompt(prompt_message)
        try:
            user_input_id = int(user_input)
            db_entity = model_type.get_by_id(user_input_id)
            
            if validation_function:
                if not validation_function(db_entity):
                    continue
            
            return user_input_id
        except ValueError:
            typer.echo(f"Entrez un nombre entier positif")
        except DoesNotExist:
            typer.echo(f"{model_type.__name__} non trouvé.")



