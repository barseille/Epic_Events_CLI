import typer
import bcrypt
import json
from crm.models.models import User

app = typer.Typer()


def login(email: str, password: str):
    user = User.get_or_none(User.email == email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
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
