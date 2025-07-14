import streamlit as st
import pandas as pd
import plotly.express as px
from data.data_loader import DataLoader
from charts.chart_generators import ChartGenerator
from components.sidebar import create_sidebar
from components.main_content import display_main_content
from components.metrics import display_metrics

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Accidentes Viales en EE.UU.",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cache para datos
@st.cache_data
def load_data():
    """Cargar datos con cache"""
    loader = DataLoader()
    return loader.load_data()

# Cache para gráficos
@st.cache_data
def get_cached_charts(df):
    """Generar gráficos con cache"""
    generator = ChartGenerator(df)
    return {
        'mapa': generator.generate_mapa(),
        'barras_clima': generator.generate_barras_clima(),
        'barras_ciudad': generator.generate_barras_ciudad(),
        'treemap': generator.generate_treemap(),
        'lineas_mes': generator.generate_lineas_mes()
    }

def main():
    # Título principal
    st.markdown('<h1 class="main-header">🚗 Dashboard de Accidentes Viales en EE.UU.</h1>', unsafe_allow_html=True)
    
    # Cargar datos
    with st.spinner('Cargando datos...'):
        df = load_data()
    
    # Generar gráficos
    with st.spinner('Generando visualizaciones...'):
        charts = get_cached_charts(df)
    
    # Crear sidebar
    filters = create_sidebar(df)
    
    # Aplicar filtros
    df_filtered = apply_filters(df, filters)
    
    # Mostrar métricas
    display_metrics(df_filtered)
    
    # Mostrar contenido principal
    display_main_content(df_filtered, charts, filters)

def apply_filters(df, filters):
    """Aplicar filtros del sidebar"""
    df_filtered = df.copy()
    
    if filters['states']:
        df_filtered = df_filtered[df_filtered['State'].isin(filters['states'])]
    
    if filters['severity']:
        df_filtered = df_filtered[df_filtered['Severity'].isin(filters['severity'])]
    
    if filters['weather']:
        df_filtered = df_filtered[df_filtered['Weather_Condition'].isin(filters['weather'])]
    
    return df_filtered

if __name__ == "__main__":
    main()