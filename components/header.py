import streamlit as st
from datetime import datetime

def create_header(df):
    """Crear header compacto con métricas principales"""
    
    # Obtener datos filtrados
    df_filtered = st.session_state.get('df_filtered', df)
    
    # Validar que hay datos
    if df_filtered.empty:
        st.error("No hay datos disponibles después de aplicar los filtros")
        return
    
    # Título principal compacto
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <h1 style="font-size: 1.8rem; color: #1f2937; margin: 0;">🚗 Dashboard de Accidentes Viales en EE.UU.</h1>
            <p style="font-size: 0.9rem; color: #6b7280; margin: 0;">Análisis de datos de accidentes de tráfico 2016-2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: right; margin-top: 0.5rem;">
            <div style="font-size: 0.8rem; color: #6b7280;">Última actualización</div>
            <div style="font-size: 0.9rem; color: #1f2937;">{datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas principales en una sola fila compacta
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="compact-metric">
            <div class="metric-value">{len(df_filtered):,}</div>
            <div class="metric-label">📊 Total Accidentes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        try:
            avg_severity = df_filtered['Severity'].mean()
            # Determinar color basado en severidad promedio
            if avg_severity <= 1.5:
                severity_color = "#22c55e"  # Verde - Baja
            elif avg_severity <= 2.5:
                severity_color = "#eab308"  # Amarillo - Media
            elif avg_severity <= 3.5:
                severity_color = "#f97316"  # Naranja - Alta
            else:
                severity_color = "#dc2626"  # Rojo - Muy Alta
            
            st.markdown(f"""
            <div class="compact-metric">
                <div class="metric-value" style="color: {severity_color};">{avg_severity:.2f}</div>
                <div class="metric-label">⚠️ Severidad Promedio</div>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div class="compact-metric">
                <div class="metric-value">N/A</div>
                <div class="metric-label">⚠️ Severidad Promedio</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="compact-metric">
            <div class="metric-value">{df_filtered['State'].nunique()}</div>
            <div class="metric-label">🗺️ Estados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        try:
            night_accidents = df_filtered[df_filtered['Sunrise_Sunset'] == 'Night'].shape[0]
            night_percentage = (night_accidents / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
            st.markdown(f"""
            <div class="compact-metric">
                <div class="metric-value">{night_percentage:.1f}%</div>
                <div class="metric-label">🌙 Nocturnos</div>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div class="compact-metric">
                <div class="metric-value">N/A</div>
                <div class="metric-label">🌙 Nocturnos</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="compact-metric">
            <div class="metric-value">{df_filtered['City'].nunique():,}</div>
            <div class="metric-label">🏙️ Ciudades</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        try:
            most_common_weather = df_filtered['Weather_Condition'].mode().iloc[0] if len(df_filtered) > 0 else "N/A"
            display_weather = most_common_weather[:8] + "..." if len(most_common_weather) > 8 else most_common_weather
            st.markdown(f"""
            <div class="compact-metric">
                <div class="metric-value" style="font-size: 0.9rem;">{display_weather}</div>
                <div class="metric-label">🌤️ Clima Común</div>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div class="compact-metric">
                <div class="metric-value">N/A</div>
                <div class="metric-label">🌤️ Clima Común</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Agregar explicación de severidad
    create_severity_legend(df_filtered)
    
    st.markdown("---")

def create_severity_legend(df):
    """Crear leyenda explicativa de los niveles de severidad"""
    
    # Obtener distribución de severidad
    try:
        severity_counts = df['Severity'].value_counts().sort_index()
        
        # Crear leyenda compacta
        st.markdown("""
        <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">
                📋 Escala de Severidad de Accidentes
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
        """, unsafe_allow_html=True)
        
        # Mostrar cada nivel con su color y descripción
        severity_info = {
            1: {"color": "#22c55e", "desc": "Leve", "detail": "Retrasos menores"},
            2: {"color": "#eab308", "desc": "Moderada", "detail": "Retrasos significativos"},
            3: {"color": "#f97316", "desc": "Severa", "detail": "Retrasos considerables"},
            4: {"color": "#dc2626", "desc": "Muy Severa", "detail": "Retrasos extremos"}
        }
        
        legend_items = []
        for level in [1, 2, 3, 4]:
            if level in severity_counts:
                count = severity_counts[level]
                percentage = (count / len(df)) * 100
                info = severity_info[level]
                
                legend_items.append(f"""
                <div style="display: flex; align-items: center; margin-right: 1rem;">
                    <div style="width: 12px; height: 12px; background: {info['color']}; border-radius: 50%; margin-right: 0.5rem;"></div>
                    <div style="font-size: 0.8rem;">
                        <strong>Nivel {level}</strong> - {info['desc']}<br>
                        <span style="color: #6b7280;">{count:,} casos ({percentage:.1f}%)</span>
                    </div>
                </div>
                """)
        
        st.markdown("".join(legend_items), unsafe_allow_html=True)
        
        st.markdown("""
            </div>
            <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem; text-align: center;">
                💡 La severidad se mide por el impacto en el flujo de tráfico y tiempo de resolución
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; color: #6b7280; text-align: center;">
                ⚠️ No se pudo cargar la información de severidad
            </div>
        </div>
        """, unsafe_allow_html=True)