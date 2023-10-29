import typer
from crm.models.models import Contrat, Client
from crm.cli_commands.cli_permissions import is_administration, load_user_info
from peewee import DoesNotExist
from crm.models.models import CONTRAT_STATUTS
from crm.cli_commands.cli_input_validators import is_valid_date
from datetime import datetime


app = typer.Typer()

@app.command()
def add_contrat():
    """
    Ajoute un nouveau contrat à la base de données.
    Seul un utilisateur avec le rôle d'administration peut ajouter un contrat.
    """
    user_info = load_user_info()
    admin_id = user_info.get('user_id', None)

    if admin_id is None:
        typer.echo("Impossible de récupérer l'ID de l'administrateur.")
        return

    if not is_administration():
        typer.echo("Accès refusé. Vous devez être dans l'équipe d'administration pour ajouter un contrat.")
        return

    while True:
        client_id = typer.prompt("ID du client")
        try:
            client = Client.get_by_id(int(client_id))
            
            # Vérifier si le client est déjà sous contrat
            existing_contract = Contrat.select().where(Contrat.client == client).exists()
            
            if existing_contract:
                typer.echo("Ce client est déjà sous contrat. Veuillez choisir un autre client.")
            else:
                break
        except ValueError:
            typer.echo("Veuillez entrer un ID de client valide (nombre entier).")    
                
        except DoesNotExist:
            typer.echo("Client non trouvé. Essayez encore.")
            
    while True:
        is_signed = typer.prompt("Le contrat est-il signé ? (Oui/Non)")
        if is_signed.lower() == "oui":
            is_signed = True
            break
        elif is_signed.lower() == "non":
            is_signed = False
            break
        else:
            typer.echo("Réponse invalide. Répondez par 'Oui' ou 'Non'.")

    while True:
        start_date = typer.prompt("Date de début du contrat (YYYY-MM-DD)")
        today = datetime.now().strftime('%Y-%m-%d')
        if is_valid_date(start_date) and start_date >= today:
            break
        else:
            typer.echo("La date de début doit être au format YYYY-MM-DD et ne peut pas être antérieure à aujourd'hui.")

    while True:
        end_date = typer.prompt("Date de fin du contrat (YYYY-MM-DD)")
        today = datetime.now().strftime('%Y-%m-%d')
        if is_valid_date(end_date) and end_date >= today:
            break
        else:
            typer.echo("La date de fin doit être au format YYYY-MM-DD et ne peut pas être antérieure à aujourd'hui.")
            
    while True:
        try:
            price = typer.prompt("Prix", type=int)
            if price >= 0:
                break
            else:
                typer.echo("Le prix doit être un nombre entier positif.")
        except ValueError:
            typer.echo("Le prix doit être un nombre entier.")


    while True:
        payment_received = typer.prompt("Paiement reçu ? (Oui/Non)")
        if payment_received.lower() == "oui":
            payment_received = True
            break
        elif payment_received.lower() == "non":
            payment_received = False
            break
        else:
            typer.echo("Réponse invalide. Répondez par 'Oui' ou 'Non'.")

    try:
        contrat = Contrat.create(
            client=client,
            status=CONTRAT_STATUTS[0], # "EN_COURS" par défault
            start_date=start_date,
            end_date=end_date,
            price=price,
            payment_received=payment_received,
            is_signed=is_signed,
            contrat_author=admin_id
        )
        typer.echo(f"Contrat pour le client {client.name} ajouté avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")

     
@app.command()
def update_contrat(contrat_id: int):
    user_info = load_user_info()
    admin_id = user_info.get('user_id', None)

    if admin_id is None:
        typer.echo("Impossible de récupérer l'ID de l'administrateur.")
        return

    if not is_administration():
        typer.echo("Accès refusé. Vous devez être dans l'équipe d'administration pour mettre à jour un contrat.")
        return

    try:
        contrat = Contrat.get_by_id(contrat_id)
        
        if contrat.is_signed:
            default_is_signed = "Oui"
        else:
            default_is_signed = "Non"


        while True:
            is_signed = typer.prompt("Le contrat est-il signé ? (Oui/Non)", default=default_is_signed)
            if is_signed.lower() == "oui":
                contrat.is_signed = True
                break
            elif is_signed.lower() == "non":
                contrat.is_signed = False
                break
            else:
                typer.echo("Réponse invalide. Répondez par 'Oui' ou 'Non'.")

        start_date = typer.prompt("Date de début du contrat", default=str(contrat.start_date))
        end_date = typer.prompt("Date de fin du contrat", default=str(contrat.end_date))
        price = typer.prompt("Prix du contrat", default=str(contrat.price))

        
        if contrat.payment_received:
            default_payment_received = "Oui"
        else:
            default_payment_received = "Non"
        
        while True:
            payment_received = typer.prompt("Paiement reçu ? (Oui/Non)", default=default_payment_received)
            if payment_received.lower() == "oui":
                contrat.payment_received = True
                break
            elif payment_received.lower() == "non":
                contrat.payment_received = False
                break
            else:
                typer.echo("Réponse invalide. Répondez par 'Oui' ou 'Non'.")

        if start_date:
            contrat.start_date = start_date
        if end_date:
            contrat.end_date = end_date
        if price:
            contrat.price = int(price)

        contrat.contrat_author = admin_id
        contrat.save()
        typer.echo(f"Contrat {contrat_id} mis à jour avec succès.")
        
    except DoesNotExist:
        typer.echo("Contrat non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        
@app.command()
def delete_contrat(contrat_id: int):
    """
    Supprime un contrat de la base de données.
    Seul un utilisateur avec le rôle d'administration peut supprimer un contrat.
    """
    user_info = load_user_info()
    admin_id = user_info.get('user_id', None)

    if admin_id is None:
        typer.echo("Impossible de récupérer l'ID de l'administrateur.")
        return

    if not is_administration():
        typer.echo("Accès refusé. Vous devez être dans l'équipe d'administration pour supprimer un contrat.")
        return

    try:
        contrat = Contrat.get_by_id(contrat_id)
        if contrat.contrat_author.id != admin_id:
            typer.echo("Accès refusé. Vous ne pouvez supprimer que les contrats que vous avez créés.")
            return

        contrat.delete_instance()
        typer.echo(f"Contrat {contrat_id} supprimé avec succès.")
    except DoesNotExist:
        typer.echo("Contrat non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
