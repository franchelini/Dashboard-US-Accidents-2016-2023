import streamlit as st
from charts.chart_generators import ChartGenerator
import plotly.express as px
import pandas as pd

def create_dashboard_layout(df):
    """Crear el layout principal del dashboard interactivo"""
    
    # Obtener datos filtrados del sidebar
    df_filtered = st.session_state.get('df_filtered', df)
    
    # Título principal del dashboard
    st.markdown("## 📊 Dashboard de Análisis de Accidentes de Tráfico")
    st.markdown("---")
    
    # SECCIÓN 1: Mapa principal (destacado)
    st.markdown("### 🗺️ Vista Geográfica Principal")
    with st.expander("🔍 Ver Mapa Interactivo Completo", expanded=True):
        create_map_section_interactive(df_filtered)
    
    st.markdown("---")
    
    # SECCIÓN 2: Análisis de Clima y Severidad
    st.markdown("### 🌤️ Análisis de Condiciones")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.expander("🌦️ Condiciones Climáticas", expanded=True):
            create_weather_section_interactive(df_filtered)
    
    with col2:
        with st.expander("📊 Niveles de Severidad", expanded=True):
            create_severity_metrics_interactive(df_filtered)
    
    st.markdown("---")
    
    # SECCIÓN 3: Análisis Temporal y Geográfico
    st.markdown("### 📈 Análisis Temporal y Ubicaciones")
    col3, col4 = st.columns([1, 1])
    
    with col3:
        with st.expander("🏙️ Ciudades con Más Accidentes", expanded=True):
            create_cities_section_interactive(df_filtered)
    
    with col4:
        with st.expander("📅 Tendencias Temporales", expanded=True):
            create_temporal_section_interactive(df_filtered)
    
    st.markdown("---")
    
    # SECCIÓN 4: Infraestructura
    st.markdown("### 🏗️ Análisis de Infraestructura")
    with st.expander("🛣️ Infraestructura y Accidentes Nocturnos", expanded=True):
        create_infrastructure_section_interactive(df_filtered)

def create_map_section_interactive(df):
    """Crear sección del mapa interactiva y expandida"""
    with st.container():
        # Métricas rápidas del mapa
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Accidentes", f"{len(df):,}")
        with col2:
            st.metric("Estados", df['State'].nunique())
        with col3:
            st.metric("Ciudades", df['City'].nunique())
        with col4:
            avg_severity = df['Severity'].mean()
            st.metric("Severidad Promedio", f"{avg_severity:.1f}")
        
        # Generar mapa expandido
        generator = ChartGenerator(df)
        fig_map = generator.generate_mapa()
        fig_map.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)

def create_weather_section_interactive(df):
    """Crear sección del clima interactiva y expandida"""
    with st.container():
        # Métricas rápidas del clima
        col1, col2, col3 = st.columns(3)
        with col1:
            most_common_weather = df['Weather_Condition'].mode().iloc[0] if not df['Weather_Condition'].mode().empty else "N/A"
            st.metric("Condición Más Común", most_common_weather)
        with col2:
            unique_conditions = df['Weather_Condition'].nunique()
            st.metric("Condiciones Únicas", unique_conditions)
        with col3:
            weather_accidents = len(df[df['Weather_Condition'] != 'Clear'])
            weather_pct = (weather_accidents / len(df)) * 100
            st.metric("% Con Mal Clima", f"{weather_pct:.1f}%")
        
        # Opciones de visualización
        view_type = st.radio("Tipo de vista:", ["Top 10", "Top 20", "Comparación por Severidad"], horizontal=True)
        
        if view_type == "Top 10":
            weather_counts = df['Weather_Condition'].value_counts().nlargest(10).reset_index()
            weather_counts.columns = ['Weather_Condition', 'Count']
            
            fig_weather = px.bar(
                weather_counts,
                x='Count',
                y='Weather_Condition',
                orientation='h',
                color='Count',
                color_continuous_scale='Viridis',
                title="Top 10 Condiciones Climáticas"
            )
            
        elif view_type == "Top 20":
            weather_counts = df['Weather_Condition'].value_counts().nlargest(20).reset_index()
            weather_counts.columns = ['Weather_Condition', 'Count']
            
            fig_weather = px.bar(
                weather_counts,
                x='Weather_Condition',
                y='Count',
                color='Count',
                color_continuous_scale='Viridis',
                title="Top 20 Condiciones Climáticas"
            )
            fig_weather.update_layout(xaxis_tickangle=-45)
            
        else:  # Comparación por Severidad
            weather_severity = df.groupby(['Weather_Condition', 'Severity']).size().reset_index(name='Count')
            top_weather = df['Weather_Condition'].value_counts().nlargest(8).index
            weather_severity_filtered = weather_severity[weather_severity['Weather_Condition'].isin(top_weather)]
            
            fig_weather = px.bar(
                weather_severity_filtered,
                x='Weather_Condition',
                y='Count',
                color='Severity',
                title="Accidentes por Clima y Severidad (Top 8)",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_weather.update_layout(xaxis_tickangle=-45)
        
        fig_weather.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=40, b=10),
            yaxis={'categoryorder':'total ascending'} if view_type == "Top 10" else {},
            font=dict(size=11)
        )
        
        st.plotly_chart(fig_weather, use_container_width=True)

