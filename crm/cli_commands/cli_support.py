from crm.cli_commands.cli_permissions import load_user_info
from crm.cli_commands.cli_input_validators import get_event_start, get_event_end
from peewee import DoesNotExist
import typer
from datetime import datetime
from crm.models.models import db, Event


app = typer.Typer()


@app.command()
def assign_support_to_event():
    """
    Assigner un membre du support à un événement.
    Seuls les membres du support peuvent exécuter cette commande.
    """
    user_info = load_user_info()
    support_id = user_info.get('user_id', None)

    if support_id is None:
        typer.echo("Impossible de récupérer l'ID du membre du support.")
        return

    if user_info.get('role').upper() != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent assigner du support aux événements.")
        return

    event_id = typer.prompt("ID de l'événement à assigner au support")

    try:
        event = Event.get_by_id(int(event_id))

        # Vérifie si l'événement est déjà assigné à un membre du support
        if event.support_contact:
            if event.support_contact.id == support_id:
                typer.echo(f"Cet événement est déjà assigné à vous-même.")
            else:
                typer.echo("Cet événement est déjà assigné à un autre membre du support.")
        else:
            event.support_contact = support_id
            event.save()
            typer.echo(f"Membre du support avec l'id{support_id} assigné à l'événement id{event_id} avec succès.")

    except ValueError:
        typer.echo("L'ID de l'événement doit être un nombre entier.")
        
    except DoesNotExist:
        typer.echo("Événement non trouvé.")
        
    except Exception as e:
        typer.echo(f"Erreur lors de l'assignation du support à l'événement : {e}")



@app.command()
def update_event():
    """
    Met à jour un événement existant dans la base de données.
    Seuls les membres de l'équipe de support peuvent exécuter cette commande.
    """
    user_info = load_user_info()
    support_id = user_info.get('user_id', None)

    if support_id is None:
        typer.echo("Impossible de récupérer l'ID du membre du support.")
        return

    if user_info.get('role').upper() != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent mettre à jour des événements.")
        return

    event_id_str = typer.prompt("ID de l'événement")
    try:
        event_id = int(event_id_str)
        event = Event.get_by_id(event_id)
        
        # Récupération du contrat associé à l'événement
        contrat = event.contrat  

        if event.support_contact_id != support_id:
            typer.echo("Accès refusé. Vous ne pouvez mettre à jour que les événements que vous avez assignés.")
            return
        
    except ValueError:
        typer.echo("L'ID de l'événement doit être un nombre entier.")
        return
    
    except DoesNotExist:
        typer.echo("Événement non trouvé.")
        return
    
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        return

    # Utilisation des fonctions de validation pour les dates
    start_date_str = get_event_start(contrat.start_date.strftime("%Y-%m-%d"), contrat.end_date.strftime("%Y-%m-%d"))
    end_date_str = get_event_end(start_date_str, contrat.end_date.strftime("%Y-%m-%d"))

    # Demande de mise à jour pour le nombre de participants et les notes
    attendees_str = typer.prompt("Nombre de participants", default=str(event.attendees))
    notes_str = typer.prompt("Notes pour l'événement", default=event.notes)

    # Validation du nombre de participants
    if not attendees_str.isdigit() or int(attendees_str) < 0:
        typer.echo("Le nombre de participants doit être un nombre entier positif.")
        return

    # Mise à jour de l'événement dans la base de données
    try:
        with db.atomic():
            event.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            event.end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            event.attendees = int(attendees_str)
            event.notes = notes_str
            event.save()
            typer.echo(f"Événement ID {event_id} mis à jour avec succès.")
            
    except Exception as e:
        typer.echo(f"Erreur lors de la mise à jour de l'événement : {e}")



@app.command()
def delete_event():
    """
    Supprime un événement de la base de données.
    Seuls les membres de l'équipe de support peuvent exécuter cette commande.
    """
    user_info = load_user_info()
    support_id = user_info.get('user_id', None)

    if support_id is None:
        typer.echo("Impossible de récupérer l'ID du membre du support.")
        return

    if user_info.get('role').upper() != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent supprimer des événements.")
        return

    event_id_str = typer.prompt("ID de l'événement à supprimer")
    
    try:
        event_id = int(event_id_str)
        event = Event.get_by_id(event_id)
        if event.support_contact_id != support_id:
            typer.echo("Accès refusé. Vous ne pouvez supprimer que les événements que vous avez assignés.")
            return
        
        # Suppression de l'événement
        event.delete_instance()  
        typer.echo(f"Événement {event_id} supprimé avec succès.")
        
    except ValueError:
        typer.echo("L'ID de l'événement doit être un nombre entier.")
        
    except DoesNotExist:
        typer.echo("Événement non trouvé.")
        
    except Exception as e:
        typer.echo(f"Erreur lors de la suppression de l'événement : {e}")