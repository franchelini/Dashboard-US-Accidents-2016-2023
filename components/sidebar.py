import streamlit as st

def create_sidebar(df):
    """Crear sidebar con filtros"""
    st.sidebar.header("🔧 Filtros")
    
    # Filtro de estados
    states = st.sidebar.multiselect(
        "Seleccionar Estados:",
        options=sorted(df['State'].unique()),
        default=None,
        help="Selecciona uno o más estados para filtrar"
    )
    
    # Filtro de severidad
    severity = st.sidebar.multiselect(
        "Nivel de Severidad:",
        options=sorted(df['Severity'].unique()),
        default=None,
        help="1=Menor, 4=Mayor severidad"
    )
    
    # Filtro de condiciones climáticas
    weather = st.sidebar.multiselect(
        "Condiciones Climáticas:",
        options=sorted(df['Weather_Condition'].unique()),
        default=None,
        help="Selecciona condiciones climáticas específicas"
    )
    
    # Selector de variable para boxplot
    st.sidebar.header("📊 Variables Climáticas")
    variable_boxplot = st.sidebar.selectbox(
        "Variable para Boxplot:",
        options=['Temperature(F)', 'Humidity(%)', 'Visibility(mi)'],
        format_func=lambda x: {
            'Temperature(F)': 'Temperatura (°F)',
            'Humidity(%)': 'Humedad (%)',
            'Visibility(mi)': 'Visibilidad (mi)'
        }[x]
    )
    
    # Información del dataset
    st.sidebar.header("ℹ️ Información")
    st.sidebar.info(f"""
    **Total de registros:** {len(df):,}
    **Estados:** {df['State'].nunique()}
    **Ciudades:** {df['City'].nunique()}
    **Condiciones climáticas:** {df['Weather_Condition'].nunique()}
    """)
    
    return {
        'states': states,
        'severity': severity,
        'weather': weather,
        'boxplot_variable': variable_boxplot
    }