from flask import Flask, request, jsonify
import logging
import json
from datetime import datetime
from pipedrive_operations.update_pipedrive_activity import update_pipedrive_activity
from utils.create_pipedrive_deal_link import create_pipedrive_link
from pipedrive_operations.get_person_name import get_person_name


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/', methods=['POST'])
def rdvsyncer():
    data = request.json

    meta = data.get("meta", {})
    activity_data = data.get("data", {})

    # Extraction des données requises
    activity_id = activity_data.get('id')
    deal_id = activity_data.get('deal_id')
    subject = activity_data.get('subject')
    person_id = activity_data.get('person_id')
    activity_type = activity_data.get('type')
    action = meta.get('action')

    # ⚠️ Conditions de traitement
    if action != "create":
        logger.info(f"Ignoré : action non prise en charge ({action}) pour activity_id={activity_id}")
        return jsonify({"message": f"Action '{action}' ignorée"}), 200

    if activity_type != "meeting":
        logger.info(f"Ignoré : type d'activité non pris en charge ({activity_type}) pour activity_id={activity_id}")
        return jsonify({"message": f"Type d'activité '{activity_type}' ignoré"}), 200

    if not (deal_id or person_id):
        logger.warning(f"Aucune entité liée (ni deal ni personne) pour activity_id={activity_id}")
        return jsonify({"message": "Aucune entité liée"}), 200

    # 🚫 Vérification des invités
    attendees = activity_data.get('attendees')
    if attendees is not None and len(attendees) > 0:
        logger.info(f"Ignoré : présence d'invités dans l'activité (activity_id={activity_id})")
        return jsonify({"message": "Activité avec invités ignorée"}), 200

    note = create_pipedrive_link(activity_data)

    if not note:
        logger.warning(f"Aucun lien créé pour l'activité (activity_id={activity_id})")
        return jsonify({"message": "Aucun lien créé"}), 200

    person_name = get_person_name(person_id)

    if not person_name:
        person_name = "Rendez-vous"

    # Mise à jour de l'activité dans Pipedrive 
    update_pipedrive_activity(activity_id, note, person_name, subject)


    return jsonify({"message": "Success"}), 200


if __name__ == '__main__':
    app.run(debug=True)
