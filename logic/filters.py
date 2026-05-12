"""
Lógica pura de filtrado. Determinista: mismo DF + filtros -> mismo resultado.
"""

def apply_search_filters(df, budget, selected_zones, selected_mood):
    """
    Filtra el DataFrame según criterios de usuario.
    Inputs: df (pd.DataFrame), budget (int), selected_zones (list), selected_mood (str)
    Outputs: pd.DataFrame filtrado.
    """
    if df.empty:
        return df

    mask = (df['precio_avg'] <= budget) & (df['zona'].isin(selected_zones))
    
    if selected_mood != "Todos":
        mask &= (df['mood'] == selected_mood)
        
    return df[mask]
