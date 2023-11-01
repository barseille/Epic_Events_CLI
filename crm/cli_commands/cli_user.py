import typer
import bcrypt
from crm.models.models import User, db
from crm.cli_commands.cli_input_validators import get_username, get_email, get_password, get_role  

app = typer.Typer()


@app.command()
def add_user():
    """Ajoute un nouvel utilisateur."""

    while True:
        username = get_username()
        existing_user_with_username = User.select().where(User.username == username).first()
        if existing_user_with_username:
            typer.echo("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
        else:
            break

    while True:
        email = get_email()
        existing_user_with_email = User.select().where(User.email == email).first()
        if existing_user_with_email:
            typer.echo("Cet email est déjà utilisé par un autre utilisateur. Veuillez en utiliser un différent.")
        else:
            break

    password = get_password()
    role = get_role()

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
