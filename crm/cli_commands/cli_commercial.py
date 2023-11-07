from crm.cli_commands.cli_input_validators import get_email, get_phone, is_valid_email, is_valid_phone, get_valid_input, get_event_start, get_event_end, is_valid_id
from crm.cli_commands.cli_permissions import is_commercial, load_user_info
from crm.models.models import Client, Event, Contrat, db
from datetime import datetime
from peewee import DoesNotExist
import peewee 
import typer


app = typer.Typer()

@app.command()
def add_client():
    """
    Ajoute un nouveau client à la base de données.
    Seul un utilisateur avec le rôle de commercial peut ajouter un client.
    """
    user_info = load_user_info()
    commercial_id = user_info.get('user_id', None)
    
    if commercial_id is None:
        typer.echo("Impossible de récupérer l'ID du commercial.")
        return
   
    if not is_commercial():
        typer.echo("Accès refusé. Vous devez être un commercial pour ajouter un client.")
        return

    name = typer.prompt("Nom du client")
    while Client.select().where(Client.name == name).exists():
        typer.echo("Ce nom de client existe déjà. Veuillez en choisir un autre.")
        name = typer.prompt("Nom du client")

    if not name:
        typer.echo("Le nom du client ne peut pas être vide.")
        return

    email = get_email()
    phone = get_phone()

    company_name = typer.prompt("Nom de l'entreprise du client", default=None)

    try:
        client = Client.create(
            name=name, 
            email=email, 
            phone=phone, 
            company_name=company_name, 
            commercial_contact=commercial_id
        )
        typer.echo(f"Client {client.name} ajouté avec succès.")
        
    except Exception as e:
        typer.echo(f"Erreur : {e}")


@app.command()
def update_client():
    """
    Met à jour les informations d'un client existant dans la base de données.
    Seul le commercial qui a créé le client peut mettre à jour ses informations.
    """
    # Vérification de l'authentification et du rôle de l'utilisateur
    if not is_commercial():
        typer.echo("Accès refusé. Vous devez être un commercial pour mettre à jour un client.")
        return

    # Récupération de l'ID du commercial
    user_info = load_user_info()
    commercial_id = user_info.get('user_id', None)
    
    if commercial_id is None:
        typer.echo("Impossible de récupérer l'ID du commercial.")
        return

    # Demande de l'ID du client via un prompt
    client_id_str = typer.prompt("Veuillez entrer l'ID du client à mettre à jour")
    try:
        client_id = int(client_id_str)
        client = Client.get_by_id(client_id)
        
        if client.commercial_contact.id != commercial_id:
            typer.echo("Accès refusé. Vous ne pouvez mettre à jour que les clients que vous avez créés.")
            return
        
    except ValueError:
        typer.echo("L'ID du client doit être un nombre entier.")
        return
    
    except DoesNotExist:
        typer.echo("Client non trouvé.")
        return
    
    except Exception as e:
        typer.echo(f"Erreur lors de la récupération du client : {e}")
        return
    
    # Demande des nouvelles informations du client
    try:
        name = typer.prompt("Nom du client", default=client.name)
        email = get_valid_input("Email du client", is_valid_email, "L'e-mail n'est pas valide.", default=client.email)
        phone = get_valid_input("Numéro de téléphone du client", is_valid_phone, "Le numéro de téléphone doit avoir au moins 10 chiffres.", default=client.phone)
        company_name = typer.prompt("Nom de l'entreprise du client", default=client.company_name)

        with db.atomic():
            client.name = name
            client.email = email
            client.phone = phone
            client.company_name = company_name
            client.save()
            typer.echo(f"Client {client.name} mis à jour avec succès.")
            
    except peewee.IntegrityError as e:
        typer.echo(f"Erreur d'intégrité des données : {e}")
        
    except peewee.PeeweeException as e:
        typer.echo(f"Erreur de base de données : {e}")
        
    except Exception as e:
        typer.echo(f"Erreur inattendue : {e}")
        

@app.command()
def delete_client():
    """
    Supprime un client de la base de données.
    Seul le commercial qui a créé le client peut le supprimer.
    """
    user_info = load_user_info()
    commercial_id = user_info.get('user_id', None)

    if commercial_id is None:
        typer.echo("Impossible de récupérer l'ID du commercial.")
        return

    if not is_commercial():
        typer.echo("Accès refusé. Vous devez être un commercial pour supprimer un client.")
        return

    client_id = get_valid_input(
        "ID du client à supprimer",
        is_valid_id,
        "L'ID du client doit être un nombre entier."
    )

    try:
        client_id = int(client_id)
        client = Client.get_by_id(client_id)
        if client.commercial_contact.id != commercial_id:
            typer.echo("Accès refusé. Vous ne pouvez supprimer que les clients que vous avez créés.")
            return

        client.delete_instance()
        typer.echo(f"Client {client_id} supprimé avec succès.")
        
    except DoesNotExist:
        typer.echo("Client non trouvé.")
        
    except Exception as e:
        typer.echo(f"Erreur lors de la suppression du client : {e}")

def is_valid_attendee_number(input_str):
    return input_str.isdigit() and int(input_str) >= 0
     
@app.command()
def add_event():
    """
    Ajoute un nouvel événement à la base de données.
    Seul un utilisateur avec le rôle de commercial peut ajouter un événement.
    """
    user_info = load_user_info()
    commercial_id = user_info.get('user_id', None)

    if commercial_id is None:
        typer.echo("Impossible de récupérer l'ID du commercial.")
        return

    if not is_commercial():
        typer.echo("Accès refusé. Vous devez être un commercial pour ajouter un événement.")
        return

    contrat_id = typer.prompt("ID du contrat associé à l'événement")
    try:
        contrat = Contrat.get_by_id(int(contrat_id))
        client = Client.get_by_id(contrat.client_id)

        if client.commercial_contact_id != commercial_id:
            typer.echo("Accès refusé. Vous n'avez pas créé ce client.")
            return

        if not (contrat.is_signed and contrat.payment_received):
            typer.echo("Le contrat doit être signé et le paiement reçu pour ajouter un événement.")
            return

        # Demande des dates de l'événement en s'assurant qu'elles sont dans la période du contrat
        start_date_event = get_event_start(contrat.start_date.strftime("%Y-%m-%d"), contrat.end_date.strftime("%Y-%m-%d"))
        end_date_event = get_event_end(start_date_event, contrat.end_date.strftime("%Y-%m-%d"))

        attendees = get_valid_input(
            "Nombre de participants",
            is_valid_attendee_number,
            "Le nombre de participants doit être un nombre entier positif."
        )

        notes = typer.prompt("Notes pour l'événement", default="", show_default=False)

        # Création de l'événement dans la base de données
        event = Event.create(
            contrat=contrat,
            start_date=datetime.strptime(start_date_event, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date_event, "%Y-%m-%d"),
            attendees=int(attendees),
            notes=notes
        )
        typer.echo(f"Événement pour le contrat {contrat_id} ajouté avec succès. ID de l'événement: {event.id}")
        
    except ValueError:
        typer.echo("L'ID du contrat doit être un nombre entier.")
        
    except DoesNotExist:
        typer.echo("Contrat ou client non trouvé.")
        
    except Exception as e:
        typer.echo(f"Erreur lors de l'ajout de l'événement : {e}")