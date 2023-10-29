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