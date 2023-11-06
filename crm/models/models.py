from peewee import Model, CharField, ForeignKeyField, DateTimeField, IntegerField, BooleanField, TextField, SQL
from datetime import datetime
# déclenché après qu'un enregistrement a été sauvegardé dans la bdd.
from playhouse.signals import post_save
from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))

# Vérification des variables d'environnement
if not all([DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT]):
    raise EnvironmentError("Variables d'environnement sont manquantes! Vérifiez votre fichier .env")


db = PostgresqlDatabase(
    DB_NAME,  # Nom de la base de données
    user=DB_USERNAME,  # Nom d'utilisateur de la base de données
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


class BaseModel(Model):
    """
    Classe de base pour tous les modèles.
    Définit la base de données à utiliser pour tous les modèles qui en héritent.
    """
    class Meta:
        database = db  


USER_ROLES = [
    'COMMERCIAL',
    'ADMINISTRATION',
    'SUPPORT'
]

CONTRAT_STATUTS = [
    'EN_COURS',
    'TERMINE'
]


class User(BaseModel):
    """ 
    Modèle représentant un utilisateur.
    """
    username = CharField(unique=True)
    email = CharField(unique=True)
    role = CharField(choices=USER_ROLES)
    password = CharField()
    

class Client(BaseModel):
    """ 
    Modèle représentant un client.
    """

    name = CharField()
    email = CharField(unique=True)
    phone = CharField(null=True)
    company_name = CharField(null=True)
    creation_date = DateTimeField(default=datetime.now)
    last_update_date = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    commercial_contact = ForeignKeyField(User, backref='clients')
    
    def save(self, *args, **kwargs):
        """
        Sauvegarde l'instance du client en base de données.
        Met à jour la date de dernière modification à l'heure actuelle avant de sauvegarder.
        """
        self.last_update_date = datetime.now()
        return super(Client, self).save(*args, **kwargs)

class Contrat(BaseModel):
    """ 
    Modèle représentant un contrat client
    """
    client = ForeignKeyField(Client, backref='contrats')
    status = CharField(choices=CONTRAT_STATUTS, default=CONTRAT_STATUTS[0])
    start_date = DateTimeField()
    end_date = DateTimeField()
    price = IntegerField()
    payment_received = BooleanField(default=False)
    is_signed = BooleanField(default=False)
    contrat_author = ForeignKeyField(User, backref='contrats_author')

class Event(BaseModel):
    """ 
    Modèle représentant un événement lié à un contrat"""
    contrat = ForeignKeyField(Contrat, backref='events')
    support_contact = ForeignKeyField(User, backref='events', null=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    attendees = IntegerField()
    notes = TextField(null=True)


@post_save(sender=Contrat)
def update_contract_status(model_class, instance, created):
    """ 
    Signal déclenché après la sauvegarde d'un contrat.
    Met à jour le statut du contrat à 'TERMINE' si la date de fin est passée et que le paiement a été reçu.
    Ce bloc de code ne sera exécuté que si un nouvel objet Contrat a été créé (et non mis à jour).
    """

    if created:
        end_date = instance.end_date
        today = datetime.now()

        # Ajout de la condition pour vérifier si le paiement a été reçu
        if end_date < today and instance.payment_received == True:
            contrat = instance
            contrat.status = 'TERMINE'
            contrat.save()
