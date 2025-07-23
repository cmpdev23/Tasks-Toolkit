def filter_activity(data):
    # Condition 1 : Vérifier si l'objet est une "activity"
    if data.get('meta', {}).get('object') != 'activity':
        return False

    # Condition 2 : Vérifier si le "type_name" est "Rendez-vous"
    if data.get('current', {}).get('type_name') != 'Rendez-vous':
        return False

    # Condition 3 : Vérifier si le "type" est "meeting"
    if data.get('current', {}).get('type') != 'meeting':
        return False

    # # Condition 4 : Vérifier si le "user_id" est 13009293
    # if data.get('meta', {}).get('user_id') != 13009293:
    #    return False

    # Condition 5 : Vérifier s'il n'y a pas d'invités dans "attendees"
    attendees = data.get('current', {}).get('attendees')
    if attendees is not None and len(attendees) > 0:
        return False

    # Si toutes les conditions sont remplies, retourner True
    return True
