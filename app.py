import streamlit as st
import pandas as pd
import plotly.express as px
from data.data_loader import DataLoader
from charts.chart_generators import ChartGenerator
from components.header import create_header
from components.dashboard_layout import create_dashboard_layout

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Accidentes Viales en EE.UU.",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para layout sin scroll

st.markdown("""
<style>
    .main > div {
        padding-top: 0.2rem;
        padding-left: 0.2rem;
        padding-right: 0.2rem;
        padding-bottom: 0.2rem;
    }
    
    .dashboard-container {
        background: transparent;
        padding: 0.05rem;
        border-radius: 8px;
        margin-bottom: 0.05rem;
    }
    
    .metric-container {
        background: transparent;
        padding: 0.15rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.10rem;
    }
    
    .chart-container {
        background: transparent;
        padding: 0.05rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 0.05rem;
        overflow: hidden;
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.25rem;
    }
    
    .filter-section {
        background: #f3f4f6;
        padding: 0.25rem;
        border-radius: 4px;
        margin-bottom: 0.25rem;
    }
    
    .compact-metric {
        text-align: center;
        padding: 0.25rem;
    }
    
    .compact-metric .metric-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f2937;
    }
    
    .compact-metric .metric-label {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    .stSelectbox > div > div > div {
        background-color: white;
        min-height: 30px;
    }
    
    .stMultiSelect > div > div > div {
        background-color: white;
        min-height: 30px;
    }
    
    .stSlider > div > div > div {
        min-height: 30px;
    }
    
    /* Reducir altura de expanders */
    .streamlit-expanderHeader {
        font-size: 0.9rem;
        padding: 0.25rem;
    }
    
    .streamlit-expanderContent {
        padding: 0.25rem;
    }
    
    /* Eliminar espacios extra */
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    
    /* Ajustar espacios entre gráficos */
    .stPlotlyChart {
        margin-bottom: 0;
    }
    
    /* Ocultar botones de plotly */
    .modebar {
        display: none !important;
    }
    
    /* Reducir espacios entre columnas */
    .stColumn > div {
        padding-left: 0.25rem;
        padding-right: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)


# Cache para datos
@st.cache_data
def load_data():
    """Cargar datos con cache"""
    loader = DataLoader()
    return loader.load_data()

def get_safe_unique_values(series, max_items=None):
    """Obtener valores únicos de una serie manejando NaN"""
    try:
        # Eliminar NaN y convertir a string si es necesario
        clean_values = series.dropna().astype(str).unique()
        # Ordenar y limitar si es necesario
        sorted_values = sorted(clean_values)
        if max_items:
            return sorted_values[:max_items]
        return sorted_values
    except Exception as e:
        st.error(f"Error procesando valores únicos: {e}")
        return []

def main():
    # Cargar datos
    with st.spinner('Cargando datos...'):
        df = load_data()
    
    # Crear sidebar con filtros globales
    create_sidebar(df)
    
    # Crear header compacto con métricas principales
    create_header(df)
    
    # Crear layout del dashboard
    create_dashboard_layout(df)

def create_sidebar(df):
    """Crear sidebar con filtros globales"""
    st.sidebar.header("🎛️ Filtros Globales")
    
    # Filtros globales que afectan todo el dashboard
    with st.sidebar.expander("🗺️ Filtros Geográficos", expanded=True):
        # Estados - manejo seguro de valores únicos
        state_options = get_safe_unique_values(df['State'])
        global_states = st.multiselect(
            "Estados:",
            options=state_options,
            default=None,
            key="global_states"
        )
        
        # Ciudades - manejo seguro con límite
        city_options = get_safe_unique_values(df['City'], max_items=50)
        global_cities = st.multiselect(
            "Ciudades (Top 50):",
            options=city_options,
            default=None,
            key="global_cities"
        )
    
    with st.sidebar.expander("⚠️ Filtros de Severidad", expanded=False):
        # Severidad - convertir a string para manejar correctamente
        severity_options = sorted([str(x) for x in df['Severity'].dropna().unique()])
        global_severity = st.multiselect(
            "Niveles de severidad:",
            options=severity_options,
            default=severity_options,
            key="global_severity"
        )
    
    with st.sidebar.expander("🌤️ Filtros Climáticos", expanded=False):
        # Condiciones climáticas - manejo seguro
        weather_options = get_safe_unique_values(df['Weather_Condition'], max_items=20)
        global_weather = st.multiselect(
            "Condiciones climáticas (Top 20):",
            options=weather_options,
            default=None,
            key="global_weather"
        )
    
    # Aplicar filtros globales
    if 'df_filtered' not in st.session_state:
        st.session_state.df_filtered = df.copy()
    
    df_filtered = df.copy()
    
    try:
        # Aplicar filtros con manejo de errores
        if global_states:
            df_filtered = df_filtered[df_filtered['State'].isin(global_states)]
        
        if global_cities:
            df_filtered = df_filtered[df_filtered['City'].astype(str).isin(global_cities)]
        
        if global_severity:
            # Convertir severidad a string para comparación
            df_filtered = df_filtered[df_filtered['Severity'].astype(str).isin(global_severity)]
        
        if global_weather:
            df_filtered = df_filtered[df_filtered['Weather_Condition'].astype(str).isin(global_weather)]
        
    except Exception as e:
        st.sidebar.error(f"Error aplicando filtros: {e}")
        df_filtered = df.copy()  # Usar datos originales si hay error
    
    st.session_state.df_filtered = df_filtered
    
    # Información del dataset filtrado
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Información")
    
    try:
        active_filters = sum([
            bool(global_states), 
            bool(global_cities), 
            bool(global_severity and len(global_severity) < len(severity_options)), 
            bool(global_weather)
        ])
        
        st.sidebar.info(f"""
        **Registros:** {len(df_filtered):,}
        **Estados:** {df_filtered['State'].nunique()}
        **Ciudades:** {df_filtered['City'].nunique()}
        **Filtros activos:** {active_filters}
        """)
    except Exception as e:
        st.sidebar.error(f"Error mostrando información: {e}")

if __name__ == "__main__":
    main()