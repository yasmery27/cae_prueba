"""
Lógica pura para la gestión del itinerario de salida.
"""

def calculate_total_cost(itinerary_list):
    """
    Suma los precios promedio de los lugares seleccionados.
    Inputs: list of dicts. Outputs: int.
    """
    return sum(item.get('precio_avg', 0) for item in itinerary_list)

def is_budget_exceeded(current_total, limit):
    """Valida si el plan sobrepasa la 'funda de cuarto'."""
    return current_total > limit
