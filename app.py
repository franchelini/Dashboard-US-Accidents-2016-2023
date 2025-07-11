import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

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

# VISUALIZACIÓN 3: BOXPLOT INTERACTIVO DE VARIABLES CLIMÁTICAS Y SEVERIDAD
df_clima = df_sample[['Severity', 'Temperature(F)', 'Humidity(%)', 'Visibility(mi)']].copy()
df_clima['Severity'] = df_clima['Severity'].astype('category') 

# VISUALIZACIÓN 4: TREE MAP DE INFRAESTRUCTURA VIAL Y ACCIDENTES  NOCTURNOS
infra_vars = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit', 
              'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 
              'Traffic_Signal', 'Turning_Loop']

# VISUALIZACIÓN 5: GRÁFICO DE BARRAS DE ACCIDENTES POR CIUDAD
city_counts = df_sample['City'].value_counts().nlargest(20).reset_index()
city_counts.columns = ['City', 'Accident_Count']

fig_bar_city = px.bar(
    city_counts,
    x='City',
    y='Accident_Count',
    title="Top 20 Ciudades con Más Accidentes",
    labels={'City': 'Ciudad', 'Accident_Count': 'Cantidad de Accidentes'},
    color='Accident_Count',
    color_continuous_scale=px.colors.sequential.Viridis
)
fig_bar_city.update_layout(
    title_x=0.5,
    xaxis_tickangle=-45
)

# VISUALIZACIÓN 6: GRÁFICO DE LÍNEAS DE ACCIDENTES POR MES
df_sample['YearMonth'] = df_sample['Start_Time'].dt.to_period('M').astype(str)
monthly_counts = df_sample['YearMonth'].value_counts().sort_index().reset_index()
monthly_counts.columns = ['YearMonth', 'Accident_Count']

fig_line_monthly = px.line(
    monthly_counts,
    x='YearMonth',
    y='Accident_Count',
    title='Tendencia Mensual de Accidentes',
    labels={'YearMonth': 'Mes', 'Accident_Count': 'Cantidad de Accidentes'},
    markers=True
)
fig_line_monthly.update_layout(
    title_x=0.5,
    xaxis_tickangle=-45,
    height=400,
    plot_bgcolor='white',
    margin={"r":30,"t":60,"l":30,"b":30}
)

# Calcular frecuencia y % nocturno para cada infraestructura
infra_data = []
for var in infra_vars:
    total = df_sample[var].sum()
    nocturnos = df_sample[(df_sample[var] == True) & (df_sample['Sunrise_Sunset'] == 'Night')].shape[0]
    porcentaje_nocturno = (nocturnos / total) * 100 if total > 0 else 0
    
    infra_data.append({
        'Infraestructura': var,
        'Count': total,
        'Porcentaje_Nocturno': porcentaje_nocturno
    })

infra_df = pd.DataFrame(infra_data).sort_values('Count', ascending=False)

# Crear treemap 
fig_treemap = px.treemap(
    infra_df,
    path=['Infraestructura'],
    values='Count',
    title='Infraestructura Vial: Frecuencia y % de Accidentes Nocturnos',
    color='Porcentaje_Nocturno',
    color_continuous_scale='Viridis',
    hover_data={
        'Count': True,
        'Porcentaje_Nocturno': ':.1f%'
    },
    labels={'Porcentaje_Nocturno': '% Nocturno'}
)

fig_treemap.update_layout(
    margin={"t":50,"l":0,"r":0,"b":0},
    height=500,
    coloraxis_colorbar={
        'title': ' % Accidentes Nocturnos',
    }
)

# Inicializar la Aplicación Dash
app = dash.Dash(__name__)
server = app.server

