import plotly.express as px

def get_barras_ciudades(df_sample):
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
    return fig_bar_city
