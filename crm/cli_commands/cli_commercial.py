from crm.cli_commands.cli_input_validators import is_valid_email, is_valid_phone
import typer
from crm.models.models import Client, Event, Contrat
from crm.cli_commands.cli_permissions import is_commercial, load_user_info
from peewee import DoesNotExist

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

    while True:
        name = typer.prompt("Nom du client")
        if name:
            break
        else:
            typer.echo("Le nom du client ne peut pas être vide.")

    while True:
        email = typer.prompt("Email du client")
        if is_valid_email(email):
            break
        else:
            typer.echo("L'e-mail n'est pas valide.")

    while True:
        phone = typer.prompt("Numéro de téléphone du client")
        if is_valid_phone(phone):
            break
        else:
            typer.echo("Le numéro de téléphone doit avoir au moins 10 chiffres.")

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
def update_client(client_id: int):
    """
    Met à jour les informations d'un client existant dans la base de données.
    Seul le commercial qui a créé le client peut mettre à jour ses informations.
    """
    user_info = load_user_info()
    commercial_id = user_info.get('user_id', None)

    if commercial_id is None:
        typer.echo("Impossible de récupérer l'ID du commercial.")
        return

    if not is_commercial():
        typer.echo("Accès refusé. Vous devez être un commercial pour mettre à jour un client.")
        return

    try:
        client = Client.get_by_id(client_id)
        
        if client.commercial_contact.id != commercial_id:
            typer.echo("Accès refusé. Vous ne pouvez mettre à jour que les clients que vous avez créés.")
            return

        name = typer.prompt("Nom du client", default=client.name)
        email = typer.prompt("Email du client", default=client.email)
        phone = typer.prompt("Numéro de téléphone du client", default=client.phone)
        company_name = typer.prompt("Nom de l'entreprise du client", default=client.company_name)

        if name:
            client.name = name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if company_name:
            client.company_name = company_name

        client.commercial_contact = commercial_id  
        client.save()
        typer.echo(f"Client {client.name} mis à jour avec succès.")
        
    except DoesNotExist:
        typer.echo("Client non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")


@app.command()
def delete_client(client_id: int):
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

    try:
        client = Client.get_by_id(client_id)
        if client.commercial_contact.id != commercial_id:
            typer.echo("Accès refusé. Vous ne pouvez supprimer que les clients que vous avez créés.")
            return

        client.delete_instance()
        typer.echo(f"Client {client.name} supprimé avec succès.")
    except DoesNotExist:
        typer.echo("Client non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")



@app.command()
def add_event_commercial(contrat_id: int, start_date: str, end_date: str, price: int, notes: str = None):
    if not is_commercial():
        typer.echo("Accès refusé. Vous devez être un commercial pour créer un événement.")
        return
    try:
        contrat = Contrat.get_by_id(contrat_id)
        # vérifier si le contrat est signé et si le paiement a été reçu
        event = Event.create(contrat=contrat, start_date=start_date, end_date=end_date, price=price, notes=notes)
        typer.echo(f"Événement pour le contrat {contrat_id} ajouté avec succès.")
    except DoesNotExist:
        typer.echo("Contrat non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
