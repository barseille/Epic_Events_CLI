import typer
from crm.models.models import Client, Contrat, CONTRAT_STATUTS, db
from crm.cli_commands.cli_permissions import is_administration, load_user_info
from peewee import DoesNotExist
import peewee 
from crm.cli_commands.cli_input_validators import (
    get_valid_id,
    get_boolean_input,
    get_start_date,
    get_end_date,
    get_price,
    get_valid_input,
    is_valid_id
)

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

    
    client_id = get_valid_id(Client, "ID du client", is_client_not_under_contrat)
    client = Client.get_by_id(client_id)

    is_signed = get_boolean_input("Le contrat est-il signé ? (Oui/Non)")
    payment_received = get_boolean_input("Paiement reçu ? (Oui/Non)")

    try:
        start_date = get_start_date()
        end_date = get_end_date(start_date)
        price = get_price()
        
        new_contrat = Contrat.create(
            client=client,
            status=CONTRAT_STATUTS[0],
            start_date=start_date,
            end_date=end_date,
            price=price,
            payment_received=payment_received,
            is_signed=is_signed,
            contrat_author=admin_id
        )
        typer.echo(f"Contrat pour le client {client.name} ajouté avec succès. ID du contrat: {new_contrat.id}")
    except Exception as e:
        typer.echo(f"Erreur lors de l'ajout du contrat : {e}")

def is_client_not_under_contrat(client_id: int) -> bool:
    """
    Vérifie si le client n'est pas déjà sous contrat.
    """
    try:
        Contrat.get(Contrat.client == client_id, Contrat.status == "EN_COURS")
        return False
    except Contrat.DoesNotExist:
        return True


@app.command()
def update_contrat():
    """
    Met à jour les informations d'un contrat existant dans la base de données.
    Seul l'administrateur qui a créé le contrat peut mettre à jour le contrat.
    """
    if not is_administration():
        typer.echo("Accès refusé. Vous devez être dans l'équipe d'administration pour mettre à jour un contrat.")
        return

    user_info = load_user_info()
    admin_id = user_info.get('user_id', None)
    if admin_id is None:
        typer.echo("Impossible de récupérer l'ID de l'administrateur.")
        return

    contrat_id_str = typer.prompt("Veuillez entrer l'ID du contrat à mettre à jour")
    
    try:
        contrat_id = int(contrat_id_str)
        contrat = Contrat.get_by_id(contrat_id)
        
    except ValueError:
        typer.echo("L'ID du contrat doit être un nombre entier.")
        return
    
    except DoesNotExist:
        typer.echo("Contrat non trouvé.")
        return
    
    except Exception as e:
        typer.echo(f"Erreur lors de la récupération du contrat : {e}")
        return

    # Vérifiez si l'utilisateur actuel est l'auteur du contrat
    if contrat.contrat_author.id != admin_id:
        typer.echo("Accès refusé. Vous ne pouvez mettre à jour que les contrats que vous avez créés.")
        return

    # Demande des nouvelles informations du contrat
    try:
        # Mise à jour du statut du contrat
        status_input = typer.prompt("Statut du contrat", default=contrat.status)
        
        # Convertit l'entrée en majuscules
        status = status_input.upper()  

        # Compare les valeurs en majuscules
        if status not in [s.upper() for s in CONTRAT_STATUTS]:  
            typer.echo("Statut non valide.")
            return
  
        # Mise à jour de la date de début
        start_date = get_start_date()

        # Mise à jour de la date de fin
        end_date = get_end_date(start_date)

        # Mise à jour du prix
        price = get_price()

        # Mise à jour de l'indicateur de paiement reçu
        payment_received = get_boolean_input("Paiement reçu ? (Oui/Non)")

        # Mise à jour de l'indicateur de contrat signé
        is_signed = get_boolean_input("Le contrat est-il signé ? (Oui/Non)")

        with db.atomic():
            contrat.status = status
            contrat.start_date = start_date
            contrat.end_date = end_date
            contrat.price = price
            contrat.payment_received = payment_received
            contrat.is_signed = is_signed
            contrat.save()
            typer.echo(f"Contrat {contrat.id} mis à jour avec succès.")
            
    except peewee.IntegrityError as e:
        typer.echo(f"Erreur d'intégrité des données : {e}")
        
    except peewee.PeeweeException as e:
        typer.echo(f"Erreur de base de données : {e}")
        
    except Exception as e:
        typer.echo(f"Erreur inattendue : {e}")


@app.command()
def delete_contrat():
    """
    Supprime un contrat de la base de données.
    Seul l'administrateur qui a créé le contrat peut le supprimer.
    """
    user_info = load_user_info()
    admin_id = user_info.get('user_id', None)

    if admin_id is None:
        typer.echo("Impossible de récupérer l'ID de l'administrateur.")
        return

    if not is_administration():
        typer.echo("Accès refusé. Vous devez être dans l'équipe d'administration pour supprimer un contrat.")
        return

    contrat_id = get_valid_input(
        "ID du contrat à supprimer",
        is_valid_id,
        "L'ID du contrat doit être un nombre entier."
    )

    try:
        contrat_id = int(contrat_id)
        contrat = Contrat.get_by_id(contrat_id)
        if contrat.contrat_author.id != admin_id:
            typer.echo("Accès refusé. Vous ne pouvez supprimer que les contrats que vous avez créés.")
            return

        contrat.delete_instance()
        typer.echo(f"Contrat {contrat_id} supprimé avec succès.")
        
    except DoesNotExist:
        typer.echo("Contrat non trouvé.")
        
    except Exception as e:
        typer.echo(f"Erreur lors de la suppression du contrat : {e}")
