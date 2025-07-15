import plotly.express as px

def get_linea_tendencia_mensual(df_sample):
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
    return fig_line_monthly
