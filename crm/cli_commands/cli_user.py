import typer
import bcrypt
from crm.models.models import User, db
from crm.cli_commands.cli_input_validators import get_username, get_email, get_password, get_role  

app = typer.Typer()

@app.command()
def add_user():
    """Ajoute un nouvel utilisateur."""
    username = get_username()
    email = get_email()
    password = get_password()
    role = get_role()

    # Vérifier si l'utilisateur existe déjà
    existing_user = User.get_or_none(User.email == email)
    if existing_user:
        typer.echo("Un utilisateur avec cet email existe déjà.")
        return

    existing_user_by_username = User.get_or_none(User.username == username)
    if existing_user_by_username:
        typer.echo("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        return

    # Hasher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Ajouter l'utilisateur à la base de données
    try:
        with db.atomic():
            User.create(
                username=username,
                role=role,
                email=email,
                password=hashed_password.decode('utf-8')
            )
        typer.echo(f"Utilisateur {username} ajouté avec succès avec le rôle {role}.")
    except Exception as e:
        typer.echo(f"Une erreur s'est produite : {e}")


# import typer
# import bcrypt
# from crm.models.models import User, db
# import re

# from crm.models.models import USER_ROLES



# app = typer.Typer()


# def is_valid_email(email: str) -> bool:
#     """Vérifie si l'email est valide."""
#     regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w+$'
#     return bool(re.search(regex, email))


# def is_strong_password(password: str) -> bool:
#     """Vérifie si le mot de passe a au moins 8 caractères."""
#     return len(password) >= 8


# def get_username():
#     """Obtenir un nom d'utilisateur valide."""
#     while True:
#         username = typer.prompt("Nom d'utilisateur")
#         if username:
#             return username
#         else:
#             typer.echo("Le nom d'utilisateur ne peut pas être vide.")


# def get_email():
#     """Obtenir un email valide."""
#     while True:
#         email = typer.prompt("Email")
#         if is_valid_email(email):
#             return email
#         else:
#             typer.echo("L'e-mail n'est pas valide.")


# def get_password():
#     """Obtenir un mot de passe valide."""
#     while True:
#         password = typer.prompt("Mot de passe")
#         if is_strong_password(password):
#             return password
#         else:
#             typer.echo("Le mot de passe doit avoir au moins 8 caractères.")


# def get_role():
#     """Obtenir un rôle valide."""
#     while True:
#         role = typer.prompt("Rôle")
#         if role.upper() in USER_ROLES:
#             return role.upper()
#         else:
#             typer.echo("Le rôle spécifié n'est pas valide.")



# @app.command()
# def add_user():
#     """Ajoute un nouvel utilisateur."""
#     username = get_username()
#     email = get_email()
#     password = get_password()
#     role = get_role()

#     # Vérifier si l'utilisateur existe déjà
#     existing_user = User.get_or_none(User.email == email)
#     if existing_user:
#         typer.echo("Un utilisateur avec cet email existe déjà.")
#         return

#     existing_user_by_username = User.get_or_none(User.username == username)
#     if existing_user_by_username:
#         typer.echo("Un utilisateur avec ce nom d'utilisateur existe déjà.")
#         return

#     # Hasher le mot de passe
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     # Ajouter l'utilisateur à la base de données
#     try:
#         with db.atomic():
#             User.create(
#                 username=username,
#                 role=role,
#                 email=email,
#                 password=hashed_password.decode('utf-8')
#             )
#         typer.echo(f"Utilisateur {username} ajouté avec succès avec le rôle {role}.")
#     except Exception as e:
#         typer.echo(f"Une erreur s'est produite : {e}")
