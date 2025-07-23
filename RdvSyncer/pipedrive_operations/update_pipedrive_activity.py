import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Charger les variables d'environnement pour l'API de Pipedrive
API_KEY = os.getenv('PIPEDRIVE_API_KEY')
BASE_URL = 'https://api.pipedrive.com/v1/activities'

# Configurer le logger
logger = logging.getLogger(__name__)


def update_pipedrive_activity(activity_id, note, person_name, subject):
    # Construire l'URL de l'API
    url = f"{BASE_URL}/{activity_id}?api_token={API_KEY}"

    # Journaliser l'URL de la requête
    logger.info(f"Updating Pipedrive activity. URL: {url}")

    # Préparer les données pour la mise à jour
    data = {'public_description': note}

    # Si l'objet est un 'Rendez-vous', modifier également le sujet (deal_title)
    if subject == "Rendez-vous":
        data['subject'] = person_name

    # Journaliser les données envoyées à l'API
    logger.info(f"Data being sent to Pipedrive: {person_name}")

    try:
        # Envoyer la requête PUT pour mettre à jour l'activité
        response = requests.put(url, data=data)

        # Vérifier le statut de la réponse
        if response.status_code == 200:
            updated_activity = response.json()
            logger.info(f"Activity {activity_id} updated successfully:")
            return updated_activity
        else:
            logger.error(f"Failed to update activity {activity_id}. Status code: {response.status_code}, Response: {response.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"An error occurred while updating the activity: {e}")
        return None
