import pytest
from crm.models.models import User, Client, Contrat, Event
from datetime import datetime

# Dates statiques pour les tests
DATE_DEBUT_CONTRAT = datetime(2023, 11, 1)
DATE_FIN_CONTRAT = datetime(2023, 12, 1)
DATE_DEBUT_EVENEMENT = datetime(2023, 11, 15)
DATE_FIN_EVENEMENT = datetime(2023, 11, 20)

# Création de fixtures pour les tests avec des données fictives.

@pytest.fixture
def mock_user_commercial():
    # Création d'un utilisateur avec le rôle commercial.
    user_commercial = User(username="commercial_user", 
                           email="commercial@gmail.com", 
                           role="COMMERCIAL", 
                           password="test_password")
    return user_commercial

@pytest.fixture
def mock_user_admin():
    # Création d'un utilisateur avec le rôle administration.
    user_admin = User(username="admin_user", 
                      email="admin@gmail.com", 
                      role="ADMINISTRATION", 
                      password="test_password")
    return user_admin

@pytest.fixture
def mock_user_support():
    # Création d'un utilisateur avec le rôle support.
    user_support = User(username="support_user", 
                        email="support@gmail.com", 
                        role="SUPPORT", 
                        password="test_password")
    return user_support

@pytest.fixture
def mock_client(mock_user_commercial):
    # Création d'un client avec un contact commercial associé.
    client = Client(name="Client_test", 
                    email="clienttest@gmail.com", 
                    phone="0123456789", 
                    company_name="Company A", 
                    commercial_contact=mock_user_commercial)
    return client

@pytest.fixture
def mock_contrat_in_progress(mock_client):
    # Création d'un contrat en cours pour le client.
    contrat_in_progress = Contrat(client=mock_client, 
                                  status="EN_COURS", 
                                  start_date=DATE_DEBUT_CONTRAT, 
                                  end_date=DATE_FIN_CONTRAT, 
                                  price=1000, 
                                  payment_received=False, 
                                  is_signed=True)
    return contrat_in_progress

@pytest.fixture
def mock_contrat_completed(mock_client):
    # Création d'un contrat terminé pour le client.
    contrat_completed = Contrat(client=mock_client, 
                                status="TERMINE", 
                                start_date=DATE_DEBUT_CONTRAT, 
                                end_date=DATE_FIN_CONTRAT, 
                                price=2000, 
                                payment_received=True, 
                                is_signed=True)
    return contrat_completed

@pytest.fixture
def mock_event(mock_contrat_in_progress, mock_user_support):
    # Création d'un événement lié au contrat en cours.
    event = Event(contrat=mock_contrat_in_progress, 
                  support_contact=mock_user_support, 
                  start_date=DATE_DEBUT_EVENEMENT, 
                  end_date=DATE_FIN_EVENEMENT, 
                  attendees=50, notes="Test unitaire des événements")
    return event
