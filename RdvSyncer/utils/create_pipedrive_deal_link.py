import logging
logger = logging.getLogger(__name__)


def create_pipedrive_link(activity_data: dict) -> str:
    deal_id = activity_data.get("deal_id")
    person_id = activity_data.get("person_id")
    base_url = "https://comparermaprime.pipedrive.com"

    if deal_id:
        pipedrive_url = f"{base_url}/deal/{deal_id}"
        logger.info(f"Création du lien vers le deal : {pipedrive_url}")
    elif person_id:
        pipedrive_url = f"{base_url}/person/{person_id}"
        logger.info(f"Création du lien vers la personne : {pipedrive_url}")
    else:
        logger.warning("Ni deal_id ni person_id fourni. Aucun lien généré.")
        return "Aucun lien disponible."

    note = f'<a href="{pipedrive_url}" target="_blank" rel="noopener noreferrer">Lien vers la fiche</a>'
    return note

