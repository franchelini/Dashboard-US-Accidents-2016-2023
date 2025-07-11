import plotly.express as px
from dash import dcc, html

def get_boxplot(df_sample):
    df_clima = df_sample[['Severity', 'Temperature(F)', 'Humidity(%)', 'Visibility(mi)']].copy()
    df_clima['Severity'] = df_clima['Severity'].astype('category')

    return html.Div(
        className="graph-container",
        children=[
            html.H2("Relación entre Variables Climáticas y Severidad", style={'textAlign': 'center', 'color': '#555'}),
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
            dcc.Graph(id='boxplot-clima'),
            html.P("Cada caja muestra la distribución de la variable climática para cada nivel de severidad (1=menor, 4=mayor).",
                  style={'textAlign': 'center', 'color': '#777', 'fontStyle': 'italic', 'marginTop': '15px'})
        ],
        style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
    )