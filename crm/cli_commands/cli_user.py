import typer
import bcrypt
from crm.models.models import User, db
from crm.cli_commands.cli_input_validators import get_username, get_email, get_password, get_role  

app = typer.Typer()


@app.command()
def add_user():
    """
    Ajoute un nouvel utilisateur en s'assurant que le nom d'utilisateur et l'email ne sont pas déjà utilisés.
    Le mot de passe est hashé avant d'être stocké.
    """

    # Obtenir un nom d'utilisateur valide et unique
    username = get_username()
    while User.get_or_none(User.username == username):
        typer.echo("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
        username = get_username()

    # Obtenir un email valide et unique
    email = get_email()
    while User.get_or_none(User.email == email):
        typer.echo("Cet email est déjà utilisé par un autre utilisateur. Veuillez en utiliser un différent.")
        email = get_email()

    # Obtenir un mot de passe valide
    password = get_password()

    # Obtenir un rôle valide
    role = get_role()

    # Hasher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Ajouter l'utilisateur à la base de données
    try:
        with db.atomic():
            User.create(
                username=username,
                email=email,
                role=role,
                password=hashed_password.decode('utf-8')
            )
        typer.echo(f"Utilisateur {username} ajouté avec succès avec le rôle {role}.")
        
    except Exception as e:
        typer.echo(f"Une erreur s'est produite lors de l'ajout de l'utilisateur : {e}")
