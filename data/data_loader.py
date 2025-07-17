import pandas as pd
import streamlit as st
from .data_processor import DataProcessor

class DataLoader:
    def __init__(self):
        self.processor = DataProcessor()
    
    def load_data(self):
        """Cargar y procesar el dataset"""
        try:
            # Progreso de carga
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text('Cargando archivo CSV...')
            progress_bar.progress(20)
            
            # Columnas necesarias
            columns_needed = [
                'State', 'City', 'Weather_Condition', 'Severity', 
                'Temperature(F)', 'Humidity(%)', 'Visibility(mi)',
                'Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 
                'No_Exit', 'Railway', 'Roundabout', 'Station', 'Stop', 
                'Traffic_Calming', 'Traffic_Signal', 'Turning_Loop',
                'Sunrise_Sunset', 'Start_Time'
            ]
            
            # Cargar datos
            df = pd.read_csv('D:\\US_Accidents_March23.csv\\US_Accidents_March23.csv', usecols=columns_needed)
            ##df = pd.read_csv('US_Accidents_March23.csv', usecols=columns_needed)
            progress_bar.progress(60)
            
            status_text.text('Procesando datos...')
            # Tomar muestra
            df_sample = df.sample(n=100000, random_state=42)
            progress_bar.progress(80)
            
            # Procesar datos
            df_processed = self.processor.process_data(df_sample)
            progress_bar.progress(100)
            
            status_text.text('Datos cargados exitosamente!')
            
            # Limpiar elementos de progreso
            progress_bar.empty()
            status_text.empty()
            
            return df_processed
            
        except FileNotFoundError:
            st.error("❌ Error: Archivo 'US_Accidents_March23.csv' no encontrado")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error al cargar datos: {e}")
            st.stop()