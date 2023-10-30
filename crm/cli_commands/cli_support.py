from crm.cli_commands.cli_permissions import load_user_info
from crm.models.models import Event
from peewee import DoesNotExist
import typer


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

    if user_info.get('role') != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent assigner du support aux événements.")
        return

    while True:
        event_id = typer.prompt("ID de l'événement")
        
        try:
            event = Event.get_by_id(int(event_id))
            
            if event.support_contact is None:
                event.support_contact = support_id
                event.save()
                typer.echo(f"Membre du support {support_id} assigné à l'événement {event_id} avec succès.")
                break
            
            elif event.support_contact.id == support_id:
                typer.echo(f"Cet événement est déjà assigné à vous même.")
                break
            
            else:
                typer.echo("Cet événement est déjà assigné à un autre membre du support.")
                
        except ValueError:
            typer.echo("Veuillez entrer un ID d'événement valide (un nombre entier).")
            
        except DoesNotExist:
            typer.echo("Événement non trouvé.")
            
        except Exception as e:
            typer.echo(f"Erreur : {e}")
            


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

    if user_info.get('role') != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent mettre à jour des événements.")
        return

    while True:
        event_id_str = typer.prompt("ID de l'événement")
        try:
            event_id = int(event_id_str)
            event = Event.get_by_id(event_id)
            if event.support_contact_id != support_id:
                typer.echo("Accès refusé. Vous ne pouvez mettre à jour que les événements que vous avez assignés.")
                return
            break
        except ValueError:
            typer.echo("L'ID de l'événement doit être un nombre entier.")
        except DoesNotExist:
            typer.echo("Événement non trouvé.")
        except Exception as e:
            typer.echo(f"Erreur : {e}")


    start_date = typer.prompt("Date de début de l'événement", default=str(event.start_date))
    end_date = typer.prompt("Date de fin de l'événement", default=str(event.end_date))


    while True:
        try:
            attendees_str = typer.prompt("Nombre de participants", default=str(event.attendees))
            attendees = int(attendees_str)
            if attendees >= 0:
                break
            else:
                typer.echo("Le nombre de participants doit être un nombre entier positif.")
        except ValueError:
            typer.echo("Le nombre de participants doit être un nombre entier.")

    notes = typer.prompt("Notes pour l'événement", default=event.notes, show_default=True)

    try:
        event.start_date = start_date
        event.end_date = end_date
        event.attendees = attendees
        event.notes = notes
        event.save()
        typer.echo(f"Événement {event_id} mis à jour avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
 
        
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

    if user_info.get('role') != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent supprimer des événements.")
        return

    while True:
        event_id_str = typer.prompt("ID de l'événement à supprimer")
        try:
            event_id = int(event_id_str)
            event = Event.get_by_id(event_id)
            if event.support_contact_id != support_id:
                typer.echo("Accès refusé. Vous ne pouvez supprimer que les événements que vous avez assignés.")
                return
            break
        
        except ValueError:
            typer.echo("L'ID de l'événement doit être un nombre entier.")
            
        except DoesNotExist:
            typer.echo("Événement non trouvé.")
            
        except Exception as e:
            typer.echo(f"Erreur : {e}")

    try:
        event.delete_instance()
        typer.echo(f"Événement {event_id} supprimé avec succès.")
        
    except Exception as e:
        typer.echo(f"Erreur : {e}")





