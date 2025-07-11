import plotly.express as px
from dash import dcc, html

def get_barras(df_sample):
    weather_counts = df_sample['Weather_Condition'].value_counts().nlargest(15).reset_index()
    weather_counts.columns = ['Weather_Condition', 'Count']

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
        title_x=0.5,
        yaxis={'categoryorder':'total ascending'}
    )

    return html.Div(
        className="graph-container",
        children=[
            html.H2("Condiciones Climáticas Más Frecuentes", style={'textAlign': 'center', 'color': '#555'}),
            dcc.Graph(id='clima-barras', figure=fig_bar_weather)
        ],
        style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
    )