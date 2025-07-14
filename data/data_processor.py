import pandas as pd
import streamlit as st

class DataProcessor:
    def process_data(self, df):
        """Procesar y limpiar los datos"""
        # Limpiar datos faltantes en columnas críticas
        df = df.dropna(subset=['State', 'Weather_Condition', 'Severity'])
        
        # Limpiar y validar columna City
        df['City'] = df['City'].astype(str)
        df = df[df['City'] != 'nan']  # Eliminar strings 'nan'
        df = df[df['City'].str.len() > 0]  # Eliminar strings vacíos
        
        # Convertir Severity a numérico manteniendo el orden
        df['Severity'] = pd.to_numeric(df['Severity'], errors='coerce')
        df = df.dropna(subset=['Severity'])  # Eliminar filas con Severity no válida
        
        # Limpiar Weather_Condition
        df['Weather_Condition'] = df['Weather_Condition'].astype(str)
        df = df[df['Weather_Condition'] != 'nan']
        df = df[df['Weather_Condition'].str.len() > 0]
        
        # Procesar fechas
        df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='mixed', errors='coerce')
        df = df.dropna(subset=['Start_Time'])  # Eliminar filas sin fecha válida
        df['YearMonth'] = df['Start_Time'].dt.to_period('M').astype(str)
        
        # Rellenar valores faltantes en variables numéricas
        numeric_cols = ['Temperature(F)', 'Humidity(%)', 'Visibility(mi)']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].median())
        
        # Convertir variables booleanas
        boolean_cols = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 
                       'No_Exit', 'Railway', 'Roundabout', 'Station', 'Stop', 
                       'Traffic_Calming', 'Traffic_Signal', 'Turning_Loop']
        
        for col in boolean_cols:
            if col in df.columns:
                df[col] = df[col].fillna(False)
        
        # Limpiar Sunrise_Sunset
        if 'Sunrise_Sunset' in df.columns:
            df['Sunrise_Sunset'] = df['Sunrise_Sunset'].fillna('Unknown')
        
        # Resetear índice después de todas las operaciones de limpieza
        df = df.reset_index(drop=True)
        
        return df