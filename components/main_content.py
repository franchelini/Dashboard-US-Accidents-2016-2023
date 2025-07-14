import streamlit as st
from charts.chart_generators import ChartGenerator

def display_main_content(df, charts, filters):
    """Mostrar contenido principal del dashboard"""
    
    # Pestañas para organizar visualizaciones
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Mapa", "🌤️ Clima", "📊 Severidad", "🏗️ Infraestructura", "📈 Tendencias"
    ])
    
    with tab1:
        st.subheader("Distribución Geográfica de Accidentes")
        st.plotly_chart(charts['mapa'], use_container_width=True)
        
        # Información adicional
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Estados con más accidentes:**")
            top_states = df['State'].value_counts().head(5)
            for state, count in top_states.items():
                st.write(f"• {state}: {count:,} accidentes")
        
        with col2:
            st.info("**Estadísticas por región:**")
            st.write(f"• Total de estados: {df['State'].nunique()}")
            st.write(f"• Promedio por estado: {df['State'].value_counts().mean():.0f}")
    
    with tab2:
        st.subheader("Análisis de Condiciones Climáticas")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(charts['barras_clima'], use_container_width=True)
        
        with col2:
            st.info("**Condiciones más comunes:**")
            weather_stats = df['Weather_Condition'].value_counts().head(5)
            for condition, count in weather_stats.items():
                percentage = (count / len(df)) * 100
                st.write(f"• {condition}: {percentage:.1f}%")
    
    with tab3:
        st.subheader("Análisis de Severidad")
        
        # Usar variable del selector del sidebar
        variable = filters['boxplot_variable']
        
        generator = ChartGenerator(df)
        boxplot_fig = generator.generate_boxplot(variable)
        st.plotly_chart(boxplot_fig, use_container_width=True)
        
        # Estadísticas de severidad
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Distribución de Severidad:**")
            severity_stats = df['Severity'].value_counts().sort_index()
            for level, count in severity_stats.items():
                percentage = (count / len(df)) * 100
                st.write(f"• Nivel {level}: {count:,} ({percentage:.1f}%)")
        
        with col2:
            st.info("**Promedios por Severidad:**")
            avg_by_severity = df.groupby('Severity')[variable].mean()
            for level, avg in avg_by_severity.items():
                st.write(f"• Nivel {level}: {avg:.1f}")
    
    with tab4:
        st.subheader("Infraestructura Vial")
        st.plotly_chart(charts['treemap'], use_container_width=True)
        
        st.info("""
        **Interpretación:**
        - **Tamaño:** Frecuencia de accidentes cerca de esa infraestructura
        - **Color:** Porcentaje de accidentes nocturnos
        - **Colores más oscuros:** Mayor proporción de accidentes nocturnos
        """)
    
    with tab5:
        st.subheader("Tendencias Temporales")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.plotly_chart(charts['lineas_mes'], use_container_width=True)
            st.plotly_chart(charts['barras_ciudad'], use_container_width=True)
        
        with col2:
            st.info("**Análisis temporal:**")
            try:
                monthly_stats = df['YearMonth'].value_counts().sort_index()
                st.write(f"• Mes con más accidentes: {monthly_stats.idxmax()}")
                st.write(f"• Mes con menos accidentes: {monthly_stats.idxmin()}")
                st.write(f"• Promedio mensual: {monthly_stats.mean():.0f}")
            except:
                st.write("Error al calcular estadísticas temporales")
            
            st.info("**Top 3 ciudades:**")
            try:
                top_cities = df['City'].value_counts().head(3)
                for city, count in top_cities.items():
                    st.write(f"• {city}: {count:,}")
            except:
                st.write("Error al calcular top ciudades")