import pandas as pd
import dash
from dash import dcc, html
from visualizaciones.mapa_coropletico import get_mapa
from visualizaciones.grafico_de_barras_condiciones_climaticas import get_barras
from visualizaciones.boxplot import get_boxplot
from visualizaciones.treemap import get_treemap


external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap",
    "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Cargar el dataset con datos aleatorios de accidentes viales en EE.UU. solo son 100,000 filas, sino PC hace PUM.
try:
    df = pd.read_csv('US_Accidents_March23.csv')
    df_sample = df.sample(n=100000, random_state=42)
except FileNotFoundError:
    print("Error: Asegúrate de que el archivo 'US_Accidents_March23.csv' esté en la misma carpeta que app.py")
    exit()

app = dash.Dash(__name__)
server = app.server


# ...importaciones y carga de datos...

# ...importaciones y carga de datos...

app.layout = html.Div(
    style={
        'background': 'linear-gradient(135deg, #43cea2 0%, #185a9d 100%)',
        'fontFamily': 'Montserrat, sans-serif',
        'minHeight': '100vh',
        'padding': '20px',
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',
        'gridTemplateRows': '100px 1fr 1fr',
        'gap': '20px'
        # Elimina 'height' y 'overflow'
    },
    children=[
        html.Div(
            html.H1(
                "Dashboard de Accidentes Viales en EE.UU.",
                className="animate__animated animate__fadeInDown",
                style={'textAlign': 'center', 'color': '#fff', 'margin': '0', 'textShadow': '2px 2px 8px #185a9d'}
            ),
            style={'gridColumn': '1 / span 2', 'gridRow': '1', 'background': 'none'}
        ),
        html.Div(get_mapa(df_sample), style={
            'gridColumn': '1', 'gridRow': '2',
            'background': 'rgba(255,255,255,0.95)', 'borderRadius': '15px',
            'minHeight': '350px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
        }),
        html.Div(get_barras(df_sample), style={
            'gridColumn': '2', 'gridRow': '2',
            'background': 'rgba(255,255,255,0.95)', 'borderRadius': '15px',
            'minHeight': '350px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
        }),
        html.Div(get_boxplot(df_sample), style={
            'gridColumn': '1', 'gridRow': '3',
            'background': 'rgba(255,255,255,0.95)', 'borderRadius': '15px',
            'minHeight': '350px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
        }),
        html.Div(get_treemap(df_sample), style={
            'gridColumn': '2', 'gridRow': '3',
            'background': 'rgba(255,255,255,0.95)', 'borderRadius': '15px',
            'minHeight': '350px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
        }),
    ]
)

# Callback para el boxplot interactivo
from dash import Input, Output
import plotly.express as px

@app.callback(
    Output('boxplot-clima', 'figure'),
    Input('variable-selector', 'value')
)
def update_boxplot(selected_variable):
    df_clima = df_sample[['Severity', 'Temperature(F)', 'Humidity(%)', 'Visibility(mi)']].copy()
    df_clima['Severity'] = df_clima['Severity'].astype('category')

    if selected_variable == 'Temperature(F)':
        y_label = "Temperatura (°F)"
        title = "Distribución de Temperaturas por Nivel de Severidad"
    elif selected_variable == 'Humidity(%)':
        y_label = "Humedad Relativa (%)"
        title = "Distribución de Humedad por Nivel de Severidad"
    else:
        y_label = "Visibility (mi)"
        title = "Distribución de Visibilidad por Nivel de Severidad"

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

if __name__ == '__main__':
    app.run(debug=True)