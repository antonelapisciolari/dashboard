from variables import celeste, amarillo, aquamarine, azul, orange, teal, gris
import re 
def filter_dataframe(df, filters):
    for column, value in filters.items():
        df = df[df[column].isin(value)]
    return df

def getColumns(df, columns):
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Columns not found in DataFrame: {missing_columns}")
        
        return df[columns]

import itertools

def generate_color_map(df, column_name):
    # Define a base list of colors to use
    base_colors = [
        aquamarine,  # Aquamarine
        amarillo,  # Yellow
        azul,  # Blue
        orange,  # Orange
        celeste,  # Light Blue
        teal,  # Teal
        gris,  # Gray
        "#9467BD"   # Purple
    ]
    
    # Get unique departments
    unique_departments = df[column_name].unique()
    
    # Cycle through colors if there are more departments than base colors
    color_cycle = itertools.cycle(base_colors)
    
    # Create a dictionary mapping each department to a color
    color_map = {dept: next(color_cycle) for dept in unique_departments}
    
    return color_map


def is_valid_email(email):
    # Simple regex for validating an email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

columnStatus = 'STATUS'
def calcularPorcentajesStatus(df):
    aprendicesStatus = getColumns(df, [columnStatus])
    total_statuses = len(aprendicesStatus)
    finalizado_count = df[columnStatus].str.lower().eq('finalizado').sum()
    baja_count = df[columnStatus].str.lower().eq('baja').sum()
    activo_count = df[columnStatus].str.lower().eq('activo').sum()
    baja_pct =0
    finalizado_pct=0
    # Calcular los porcentajes
    if finalizado_count != 0:
       finalizado_pct = int((finalizado_count / total_statuses) * 100) 
    if baja_count !=0:
        baja_pct = int((baja_count / total_statuses) * 100)
    return finalizado_pct, baja_pct,activo_count, baja_count,finalizado_count