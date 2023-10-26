from crm.cli_commands.cli_user import app as user_app
from crm.cli_commands.cli_auth import app as auth_app
import typer

app = typer.Typer()

app.add_typer(user_app, name="user")
app.add_typer(auth_app, name="auth")

if __name__ == "__main__":
    app()
