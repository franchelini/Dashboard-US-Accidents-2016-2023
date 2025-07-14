import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ChartGenerator:
    def __init__(self, df):
        self.df = df
    
    def generate_mapa(self):
        """Generar mapa coroplético"""
        state_counts = self.df['State'].value_counts().reset_index()
        state_counts.columns = ['State', 'Accident_Count']
        
        fig = px.choropleth(
            state_counts,
            locations='State',
            locationmode="USA-states",
            color='Accident_Count',
            color_continuous_scale="Viridis",
            scope="usa",
            title="Distribución Geográfica de Accidentes",
            hover_name='State',
            labels={'Accident_Count': 'Cantidad de Accidentes'}
        )
        
        fig.update_layout(
            title_x=0.5,
            margin={"r":0,"t":40,"l":0,"b":0},
            height=500
        )
        
        return fig
    
    def generate_barras_clima(self):
        """Generar gráfico de barras de clima"""
        weather_counts = self.df['Weather_Condition'].value_counts().nlargest(15).reset_index()
        weather_counts.columns = ['Weather_Condition', 'Count']
        
        fig = px.bar(
            weather_counts,
            x='Count',
            y='Weather_Condition',
            orientation='h',
            title="Top 15 Condiciones Climáticas",
            labels={'Count': 'Cantidad de Accidentes', 'Weather_Condition': 'Condición Climática'},
            color='Count',
            color_continuous_scale=px.colors.sequential.Plasma
        )
        
        fig.update_layout(
            title_x=0.5,
            yaxis={'categoryorder':'total ascending'},
            height=500
        )
        
        return fig
    
    def generate_barras_ciudad(self):
        """Generar gráfico de barras de ciudades"""
        city_counts = self.df['City'].value_counts().nlargest(20).reset_index()
        city_counts.columns = ['City', 'Accident_Count']
        
        fig = px.bar(
            city_counts,
            x='City',
            y='Accident_Count',
            title="Top 20 Ciudades con Más Accidentes",
            labels={'City': 'Ciudad', 'Accident_Count': 'Cantidad de Accidentes'},
            color='Accident_Count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        fig.update_layout(
            title_x=0.5,
            xaxis_tickangle=-45,
            height=500
        )
        
        return fig
    
    def generate_boxplot(self, variable):
        """Generar boxplot para variable específica"""
        df_clima = self.df[['Severity', 'Temperature(F)', 'Humidity(%)', 'Visibility(mi)']].copy()
        
        titles = {
            'Temperature(F)': 'Distribución de Temperaturas por Severidad',
            'Humidity(%)': 'Distribución de Humedad por Severidad',
            'Visibility(mi)': 'Distribución de Visibilidad por Severidad'
        }
        
        labels = {
            'Temperature(F)': 'Temperatura (°F)',
            'Humidity(%)': 'Humedad (%)',
            'Visibility(mi)': 'Visibilidad (mi)'
        }
        
        fig = px.box(
            df_clima,
            x='Severity',
            y=variable,
            color='Severity',
            title=titles.get(variable, 'Boxplot'),
            labels={'Severity': 'Nivel de Severidad', variable: labels.get(variable, variable)},
            category_orders={'Severity': ['1', '2', '3', '4']},
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        
        fig.update_layout(
            title_x=0.5,
            xaxis_title="Nivel de Severidad",
            yaxis_title=labels.get(variable, variable),
            showlegend=False,
            height=500
        )
        
        return fig
    
    def generate_treemap(self):
        """Generar treemap de infraestructura"""
        infra_vars = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
                      'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
                      'Traffic_Signal', 'Turning_Loop']
        
        infra_data = []
        for var in infra_vars:
            if var in self.df.columns:
                total = self.df[var].sum()
                if total > 0:
                    nocturnos = self.df[(self.df[var] == True) & (self.df['Sunrise_Sunset'] == 'Night')].shape[0]
                    porcentaje_nocturno = (nocturnos / total) * 100
                    
                    infra_data.append({
                        'Infraestructura': var,
                        'Count': total,
                        'Porcentaje_Nocturno': porcentaje_nocturno
                    })
        
        if not infra_data:
            # Crear gráfico vacío si no hay datos
            fig = go.Figure()
            fig.update_layout(title="No hay datos disponibles para infraestructura")
            return fig
        
        infra_df = pd.DataFrame(infra_data).sort_values('Count', ascending=False)
        
        fig = px.treemap(
            infra_df,
            path=['Infraestructura'],
            values='Count',
            title='Infraestructura Vial: Frecuencia y % de Accidentes Nocturnos',
            color='Porcentaje_Nocturno',
            color_continuous_scale='Viridis',
            labels={'Porcentaje_Nocturno': '% Nocturno'}
        )
        
        fig.update_layout(
            margin={"t":50,"l":0,"r":0,"b":0},
            height=500
        )
        
        return fig
    
    def generate_lineas_mes(self):
        """Generar gráfico de líneas mensual"""
        monthly_counts = self.df['YearMonth'].value_counts().sort_index().reset_index()
        monthly_counts.columns = ['YearMonth', 'Accident_Count']
        
        fig = px.line(
            monthly_counts,
            x='YearMonth',
            y='Accident_Count',
            title='Tendencia Mensual de Accidentes',
            labels={'YearMonth': 'Mes', 'Accident_Count': 'Cantidad de Accidentes'},
            markers=True
        )
        
        fig.update_layout(
            title_x=0.5,
            xaxis_tickangle=-45,
            height=400
        )
        
        return fig