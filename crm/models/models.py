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

# Base model
class BaseModel(Model):
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
    username = CharField(unique=True)
    email = CharField(unique=True)
    role = CharField(choices=USER_ROLES)
    password = CharField()
    

class Client(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    phone = CharField(null=True)
    company_name = CharField(null=True)
    creation_date = DateTimeField(default=datetime.now)
    last_update_date = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    commercial_contact = ForeignKeyField(User, backref='clients')
    
    def save(self, *args, **kwargs):
        self.last_update_date = datetime.now()
        return super(Client, self).save(*args, **kwargs)

class Contrat(BaseModel):
    client = ForeignKeyField(Client, backref='contrats')
    status = CharField(choices=CONTRAT_STATUTS, default=CONTRAT_STATUTS[0])
    start_date = DateTimeField()
    end_date = DateTimeField()
    price = IntegerField()
    payment_received = BooleanField(default=False)
    is_signed = BooleanField(default=False)
    contrat_author = ForeignKeyField(User, backref='contrats_author')

class Event(BaseModel):
    contrat = ForeignKeyField(Contrat, backref='events')
    support_contact = ForeignKeyField(User, backref='events', null=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    attendees = IntegerField()
    notes = TextField(null=True)


@post_save(sender=Contrat)
def update_contract_status(model_class, instance, created):
    # Ce bloc de code ne sera exécuté que si un nouvel objet Contrat a été créé (et non mis à jour).
    if created:
        end_date = instance.end_date
        today = datetime.now()

        # Ajout de la condition pour vérifier si le paiement a été reçu
        if end_date < today and instance.payment_received == True:
            contrat = instance
            contrat.status = 'TERMINE'
            contrat.save()

