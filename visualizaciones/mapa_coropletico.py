import plotly.express as px
from dash import dcc, html

def get_mapa(df_sample):
    state_counts = df_sample['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Accident_Count']

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
        title_x=0.5,
        margin={"r":0,"t":40,"l":0,"b":0}
    )

    # Ejemplo dentro de visualizaciones/mapa_coropletico.py
    return html.Div(
        className="graph-container animate__animated animate__fadeInUp",
        children=[
            html.H2("Distribución Geográfica de Accidentes", style={'textAlign': 'center', 'color': '#43cea2'}),
            dcc.Graph(id='mapa-accidentes', figure=fig_map)
        ],
        style={'padding': '20px', 'background': 'rgba(255,255,255,0.95)', 'borderRadius': '15px', 'margin': '30px', 'boxShadow': '0 4px 24px rgba(24,90,157,0.2)'}
    )