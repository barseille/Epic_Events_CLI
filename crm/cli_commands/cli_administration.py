import typer
from crm.models.models import Contrat, Client
from crm.cli_commands.cli_permissions import is_administration, load_user_info
from peewee import DoesNotExist
from crm.models.models import CONTRAT_STATUTS
from crm.cli_commands.cli_input_validators import get_start_date, get_end_date, get_price, get_boolean_input, get_valid_id



app = typer.Typer()


def is_client_not_under_contract(client: Client) -> bool:
    existing_contract = Contrat.select().where(Contrat.client == client).exists()
    if existing_contract:
        typer.echo("Ce client est déjà sous contrat. Veuillez choisir un autre client.")
        return False
    return True

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
    
    client_id = get_valid_id(Client, "ID du client", is_client_not_under_contract)
    client = Client.get_by_id(client_id)

    is_signed = get_boolean_input("Le contrat est-il signé ? (Oui/Non)")
    payment_received = get_boolean_input("Paiement reçu ? (Oui/Non)")


    try:
        start_date = get_start_date()
        end_date = get_end_date(start_date)
        price = get_price()
        
        Contrat.create(
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
def update_contrat():
    """
    Met à jour un contrat existant dans la base de données.
    Seul un utilisateur avec le rôle d'administration peut mettre à jour un contrat.
    """
    user_info = load_user_info()
    admin_id = user_info.get('user_id', None)

    if admin_id is None:
        typer.echo("Impossible de récupérer l'ID de l'administrateur.")
        return

    if not is_administration():
        typer.echo("Accès refusé. Vous devez être dans l'équipe d'administration pour mettre à jour un contrat.")
        return

    while True:
        contrat_id_str = typer.prompt("ID du contrat à mettre à jour")
        try:
            contrat_id = int(contrat_id_str)
            contrat = Contrat.get_by_id(contrat_id)
            break
        except ValueError:
            typer.echo("L'ID du contrat doit être un nombre entier.")
        except DoesNotExist:
            typer.echo("Contrat non trouvé.")
        except Exception as e:
            typer.echo(f"Erreur : {e}")
            

    start_date = get_start_date(str(contrat.start_date))
    end_date = get_end_date(start_date, str(contrat.end_date))
    price = get_price()

    is_signed = get_boolean_input("Le contrat est-il signé ? (Oui/Non)", default="Oui" if contrat.is_signed else "Non")
    payment_received = get_boolean_input("Paiement reçu ? (Oui/Non)", default="Oui" if contrat.payment_received else "Non")

    try:
        contrat.start_date = start_date
        contrat.end_date = end_date
        contrat.price = price
        contrat.is_signed = is_signed
        contrat.payment_received = payment_received
        contrat.contrat_author = admin_id
        contrat.save()
        
        typer.echo(f"Contrat {contrat_id} mis à jour avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")


@app.command()
def delete_contrat():
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

    while True:
        contrat_id_str = typer.prompt("ID du contrat à supprimer")
        try:
            contrat_id = int(contrat_id_str)
            contrat = Contrat.get_by_id(contrat_id)
            break
        except ValueError:
            typer.echo("L'ID du contrat doit être un nombre entier.")
        except DoesNotExist:
            typer.echo("Contrat non trouvé.")
        except Exception as e:
            typer.echo(f"Erreur : {e}")

    try:
        contrat.delete_instance()
        typer.echo(f"Contrat {contrat_id} supprimé avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")

