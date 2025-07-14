import pandas as pd
import streamlit as st

class DataProcessor:
    def process_data(self, df):
        """Procesar y limpiar los datos"""
        # Limpiar datos faltantes
        df = df.dropna(subset=['State', 'Weather_Condition', 'Severity'])
        
        # Convertir Severity a numérico manteniendo el orden
        df['Severity'] = pd.to_numeric(df['Severity'], errors='coerce')
        df = df.dropna(subset=['Severity'])  # Eliminar filas con Severity no válida
        
        # Procesar fechas
        df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='mixed', errors='coerce')
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
        
        return df