def create_severity_metrics_interactive(df):
    """Crear métricas de severidad interactivas y expandidas"""
    with st.container():
        # Métricas rápidas de severidad
        col1, col2, col3, col4 = st.columns(4)
        severity_counts = df['Severity'].value_counts().sort_index()
        
        with col1:
            if 1 in severity_counts.index:
                st.metric("Nivel 1 (Leve)", f"{severity_counts[1]:,}")
        with col2:
            if 2 in severity_counts.index:
                st.metric("Nivel 2 (Moderada)", f"{severity_counts[2]:,}")
        with col3:
            if 3 in severity_counts.index:
                st.metric("Nivel 3 (Severa)", f"{severity_counts[3]:,}")
        with col4:
            if 4 in severity_counts.index:
                st.metric("Nivel 4 (Muy Severa)", f"{severity_counts[4]:,}")
        
        # Opciones de visualización
        chart_type = st.radio("Tipo de gráfico:", ["Gráfico de Torta", "Gráfico de Barras", "Por Estados"], horizontal=True)
        
        if chart_type == "Gráfico de Torta":
            # Colores correctos para cada nivel
            colors = {1: '#22c55e', 2: '#eab308', 3: '#f97316', 4: '#dc2626'}
            descriptions = {1: 'Leve', 2: 'Moderada', 3: 'Severa', 4: 'Muy Severa'}
            labels = [f"Nivel {level} - {descriptions.get(level, 'N/A')}" for level in severity_counts.index]
            
            fig_severity = px.pie(
                values=severity_counts.values,
                names=labels,
                title="Distribución de Severidad"
            )
            fig_severity.update_traces(
                marker=dict(colors=[colors.get(level, '#gray') for level in severity_counts.index]),
                textposition='inside', textinfo='percent+value'
            )
            
        elif chart_type == "Gráfico de Barras":
            severity_df = severity_counts.reset_index()
            severity_df.columns = ['Severity', 'Count']
            severity_df['Description'] = severity_df['Severity'].map({1: 'Leve', 2: 'Moderada', 3: 'Severa', 4: 'Muy Severa'})
            severity_df['Label'] = 'Nivel ' + severity_df['Severity'].astype(str) + ' - ' + severity_df['Description']
            
            fig_severity = px.bar(
                severity_df,
                x='Label',
                y='Count',
                color='Severity',
                title="Cantidad de Accidentes por Severidad",
                color_continuous_scale=['#22c55e', '#eab308', '#f97316', '#dc2626']
            )
            
        else:  # Por Estados
            state_severity = df.groupby(['State', 'Severity']).size().reset_index(name='Count')
            top_states = df['State'].value_counts().nlargest(10).index
            state_severity_filtered = state_severity[state_severity['State'].isin(top_states)]
            
            fig_severity = px.bar(
                state_severity_filtered,
                x='State',
                y='Count',
                color='Severity',
                title="Severidad por Estados (Top 10)",
                color_discrete_sequence=['#22c55e', '#eab308', '#f97316', '#dc2626']
            )
            fig_severity.update_layout(xaxis_tickangle=-45)
        
        fig_severity.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(size=10)
        )
        
        st.plotly_chart(fig_severity, use_container_width=True)

