import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# Cargar el dataset
# Se tomaron 100,000 muestras aleatorias del dataset original para optimiza, sino sería muy pesado. Pero asumo que más adelante se podría trabajar con el dataset completo.

try:
    df = pd.read_csv('US_Accidents_March23.csv')
    df_sample = df.sample(n=100000, random_state=42)
except FileNotFoundError:
    print("Error: Asegúrate de que el archivo 'US_Accidents_March23.csv' esté en la misma carpeta que app.py")
    exit()

# Convertir la columna de inicio a formato de fecha para futuros análisis
# Le decimos a Pandas que sea flexible con el formato de fecha y que ignore los errores
df_sample['Start_Time'] = pd.to_datetime(df_sample['Start_Time'], format='mixed', errors='coerce')



# VISUALIZACIÓN 1: MAPA COROPLÉTICO DE ACCIDENTES POR ESTADO
# Agrupamos los datos por estado y contamos el número de accidentes
state_counts = df_sample['State'].value_counts().reset_index()
state_counts.columns = ['State', 'Accident_Count']

# Creamos el mapa con Plotly Express
fig_map = px.choropleth(
    state_counts,
    locations='State',
    locationmode="USA-states",
    color='Accident_Count',
    color_continuous_scale="Viridis",
    scope="usa",
    title="Número de Accidentes por Estado (en la muestra)",
    hover_name='State',
    labels={'Accident_Count': 'Cantidad de Accidentes'}
)
fig_map.update_layout(
    title_x=0.5, # Centrar el título
    margin={"r":0,"t":40,"l":0,"b":0} # Ajustar márgenes
)


# VISUALIZACIÓN 2: GRÁFICO DE BARRAS DE CONDICIONES CLIMÁTICAS
# Contamos las 15 condiciones climáticas más comunes
weather_counts = df_sample['Weather_Condition'].value_counts().nlargest(15).reset_index()
weather_counts.columns = ['Weather_Condition', 'Count']

# Creamos el gráfico de barras
fig_bar_weather = px.bar(
    weather_counts,
    x='Count',
    y='Weather_Condition',
    orientation='h',
    title="Top 15 Condiciones Climáticas en Accidentes",
    labels={'Count': 'Cantidad de Accidentes', 'Weather_Condition': 'Condición Climática'},
    color='Count',
    color_continuous_scale=px.colors.sequential.Plasma
)
fig_bar_weather.update_layout(
    title_x=0.5, # Centrar el título
    yaxis={'categoryorder':'total ascending'} # Ordenar barras de menor a mayor
)


# Inicializar la Aplicación Dash ---
app = dash.Dash(__name__)

# Necesario para el despliegue en servicios como Render
server = app.server

#  Definir el Layout del Dashboard 
app.layout = html.Div(
    style={'backgroundColor': '#f0f0f0', 'fontFamily': 'sans-serif'}, # Estilo general
    children=[
        # Título principal del dashboard
        html.H1(
            "Dashboard de Análisis de Accidentes Viales en EE.UU.",
            style={'textAlign': 'center', 'color': '#333'}
        ),

        # Contenedor para el mapa
        html.Div(
            className="graph-container",
            children=[
                html.H2("Distribución Geográfica de Accidentes", style={'textAlign': 'center', 'color': '#555'}),
                dcc.Graph(
                    id='mapa-accidentes',
                    figure=fig_map # Aquí usamos la figura del mapa que creamos
                )
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        ),

        # Contenedor para el gráfico de barras
        html.Div(
            className="graph-container",
            children=[
                html.H2("Impacto del Clima en los Accidentes", style={'textAlign': 'center', 'color': '#555'}),
                dcc.Graph(
                    id='clima-barras',
                    figure=fig_bar_weather # Aquí usamos la figura de barras que creamos
                )
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        )
    ]
)

#  Ejecutar la Aplicación 
if __name__ == '__main__':
    # El modo debug te permite ver los cambios en vivo mientras desarrollas
    app.run(debug=True)