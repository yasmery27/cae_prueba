def validate_event(event):
    required_fields = [
        "Evento",
        "Zona",
        "Precio",
        "Horario"
    ]

    for field in required_fields:
        if field not in event:
            return False

    return True
