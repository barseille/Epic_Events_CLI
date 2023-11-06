import typer
from crm.models.models import USER_ROLES
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from peewee import Model


def is_valid_email(email: str) -> bool:
    """Vérifie si l'email est valide."""
    
    try:
        validate_email(email)
        return True
    
    # Email n'est pas valide selon les critères de validation
    except EmailNotValidError:
        return False


def is_strong_password(password: str) -> bool:
    """Vérifie si le mot de passe a au moins 8 caractères."""
    
    return len(password) >= 8


def is_valid_phone(phone: str) -> bool:
    
    return len(phone) >= 10 and phone.isdigit()


def get_valid_input(prompt_message, validation_function, error_message, default=None):
    """Obtient une entrée valide de l'utilisateur en utilisant une fonction de validation spécifique."""
    
    while True:
        user_input = typer.prompt(prompt_message, default=default)
        if validation_function(user_input):
            return user_input
        
        else:
            typer.echo(error_message)


def is_not_empty(user_input):
    """Vérifie si l'entrée fournie n'est pas vide."""
    
    return user_input != ""

def get_username():
    """Obtenir un nom d'utilisateur valide."""
    
    return get_valid_input("Nom d'utilisateur", is_not_empty, "Le nom d'utilisateur ne peut pas être vide.")


def get_email():
    """Obtenir un email valide."""
    
    return get_valid_input("Email", is_valid_email, "L'e-mail n'est pas valide.")


def get_password():
    """Obtenir un mot de passe valide."""
    
    return get_valid_input("Mot de passe", is_strong_password, "Le mot de passe doit avoir au moins 8 caractères.")


def is_valid_role(role_input):
    """Vérifie si le rôle entré est dans la liste des rôles autorisés."""
    
    return role_input.upper() in USER_ROLES

def get_role():
    """Obtenir un rôle valide."""
    
    return get_valid_input("Rôle", is_valid_role, "Le rôle spécifié n'est pas valide.")



def get_phone():
    """Obtenir un numéro de téléphone valide."""
    
    return get_valid_input("Numéro de téléphone du client", is_valid_phone, "Le numéro de téléphone doit avoir au moins 10 chiffres.")


def get_price() -> int:
    """Demande à l'utilisateur d'entrer un prix jusqu'à ce qu'il entre un entier positif."""
    
    while True:
        price_str = typer.prompt("Prix")
        
        try:
            price = int(price_str)
            if price >= 0:
                return price
            else:
                typer.echo("Le prix doit être un nombre entier positif.")
                
        except ValueError:
            typer.echo("Veuillez entrer un nombre entier valide.")


def is_valid_date(date_str: str, format="%Y-%m-%d") -> bool:
    """Vérifie si la date est valide et n'est pas antérieure à aujourd'hui."""
    
    try:
        input_date = datetime.strptime(date_str, format).date()
        current_date = datetime.now().date()
        return input_date >= current_date
    
    except ValueError:
        return False


def get_start_date() -> str:
    """Obtient une date de début valide de l'utilisateur."""
    
    return get_valid_input(
        prompt_message="Date de début (AAAA-MM-JJ)",
        validation_function=is_valid_date,
        error_message="La date de début doit être au format AAAA-MM-JJ et ne peut pas être antérieure à aujourd'hui."
    )


def is_end_date_valid(end_date_str: str, start_date_str: str) -> bool:
    """Vérifie si la date de fin est valide et postérieure à la date de début."""
    
    try:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        return end_date >= start_date
    
    except ValueError:
        return False


def get_end_date(start_date_str: str) -> str:
    """Obtient une date de fin valide de l'utilisateur, qui doit être postérieure à la date de début."""
    
    def validation_function(end_date_str):
        return is_end_date_valid(end_date_str, start_date_str)
    
    return get_valid_input(
        prompt_message="Date de fin (AAAA-MM-JJ)",
        validation_function=validation_function,
        error_message="La date de fin doit être au format AAAA-MM-JJ et postérieure à la date de début."
    )

    
def get_boolean_input(prompt_message: str) -> bool:
    """Obtient une entrée booléenne valide de l'utilisateur."""
    
    while True:
        
        user_input = typer.prompt(prompt_message).lower()
        if user_input in ['oui', 'non']:
            return user_input == 'oui'
        else:
            typer.echo("Réponse invalide. Répondez par 'Oui' ou 'Non'.")


def get_valid_id(model: Model, prompt_message: str, validation_function) -> int:
    """
    Obtient un ID valide de l'utilisateur pour un modèle donné en utilisant une fonction de validation.
    """
    
    while True:
        user_input = typer.prompt(prompt_message)
        
        try:
            user_id = int(user_input)
            # Vérifie d'abord si l'ID correspond à un enregistrement existant.
            model.get_by_id(user_id)
            # Ensuite, utilise la fonction de validation pour des vérifications supplémentaires.
            if validation_function(user_id):
                return user_id
            else:
                typer.echo("Ce client a déjà un contrat.")
                
        except ValueError:
            typer.echo("Veuillez entrer un nombre entier valide.")
            
        except model.DoesNotExist:
            typer.echo("Aucun client trouvé à cet ID.")

          
def valid_event_date(date_str: str, start_str: str, end_str: str) -> bool:
    """ Vérifie si la date de l'événement est pendant la durée du contrat"""
    
    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    start = datetime.strptime(start_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()
    return start <= event_date <= end


def valid_event_date_for_start(date_str: str, start_str: str, end_str: str) -> bool:
    """ Vérifie si la date de l'événement est pendant la durée du contrat"""
    
    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    start = datetime.strptime(start_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()
    return start <= event_date <= end


def valid_event_date_for_end(date_str: str, start_event_str: str, end_str: str) -> bool:
    """ Vérifie si la date de fin de l'événement est après la date de début et avant la fin du contrat"""
    
    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    start_event = datetime.strptime(start_event_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()
    return start_event <= event_date <= end


def get_event_start(start_str: str, end_str: str) -> str:
    """ Demande la date de début de l'événement"""
    
    def validation_function(date_str):
        return valid_event_date_for_start(date_str, start_str, end_str)
    return get_valid_input(
        "Début de l'événement (AAAA-MM-JJ)",
        validation_function,
        "La date doit être durant la période du contrat."
    )

def get_event_end(start_event_str: str, end_str: str) -> str:
    """ Demande la date de fin de l'événement"""
    
    def validation_function(date_str):
        return valid_event_date_for_end(date_str, start_event_str, end_str)
    return get_valid_input(
        "Fin de l'événement (AAAA-MM-JJ)",
        validation_function,
        "La fin doit être après le début et avant la fin du contrat."
    )