# Definir el Layout del Dashboard 
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
                dcc.Graph(id='mapa-accidentes', figure=fig_map)
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        ),
        # Contenedor para el gráfico de barras
        html.Div(
            className="graph-container",
            children=[
                html.H2("Condiciones Climáticas Más Frecuentes", style={'textAlign': 'center', 'color': '#555'}),
                dcc.Graph(id='clima-barras', figure=fig_bar_weather)
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        ),

        # Contenedor para el boxplot interactivo
        html.Div(
            className="graph-container",
            children=[
                html.H2("Relación entre Variables Climáticas y Severidad", style={'textAlign': 'center', 'color': '#555'}),
                
                # Selector de variable climática
                html.Div([
                    html.Label("Seleccione variable climática:", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='variable-selector',
                        options=[
                            {'label': 'Temperatura (°F)', 'value': 'Temperature(F)'},
                            {'label': 'Humedad (%)', 'value': 'Humidity(%)'},
                            {'label': 'Visibility (mi)', 'value': 'Visibility(mi)'}
                        ],
                        value='Temperature(F)',
                        clearable=False,
                        style={'width': '300px', 'marginBottom': '20px'}
                    )
                ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '15px'}),
                
                # Gráfico boxplot interactivo
                dcc.Graph(id='boxplot-clima'),
                
                # Explicación
                html.P("Cada caja muestra la distribución de la variable climática para cada nivel de severidad (1=menor, 4=mayor).",
                      style={'textAlign': 'center', 'color': '#777', 'fontStyle': 'italic', 'marginTop': '15px'})
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        ),

        # Contenedor para el treemap de infraestructura (ACTUALIZADO)
        html.Div(
            className="graph-container",
            children=[
                html.H2("Presencia de Infraestructura Vial en Accidentes", style={'textAlign': 'center', 'color': '#555'}),
                dcc.Graph(id='treemap-infra', figure=fig_treemap),
                html.P("Tamaño: Frecuencia de accidentes | Color: % de accidentes nocturnos",
                      style={'textAlign': 'center', 'color': '#777', 'fontStyle': 'italic', 'marginTop': '15px'})
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        ),
        # Contenedor para el gráfico de barras de ciudades
        html.Div(
            className="graph-container",
            children=[
                html.H2("Ciudades con Mayor Cantidad de Accidentes", style={'textAlign': 'center', 'color': '#555'}),
                dcc.Graph(id='city-bar', figure=fig_bar_city)
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        ),
        # Contenedor para la tendencia mensual de accidentes
        html.Div(
            className="graph-container",
            children=[
                html.H2("Tendencia Mensual de Accidentes", style={'textAlign': 'center', 'color': '#555'}),
                dcc.Graph(id='line-monthly', figure=fig_line_monthly)
            ],
            style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
        ),
    ]
)

# Callback para actualizar el boxplot según la selección
@app.callback(
    Output('boxplot-clima', 'figure'),
    Input('variable-selector', 'value')
)
def update_boxplot(selected_variable):
    # Configurar etiquetas según la variable seleccionada
    if selected_variable == 'Temperature(F)':
        y_label = "Temperatura (°F)"
        title = "Distribución de Temperaturas por Nivel de Severidad"
    elif selected_variable == 'Humidity(%)':
        y_label = "Humedad Relativa (%)"
        title = "Distribución de Humedad por Nivel de Severidad"
    else:
        y_label = "Visibility (mi)"
        title = "Distribución de Visibilidad por Nivel de Severidad"
    
    # Crear el boxplot
    fig = px.box(
        df_clima,
        x='Severity',
        y=selected_variable,
        color='Severity',
        title=title,
        labels={'Severity': 'Nivel de Severidad', selected_variable: y_label},
        category_orders={'Severity': ['1', '2', '3', '4']},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Nivel de Severidad (1=menor, 4=mayor)",
        yaxis_title=y_label,
        showlegend=False,
        plot_bgcolor='white',
        margin={"r":30,"t":60,"l":30,"b":30},
        height=500
    )
    
    return fig

# Ejecutar la Aplicación
if __name__ == '__main__':
    app.run(debug=True)