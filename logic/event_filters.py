def filter_events(events, budget, zone, schedule):
    filtered = []

    for event in events:
        matches_budget = budget == "Todos" or event["Precio"] == budget
        matches_zone = zone == "Todas" or event["Zona"] == zone
        matches_schedule = schedule == "Todos" or event["Horario"] == schedule

        if matches_budget and matches_zone and matches_schedule:
            filtered.append(event)

    return filtered
