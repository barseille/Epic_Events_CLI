import typer
import bcrypt
from crm.models.models import User, db
import re

app = typer.Typer()


def is_valid_email(email: str) -> bool:
    regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w+$'
    return bool(re.search(regex, email))


def is_strong_password(password: str) -> bool:
    return len(password) >= 8


@app.command()
def add_user():
    while True:
        username = typer.prompt("Nom d'utilisateur")
        if username:
            break
        else:
            typer.echo("Le nom d'utilisateur ne peut pas être vide.")

    while True:
        email = typer.prompt("Email")
        if is_valid_email(email):
            break
        else:
            typer.echo("L'e-mail n'est pas valide.")

    while True:
        password = typer.prompt("Mot de passe")
        if is_strong_password(password):
            break
        else:
            typer.echo("Le mot de passe doit avoir au moins 8 caractères.")

    while True:
        role = typer.prompt("Rôle")
        if role.upper() in ['COMMERCIAL', 'ADMINISTRATION', 'SUPPORT']:
            break
        else:
            typer.echo("Le rôle spécifié n'est pas valide.")

    try:     
        # Vérifie si l'utilisateur existe déjà
        existing_user = User.get_or_none(User.email == email)
        if existing_user:
            typer.echo("Un utilisateur avec cet email existe déjà.")
            return

        # Vérifie si l'utilisateur existe déjà par nom d'utilisateur
        existing_user_by_username = User.get_or_none(User.username == username)
        if existing_user_by_username:
            typer.echo("Un utilisateur avec ce nom d'utilisateur existe déjà.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Crée le nouvel utilisateur
        with db.atomic():
            User.create(
                username=username,
                # que ce soit en minuscules, majuscules ou une combinaison des deux), 
                # il sera converti en majuscules avant d'être inséré dans la base de données
                role=role.upper(),
                email=email,
                password=hashed_password.decode('utf-8')
            )
        typer.echo(f"Utilisateur {username} ajouté avec succès avec le rôle {role.upper()}.")
        
    except Exception as e:
        typer.echo(f"Une erreur s'est produite : {e}")
