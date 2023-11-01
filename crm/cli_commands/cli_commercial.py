from crm.cli_commands.cli_input_validators import is_valid_email, is_valid_phone,get_start_date, get_end_date
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
        existing_client_with_name = Client.select().where(Client.name == name).first()
        if existing_client_with_name:
            typer.echo("Ce nom de client existe déjà. Veuillez en choisir un autre.")
            continue
        if name:
            break
        else:
            typer.echo("Le nom du client ne peut pas être vide.")

    while True:
        email = typer.prompt("Email du client")
        existing_client_with_email = Client.select().where(Client.email == email).first()
        if existing_client_with_email:
            typer.echo("Cet email est déjà utilisé par un autre client. Veuillez en utiliser un différent.")
            continue
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
def update_client():
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

    while True:
        client_id_str = typer.prompt("ID du client à mettre à jour")
        try:
            client_id = int(client_id_str)
            client = Client.get_by_id(client_id)
            if client.commercial_contact.id != commercial_id:
                typer.echo("Accès refusé. Vous ne pouvez mettre à jour que les clients que vous avez créés.")
                return
            break
        except ValueError:
            typer.echo("L'ID du client doit être un nombre entier.")
        except DoesNotExist:
            typer.echo("Client non trouvé.")
        except Exception as e:
            typer.echo(f"Erreur : {e}")

    name = typer.prompt("Nom du client", default=client.name)
    email = typer.prompt("Email du client", default=client.email)
    phone = typer.prompt("Numéro de téléphone du client", default=client.phone)
    company_name = typer.prompt("Nom de l'entreprise du client", default=client.company_name)

    try:
        client.name = name
        client.email = email
        client.phone = phone
        client.company_name = company_name
        client.commercial_contact = commercial_id
        client.save()
        typer.echo(f"Client {client.name} mis à jour avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")



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

    while True:
        client_id_str = typer.prompt("ID du client à supprimer")
        try:
            client_id = int(client_id_str)
            client = Client.get_by_id(client_id)
            if client.commercial_contact.id != commercial_id:
                typer.echo("Accès refusé. Vous ne pouvez supprimer que les clients que vous avez créés.")
                return
            break
        except ValueError:
            typer.echo("L'ID du client doit être un nombre entier.")
        except DoesNotExist:
            typer.echo("Client non trouvé.")
        except Exception as e:
            typer.echo(f"Erreur : {e}")

    try:
        client.delete_instance()
        typer.echo(f"Client {client_id} supprimé avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")


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

    while True:
        contrat_id = typer.prompt("ID du contrat")
        try:
            contrat = Contrat.get_by_id(int(contrat_id))
            client = Client.get_by_id(contrat.client_id)

            if client.commercial_contact_id != commercial_id:
                typer.echo("Accès refusé. Vous n'avez pas créé ce client.")
                return

            if contrat.is_signed and contrat.payment_received:
                break
            else:
                typer.echo("Le contrat doit être signé et le paiement doit être reçu pour ajouter un événement.")
        except DoesNotExist:
            typer.echo("Contrat ou client non trouvé.")
        except Exception as e:
            typer.echo(f"Erreur : {e}")

    start_date = get_start_date() 
    end_date = get_end_date()

    while True:
        try:
            attendees_str = typer.prompt("Nombre de participants")
            attendees = int(attendees_str)
            if attendees >= 0:
                break
            else:
                typer.echo("Le nombre de participants doit être un nombre entier positif.")
        except ValueError:
            typer.echo("Le nombre de participants doit être un nombre entier.")

    notes = typer.prompt("Notes pour l'événement", default=None, show_default=False)

    try:
        event = Event.create(
            contrat=contrat,
            start_date=start_date,
            end_date=end_date,
            attendees=attendees,
            notes=notes
        )
        typer.echo(f"Événement pour le contrat {contrat_id} ajouté avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