def create_cities_section_interactive(df):
    """Crear sección de ciudades interactiva y expandida"""
    with st.container():
        # Métricas rápidas de ciudades
        col1, col2, col3 = st.columns(3)
        with col1:
            top_city = df['City'].value_counts().index[0] if len(df) > 0 else "N/A"
            top_city_count = df['City'].value_counts().iloc[0] if len(df) > 0 else 0
            st.metric("Ciudad #1", f"{top_city}", f"{top_city_count:,} accidentes")
        with col2:
            total_cities = df['City'].nunique()
            st.metric("Total Ciudades", f"{total_cities:,}")
        with col3:
            avg_per_city = len(df) / total_cities if total_cities > 0 else 0
            st.metric("Promedio por Ciudad", f"{avg_per_city:.1f}")
        
        # Opciones de visualización
        view_options = st.radio("Mostrar:", ["Top 10", "Top 20", "Por Estado"], horizontal=True)
        
        if view_options == "Top 10":
            city_counts = df['City'].value_counts().nlargest(10).reset_index()
            city_counts.columns = ['City', 'Count']
            
            fig_cities = px.bar(
                city_counts,
                x='Count',
                y='City',
                orientation='h',
                color='Count',
                color_continuous_scale='Plasma',
                title="Top 10 Ciudades con Más Accidentes"
            )
            fig_cities.update_layout(yaxis={'categoryorder':'total ascending'})
            
        elif view_options == "Top 20":
            city_counts = df['City'].value_counts().nlargest(20).reset_index()
            city_counts.columns = ['City', 'Count']
            
            fig_cities = px.bar(
                city_counts,
                x='City',
                y='Count',
                color='Count',
                color_continuous_scale='Plasma',
                title="Top 20 Ciudades con Más Accidentes"
            )
            fig_cities.update_layout(xaxis_tickangle=-45)
            
        else:  # Por Estado
            state_city = df.groupby(['State', 'City']).size().reset_index(name='Count')
            top_states = df['State'].value_counts().nlargest(5).index
            state_city_filtered = state_city[state_city['State'].isin(top_states)]
            top_cities_per_state = state_city_filtered.groupby('State').apply(
                lambda x: x.nlargest(3, 'Count')
            ).reset_index(drop=True)
            
            fig_cities = px.bar(
                top_cities_per_state,
                x='City',
                y='Count',
                color='State',
                title="Top 3 Ciudades por Estado (Top 5 Estados)",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_cities.update_layout(xaxis_tickangle=-45)
        
        fig_cities.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(size=10)
        )
        
        st.plotly_chart(fig_cities, use_container_width=True)

def create_temporal_section_interactive(df):
    """Crear sección temporal interactiva y expandida"""
    with st.container():
        # Métricas rápidas temporales
        col1, col2, col3 = st.columns(3)
        with col1:
            if 'Start_Time' in df.columns:
                df['Year'] = pd.to_datetime(df['Start_Time']).dt.year
                peak_year = df['Year'].value_counts().index[0]
                peak_year_count = df['Year'].value_counts().iloc[0]
                st.metric("Año Pico", f"{peak_year}", f"{peak_year_count:,} accidentes")
        with col2:
            if 'YearMonth' in df.columns:
                total_months = df['YearMonth'].nunique()
                st.metric("Meses Analizados", f"{total_months}")
        with col3:
            if 'YearMonth' in df.columns:
                avg_monthly = len(df) / total_months if total_months > 0 else 0
                st.metric("Promedio Mensual", f"{avg_monthly:.0f}")
        
        # Opciones de visualización
        time_view = st.radio("Vista temporal:", ["Tendencia Mensual", "Por Años", "Por Meses del Año"], horizontal=True)
        
        if time_view == "Tendencia Mensual":
            if 'YearMonth' in df.columns:
                monthly_counts = df['YearMonth'].value_counts().sort_index().reset_index()
                monthly_counts.columns = ['YearMonth', 'Count']
                
                fig_temporal = px.line(
                    monthly_counts,
                    x='YearMonth',
                    y='Count',
                    markers=True,
                    line_shape='spline',
                    title="Evolución Mensual de Accidentes"
                )
                fig_temporal.update_layout(xaxis_tickangle=-45)
                
        elif time_view == "Por Años":
            if 'Start_Time' in df.columns:
                df['Year'] = pd.to_datetime(df['Start_Time']).dt.year
                yearly_counts = df['Year'].value_counts().sort_index().reset_index()
                yearly_counts.columns = ['Year', 'Count']
                
                fig_temporal = px.bar(
                    yearly_counts,
                    x='Year',
                    y='Count',
                    color='Count',
                    color_continuous_scale='Viridis',
                    title="Accidentes por Año"
                )
                
        else:  # Por Meses del Año
            if 'Start_Time' in df.columns:
                df['Month'] = pd.to_datetime(df['Start_Time']).dt.month
                month_names = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
                              7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
                monthly_counts = df['Month'].value_counts().sort_index().reset_index()
                monthly_counts.columns = ['Month', 'Count']
                monthly_counts['Month_Name'] = monthly_counts['Month'].map(month_names)
                
                fig_temporal = px.bar(
                    monthly_counts,
                    x='Month_Name',
                    y='Count',
                    color='Count',
                    color_continuous_scale='Blues',
                    title="Distribución por Meses del Año"
                )
        
        fig_temporal.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(size=10)
        )
        
        st.plotly_chart(fig_temporal, use_container_width=True)

