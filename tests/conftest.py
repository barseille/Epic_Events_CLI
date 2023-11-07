# conftest.py
import pytest
from peewee import SqliteDatabase, Model
from crm.models.models import User, Client, Contrat, Event

# Créer une instance de base de données en mémoire pour les tests
test_database = SqliteDatabase(':memory:')

class TestModel(Model):
    class Meta:
        database = test_database

# Utiliser une fixture pour configurer la base de données avant chaque test
@pytest.fixture(autouse=True)
def setup_database():
    # Connecter la base de données de test
    test_database.bind([User, Client, Contrat, Event], bind_refs=False, bind_backrefs=False)
    test_database.connect()
    test_database.create_tables([User, Client, Contrat, Event])

    yield

    # Nettoyer la base de données après chaque test
    test_database.drop_tables([User, Client, Contrat, Event])
    test_database.close()
