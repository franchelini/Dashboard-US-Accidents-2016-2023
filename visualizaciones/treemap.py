import plotly.express as px
from dash import dcc, html
import pandas as pd

def get_treemap(df_sample):
    infra_vars = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
                  'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
                  'Traffic_Signal', 'Turning_Loop']

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

    return html.Div(
        className="graph-container",
        children=[
            html.H2("Presencia de Infraestructura Vial en Accidentes", style={'textAlign': 'center', 'color': '#555'}),
            dcc.Graph(id='treemap-infra', figure=fig_treemap),
            html.P("Tamaño: Frecuencia de accidentes | Color: % de accidentes nocturnos",
                  style={'textAlign': 'center', 'color': '#777', 'fontStyle': 'italic', 'marginTop': '15px'})
        ],
        style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}
    )