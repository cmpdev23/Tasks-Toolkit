import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()
# Charger les variables d'environnement pour l'API de Pipedrive
API_KEY = os.getenv('PIPEDRIVE_API_KEY') 
BASE_URL = 'https://api.pipedrive.com/api/v2/persons/'

def get_person_name(person_id: int) -> str:
    """
    Récupère le nom d'une personne à partir de son ID dans Pipedrive.
    """
    url = f"{BASE_URL}{person_id}?api_token={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        
        person_data = response.json()
        if person_data['success']:
            person_name = person_data['data']['name']
            logging.info(f"Nom de la personne récupéré : {person_name}")
            return person_name
        else:
            logging.error(f"Erreur lors de la récupération du nom de la personne : {person_data['error']}")
            return "Nom non disponible"
    except requests.RequestException as e:
        logging.error(f"Une erreur s'est produite lors de la récupération du nom de la personne : {e}")
        return "Erreur de récupération du nom"