def create_infrastructure_section_interactive(df):
    """Crear sección de infraestructura interactiva y expandida"""
    with st.container():
        # Métricas rápidas de infraestructura
        infra_vars = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
                      'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
                      'Traffic_Signal', 'Turning_Loop']
        
        available_infra = [var for var in infra_vars if var in df.columns]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_infra_accidents = sum(df[var].sum() for var in available_infra if var in df.columns)
            st.metric("Total con Infraestructura", f"{total_infra_accidents:,}")
        with col2:
            if available_infra:
                night_infra = sum(df[(df[var] == True) & (df['Sunrise_Sunset'] == 'Night')].shape[0] 
                                for var in available_infra)
                night_pct = (night_infra / total_infra_accidents * 100) if total_infra_accidents > 0 else 0
                st.metric("% Nocturnos", f"{night_pct:.1f}%")
        with col3:
            st.metric("Tipos Infraestructura", len(available_infra))
        
        # Opciones de visualización
        infra_view = st.radio("Vista infraestructura:", ["Treemap", "Gráfico de Barras", "Por Severidad"], horizontal=True)
        
        # Generar datos de infraestructura
        infra_data = []
        for var in available_infra:
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
            
            if infra_view == "Treemap":
                fig_infra = px.treemap(
                    infra_df,
                    path=['Infraestructura'],
                    values='Count',
                    color='Porcentaje_Nocturno',
                    color_continuous_scale='Viridis',
                    hover_data=['Count', 'Porcentaje_Nocturno'],
                    title="Infraestructura: Tamaño=Frecuencia, Color=%Nocturnos"
                )
                
            elif infra_view == "Gráfico de Barras":
                fig_infra = px.bar(
                    infra_df,
                    x='Infraestructura',
                    y='Count',
                    color='Porcentaje_Nocturno',
                    color_continuous_scale='Viridis',
                    title="Accidentes por Tipo de Infraestructura",
                    hover_data=['Porcentaje_Nocturno']
                )
                fig_infra.update_layout(xaxis_tickangle=-45)
                
            else:  # Por Severidad
                # Crear datos combinando infraestructura y severidad
                severity_infra_data = []
                for var in available_infra[:8]:  # Top 8 para mejor visualización
                    infra_accidents = df[df[var] == True]
                    if len(infra_accidents) > 0:
                        severity_dist = infra_accidents['Severity'].value_counts().sort_index()
                        for sev, count in severity_dist.items():
                            severity_infra_data.append({
                                'Infraestructura': var,
                                'Severity': sev,
                                'Count': count
                            })
                
                if severity_infra_data:
                    severity_infra_df = pd.DataFrame(severity_infra_data)
                    fig_infra = px.bar(
                        severity_infra_df,
                        x='Infraestructura',
                        y='Count',
                        color='Severity',
                        title="Severidad por Tipo de Infraestructura (Top 8)",
                        color_discrete_sequence=['#22c55e', '#eab308', '#f97316', '#dc2626']
                    )
                    fig_infra.update_layout(xaxis_tickangle=-45)
                else:
                    fig_infra = px.bar(title="No hay datos de severidad disponibles")
            
            fig_infra.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=40, b=10),
                font=dict(size=10),
                coloraxis_colorbar=dict(title="% Nocturnos") if infra_view != "Por Severidad" else {}
            )
            
            st.plotly_chart(fig_infra, use_container_width=True)
            
            # Explicación expandida
            if infra_view == "Treemap":
                st.markdown("""
                <div style="font-size: 0.8rem; color: #6b7280; text-align: center; margin-top: 0.5rem;">
                    💡 El tamaño representa la frecuencia de accidentes | El color indica el porcentaje de accidentes nocturnos
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay datos de infraestructura disponibles")