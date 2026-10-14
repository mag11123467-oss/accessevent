def format_event_response(event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_date": (event.event_date.isoformat() if event.event_date else None),
        "location": event.location,
        "organizer_id": event.organizer_id,
        "accessibility": {
            "is_inclusive": event.is_inclusive,
            "sign_language": event.sign_language,
            "visual_alerts": event.visual_alerts,
        },
    }


def build_accessibility_description(event):
    features = []
    if event.is_inclusive:
        features.append("инклюзивное мероприятие")
    if event.sign_language:
        features.append("сурдоперевод")
    if event.visual_alerts:
        features.append("визуальные оповещения")
    return ", ".join(features) if features else "особые условия не заявлены"


def mark_event_inclusive(event):
    event.is_inclusive = True
    event.visual_alerts = True
    return "Мероприятие отмечено как инклюзивное"