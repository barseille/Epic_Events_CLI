import logging
from crm.models.models import db, User, Client, Contrat, Event

# Configurer le logging
logging.basicConfig(level=logging.INFO)

def create_db():
    try:
        logging.info("Tentative de connexion à la base de données...")
        db.connect()
        logging.info("Connecté à la base de données.")

        logging.info("Suppression des tables existantes...")
        db.drop_tables([User, Client, Contrat, Event])
        logging.info("Tables supprimées.")

        logging.info("Création de nouvelles tables...")
        db.create_tables([User, Client, Contrat, Event])
        logging.info("Tables créées avec succès.")

    except Exception as e:
        logging.error(f"Une erreur s'est produite : {e}")
    finally:
        logging.info("Fermeture de la base de données.")
        db.close()

if __name__ == "__main__":
    create_db()
