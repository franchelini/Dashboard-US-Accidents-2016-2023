import streamlit as st
import pandas as pd

def display_metrics(df):
    """Mostrar métricas principales con validación"""
    
    # Validar que el DataFrame no esté vacío
    if df.empty:
        st.error("No hay datos disponibles para mostrar métricas")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total de Accidentes",
            value=f"{len(df):,}",
            delta=f"{len(df) - 100000:,}" if len(df) != 100000 else "Muestra completa"
        )
    
    with col2:
        # Manejar Severity como categorical o numérico
        try:
            if df['Severity'].dtype.name == 'category':
                avg_severity = df['Severity'].astype(int).mean()
            else:
                avg_severity = df['Severity'].mean()
            
            st.metric(
                label="⚠️ Severidad Promedio",
                value=f"{avg_severity:.2f}",
                delta=f"{avg_severity - 2:.2f}" if avg_severity != 2 else "Nivel medio"
            )
        except Exception as e:
            st.metric(
                label="⚠️ Severidad Promedio",
                value="Error",
                delta="No disponible"
            )
    
    with col3:
        st.metric(
            label="🗺️ Estados Afectados",
            value=df['State'].nunique(),
            delta=f"{df['State'].nunique() - 50} estados"
        )
    
    with col4:
        try:
            night_accidents = df[df['Sunrise_Sunset'] == 'Night'].shape[0]
            night_percentage = (night_accidents / len(df)) * 100
            st.metric(
                label="🌙 Accidentes Nocturnos",
                value=f"{night_percentage:.1f}%",
                delta=f"{night_accidents:,} accidentes"
            )
        except Exception as e:
            st.metric(
                label="🌙 Accidentes Nocturnos",
                value="Error",
                delta="No disponible"
            )
    
    # Información adicional
    with st.expander("📋 Detalles de las métricas"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📈 Distribución de Severidad:**")
            try:
                severity_counts = df['Severity'].value_counts().sort_index()
                for level, count in severity_counts.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"• Nivel {level}: {count:,} ({percentage:.1f}%)")
            except:
                st.write("Error al calcular distribución de severidad")
        
        with col2:
            st.markdown("**🏆 Top 5 Estados:**")
            try:
                top_states = df['State'].value_counts().head(5)
                for state, count in top_states.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"• {state}: {count:,} ({percentage:.1f}%)")
            except:
                st.write("Error al calcular top estados")