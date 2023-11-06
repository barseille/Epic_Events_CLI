from typer.testing import CliRunner
from crm.__main__ import app
import pytest

runner = CliRunner()

@pytest.fixture
def mock_user_functions(mocker):
    
    # Utilise mocker pour simuler les fonctions
    mocker.patch('crm.cli_commands.cli_user.get_username', return_value='new_user')
    mocker.patch('crm.cli_commands.cli_user.get_email', return_value='new_user@example.com')
    mocker.patch('crm.cli_commands.cli_user.get_password', return_value='password123')
    mocker.patch('crm.cli_commands.cli_user.get_role', return_value='admin')
    mocker.patch('crm.models.models.User.get_or_none', return_value=None)

def test_add_user_success(mock_user_functions):
    # Exécute la commande pour ajouter un utilisateur
    result = runner.invoke(app, ["user", "add-user"])

    # Vérifie que l'utilisateur a été ajouté avec succès
    assert "Utilisateur new_user ajouté avec succès avec le rôle admin." in result.output
