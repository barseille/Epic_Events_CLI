import typer
import bcrypt
import json
import os
from crm.models.models import User


app = typer.Typer()


def verify_user(email: str, password: str) -> bool:
    """
    Vérifie l'existence d'un utilisateur avec l'email spécifié et
    si le mot de passe fourni correspond à celui haché enregistré dans la base de données.
    """
    try:
        # Utilise la méthode get_or_none pour récupérer l'utilisateur correspondant à l'email donné.
        # Retourne l'utilisateur si trouvé, sinon None.
        user = User.get_or_none(User.email == email)
        
        if user:
            # Compare le mot de passe fourni avec le mot de passe haché de l'utilisateur trouvé.
            # Encode les mots de passe en UTF-8 avant la comparaison.
            return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        
    except Exception as e:
        typer.echo(f"Une erreur est survenue lors de la vérification de l'utilisateur: {e}")
        
    return False



def login(email: str, password: str):
    """
    Connecte l'utilisateur en vérifiant son email et mot de passe.
    """
    try:
        # La fonction verify_user retourne True si l'email et le mot de passe sont corrects.
        if verify_user(email, password):
            
            # La fonction User.get est utilisée pour récupérer l'objet User complet associé à cet email.
            user = User.get(User.email == email)
            
            typer.echo("Authentification réussie.")
            
            # Enregistre les informations de l'utilisateur pour la session actuelle.
            save_user_info(user.id, user.username, user.email, user.role)
            
        else:
            typer.echo("Email ou mot de passe incorrecte !")
            
    except Exception as e:
        typer.echo(f"Une erreur est survenue lors de la tentative de connexion: {e}")


def save_user_info(user_id, username, email, role):
    """
    Enregistre les informations de l'utilisateur :
    - L'identifiant de l'utilisateur.
    - Le nom d'utilisateur.
    - L'email de l'utilisateur.
    - Le rôle de l'utilisateur.
    """
    try:
        with open("config.json", "w") as f:
            json.dump({"user_id": user_id, "username": username, "email": email, "role": role}, f, indent=4)
            
    # IOError est levée en cas de problème d'accès au fichier
    except IOError as e:
        typer.echo(f"Une erreur est survenue lors de l'enregistrement des informations de l'utilisateur: {e}")


def load_user_info():
    """
    Charge les informations de l'utilisateur et 
    retour les informations de l'utilisateur 
    si le fichier existe et est valide, None sinon.
    """
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        typer.echo("Aucun utilisateur n'est actuellement connecté.")
        return None
    except json.JSONDecodeError:
        typer.echo("Le fichier de configuration est corrompu.")
        return None


def clear_user_info():
    """
    Efface les informations de l'utilisateur pour déconnecter l'utilisateur.
    """
    try:
        # Vérifie si le fichier config.json existe et le supprime pour déconnecter l'utilisateur.
        if os.path.exists("config.json"):
            os.remove("config.json")
            typer.echo("Déconnexion réussie.")
        else:
            typer.echo("Aucun utilisateur n'est actuellement connecté.")
    except Exception as e:
        typer.echo(f"Une erreur est survenue lors de la tentative de déconnexion: {e}")


@app.command()
def logout():
    """
    Déconnecte l'utilisateur actuel en effaçant ses informations de session.
    """
    user_info = load_user_info()
    if user_info:
        clear_user_info()
    else:
        typer.echo("Aucun utilisateur n'est actuellement connecté.")

       
@app.command()
def authenticate(email: str = typer.Option(..., prompt="Email"), 
                 password: str = typer.Option(..., prompt="Mot de passe", hide_input=True)):
    """
    Authentifie l'utilisateur en demandant l'email et le mot de passe,
    puis en appelant la fonction de connexion.
    ... : argument obligatoire
    """
    login(email, password)

