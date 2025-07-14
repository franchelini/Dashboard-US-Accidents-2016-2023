import streamlit as st
from charts.chart_generators import ChartGenerator
import plotly.express as px
import pandas as pd

def create_dashboard_layout(df):
    """Crear el layout principal del dashboard compacto"""
    
    # Obtener datos filtrados del sidebar
    df_filtered = st.session_state.get('df_filtered', df)
    
    # Layout de 2 filas, con alturas específicas
    
    # FILA 1: Mapa grande + 2 gráficos pequeños
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        create_map_section(df_filtered)
    
    with row1_col2:
        create_weather_section(df_filtered)
        create_severity_metrics(df_filtered)
    
    # FILA 2: 3 gráficos medianos
    row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])
    
    with row2_col1:
        create_cities_section(df_filtered)
    
    with row2_col2:
        create_temporal_section(df_filtered)
    
    with row2_col3:
        create_infrastructure_section(df_filtered)

def create_map_section(df):
    """Crear sección del mapa compacta"""
    with st.container():
        st.markdown('<div class="chart-container" style="height: 400px; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🗺️ Distribución Geográfica</div>', unsafe_allow_html=True)
        
        # Generar mapa
        generator = ChartGenerator(df)
        fig_map = generator.generate_mapa()
        fig_map.update_layout(
            height=360,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def create_weather_section(df):
    """Crear sección del clima compacta"""
    with st.container():
        st.markdown('<div class="chart-container" style="height: 190px; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🌤️ Clima Top 10</div>', unsafe_allow_html=True)
        
        # Generar gráfico compacto
        weather_counts = df['Weather_Condition'].value_counts().nlargest(10).reset_index()
        weather_counts.columns = ['Weather_Condition', 'Count']
        
        fig_weather = px.bar(
            weather_counts,
            x='Count',
            y='Weather_Condition',
            orientation='h',
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig_weather.update_layout(
            height=160,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            yaxis={'categoryorder':'total ascending', 'title': ''},
            xaxis={'title': ''},
            font=dict(size=9)
        )
        
        st.plotly_chart(fig_weather, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def create_severity_metrics(df):
    """Crear métricas de severidad compactas con explicación"""
    with st.container():
        st.markdown('<div class="chart-container" style="height: 200px; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Severidad por Niveles</div>', unsafe_allow_html=True)
        
        # Distribución de severidad con colores específicos
        severity_counts = df['Severity'].value_counts().sort_index()
        
        # Colores correctos para cada nivel
        colors = {
            1: '#22c55e',  # Verde - Leve
            2: '#eab308',  # Amarillo - Moderada
            3: '#f97316',  # Naranja - Severa
            4: '#dc2626'   # Rojo - Muy Severa
        }
        
        # Descripciones para cada nivel
        descriptions = {
            1: 'Leve',
            2: 'Moderada',
            3: 'Severa',
            4: 'Muy Severa'
        }
        
        # Crear etiquetas con nivel y descripción
        labels = [f"Nivel {level} - {descriptions.get(level, 'N/A')}" for level in severity_counts.index]
        
        # Crear el gráfico de pie
        fig_severity = px.pie(
            values=severity_counts.values,
            names=labels,
            title=""
        )
        
        # Asignar colores manualmente a cada segmento
        fig_severity.update_traces(
            marker=dict(
                colors=[colors.get(level, '#gray') for level in severity_counts.index]
            ),
            textposition='inside',
            textinfo='percent',
            hovertemplate='<b>%{label}</b><br>' +
                         'Cantidad: %{value}<br>' +
                         'Porcentaje: %{percent}<br>' +
                         '<extra></extra>'
        )
        
        fig_severity.update_layout(
            height=170,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.15, 
                xanchor="center", 
                x=0.5,
                font=dict(size=7)
            ),
            font=dict(size=9)
        )
        
        st.plotly_chart(fig_severity, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def create_cities_section(df):
    """Crear sección de ciudades compacta"""
    with st.container():
        st.markdown('<div class="chart-container" style="height: 280px; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏙️ Top 15 Ciudades</div>', unsafe_allow_html=True)
        
        # Generar gráfico
        city_counts = df['City'].value_counts().nlargest(15).reset_index()
        city_counts.columns = ['City', 'Count']
        
        fig_cities = px.bar(
            city_counts,
            x='City',
            y='Count',
            color='Count',
            color_continuous_scale='Plasma'
        )
        fig_cities.update_layout(
            height=240,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_tickangle=-45,
            showlegend=False,
            xaxis={'title': ''},
            yaxis={'title': ''},
            font=dict(size=8)
        )
        
        st.plotly_chart(fig_cities, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def create_temporal_section(df):
    """Crear sección temporal compacta"""
    with st.container():
        st.markdown('<div class="chart-container" style="height: 280px; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Tendencia Mensual</div>', unsafe_allow_html=True)
        
        # Análisis mensual
        monthly_counts = df['YearMonth'].value_counts().sort_index().reset_index()
        monthly_counts.columns = ['YearMonth', 'Count']
        
        fig_temporal = px.line(
            monthly_counts,
            x='YearMonth',
            y='Count',
            markers=True,
            line_shape='spline'
        )
        fig_temporal.update_layout(
            height=240,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_tickangle=-45,
            showlegend=False,
            xaxis={'title': ''},
            yaxis={'title': ''},
            font=dict(size=8)
        )
        
        st.plotly_chart(fig_temporal, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def create_infrastructure_section(df):
    """Crear sección de infraestructura compacta"""
    with st.container():
        st.markdown('<div class="chart-container" style="height: 280px; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏗️ Infraestructura</div>', unsafe_allow_html=True)
        
        # Generar treemap
        infra_vars = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
                      'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
                      'Traffic_Signal', 'Turning_Loop']
        
        infra_data = []
        for var in infra_vars:
            if var in df.columns:
                total = df[var].sum()
                if total > 0:
                    nocturnos = df[(df[var] == True) & (df['Sunrise_Sunset'] == 'Night')].shape[0]
                    porcentaje_nocturno = (nocturnos / total) * 100
                    
                    infra_data.append({
                        'Infraestructura': var,
                        'Count': total,
                        'Porcentaje_Nocturno': porcentaje_nocturno
                    })
        
        if infra_data:
            infra_df = pd.DataFrame(infra_data).sort_values('Count', ascending=False)
            
            fig_treemap = px.treemap(
                infra_df,
                path=['Infraestructura'],
                values='Count',
                color='Porcentaje_Nocturno',
                color_continuous_scale='Viridis',
                hover_data=['Count', 'Porcentaje_Nocturno']
            )
            fig_treemap.update_layout(
                height=240,
                margin=dict(l=0, r=0, t=0, b=0),
                font=dict(size=8)
            )
            
            st.plotly_chart(fig_treemap, use_container_width=True)
            
            # Pequeña explicación
            st.markdown("""
            <div style="font-size: 0.7rem; color: #6b7280; text-align: center; margin-top: 0.25rem;">
                💡 Tamaño = Frecuencia | Color = % Nocturnos
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos de infraestructura disponibles")
        
        st.markdown('</div>', unsafe_allow_html=True)