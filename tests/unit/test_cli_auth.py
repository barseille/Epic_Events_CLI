from typer.testing import CliRunner
from unittest.mock import patch
import crm.cli_commands.cli_auth as cli_auth
import json
import os

runner = CliRunner()

def test_logout_user_logged_in():
    # Prépare un fichier config.json pour simuler un utilisateur connecté
    with open("config.json", "w") as f:
        json.dump({"user_id": 1, "username": "testuser", "email": "test@example.com", "role": "admin"}, f)

    # Exécute la commande logout
    result = runner.invoke(cli_auth.app, ["logout"])

    # Vérifie que le fichier config.json a été supprimé et que la sortie est correcte
    assert not os.path.exists("config.json")
    assert "Déconnexion réussie." in result.output

def test_logout_no_user_logged_in():
    # Si le fichier config.json n'existe pas
    if os.path.exists("config.json"):
        os.remove("config.json")

    # Exécute la commande logout
    result = runner.invoke(cli_auth.app, ["logout"])

    # Vérifie la sortie pour un utilisateur non connecté
    assert "Aucun utilisateur n'est actuellement connecté." in result.output
