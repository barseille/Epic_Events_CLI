import logging
from crm.models.models import db, User, Client, Contrat, Event

# Configurer le logging
logging.basicConfig(level=logging.INFO)

def create_db():
    try:
        """
        Crée et initialise la base de données.

        Cette fonction connecte à la base de données, supprime les tables existantes si elles existent,
        et crée de nouvelles tables pour les utilisateurs, les clients, les contrats et les événements.
        Elle gère les exceptions en cas d'erreurs de connexion ou d'opérations avec la base de données
        et assure la fermeture de la connexion à la fin de l'opération.
        """
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
