from crm.models.models import db, User, Client, Contrat, Event


def create_db():
    db.connect()
    db.drop_tables([User, Client, Contrat, Event])
    db.create_tables([User, Client, Contrat, Event])
    db.close()


if __name__ == "__main__":
    create_db()