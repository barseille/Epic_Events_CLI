from crm.cli_commands.cli_user import app as user_app
from crm.cli_commands.cli_auth import app as auth_app
from crm.cli_commands.cli_commercial import app as commercial_app
from crm.cli_commands.cli_administration import app as administration_app
from crm.cli_commands.cli_support import app as support_app

import typer

app = typer.Typer()

app.add_typer(user_app, name="user")
app.add_typer(auth_app, name="auth")
app.add_typer(commercial_app, name="commercial")
app.add_typer(administration_app, name="administration")
app.add_typer(support_app, name="support")


if __name__ == "__main__":
    """
    Point d'entrée principal de l'application CLI CRM.

    Ce module intègre les sous-commandes des différents domaines :
    - l'authentification
    - le commercial
    - l'administration
    - le support.
    """
    app()
