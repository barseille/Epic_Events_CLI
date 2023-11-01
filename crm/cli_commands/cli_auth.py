import typer
import bcrypt
import json
import os
from crm.models.models import User

app = typer.Typer()


def verify_user(email: str, password: str) -> bool:
    """
    Vérifie si l'email et le mot de passe correspondent à un utilisateur dans la base de données.
    """
    user = User.get_or_none(User.email == email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return True
    return False

def login(email: str, password: str):
    """
    Authentifie un utilisateur en vérifiant son email et son mot de passe.
    """
    if verify_user(email, password):
        user = User.get(User.email == email)
        typer.echo("Authentification réussie.")
        save_user_info(user.id, user.username, user.email, user.role)
    else:
        typer.echo("Email ou mot de passe incorrecte !")

def save_user_info(user_id, username, email, role):
    with open("config.json", "w") as f:
        json.dump({"user_id": user_id, "username": username, "email": email, "role": role}, f, indent=4)


@app.command()
def authenticate(email: str = typer.Option(..., prompt="Email"), 
                 password: str = typer.Option(..., prompt="Mot de passe")):
    login(email, password)
    

def load_user_info():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def clear_user_info():
    if os.path.exists("config.json"):
        os.remove("config.json")
        typer.echo("Déconnexion réussie.")
    else:
        typer.echo("Aucun utilisateur n'est actuellement connecté.")

@app.command()
def logout():
    """
    Déconnecte l'utilisateur actuel.
    """
    user_info = load_user_info()
    if user_info:
        clear_user_info()
    else:
        typer.echo("Aucun utilisateur n'est actuellement connecté.")

