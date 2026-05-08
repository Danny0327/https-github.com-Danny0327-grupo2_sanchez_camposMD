import os

import pandas as pd
import plotly.express as px
import streamlit as st

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

engine = create_engine(
    DATABASE_URL
)


st.set_page_config(
    page_title="NASA ETL Dashboard",
    layout="wide"
)


st.title("🚀 NASA ETL Dashboard")

st.markdown(
    "Visualización de datos APOD de NASA"
)


@st.cache_data
def load_data():

    query = """
        SELECT *
        FROM apod
        ORDER BY date DESC
    """

    df = pd.read_sql(
        query,
        engine
    )

    return df


df = load_data()


# =========================
# MÉTRICAS
# =========================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total registros",
        len(df)
    )
with col2:

    st.metric(
        "Primer fecha",
        str(df["date"].min())
    )

with col3:

    st.metric(
        "Última fecha",
        str(df["date"].max())
    )


st.divider()


# =========================
# TABLA
# =========================

st.subheader("📄 Datos APOD")

st.dataframe(
    df,
    use_container_width=True
)


# =========================
# FILTRO
# =========================

media_filter = st.selectbox(
    "Filtrar por media type",
    options=["Todos"] +
    list(df["media_type"].dropna().unique())
)

filtered_df = df

if media_filter != "Todos":

    filtered_df = df[
        df["media_type"] == media_filter
    ]


# =========================
# GRÁFICA
# =========================

st.subheader(
    "📊 Cantidad por tipo de media"
)

chart_data = (
    filtered_df["media_type"]
    .value_counts()
    .reset_index()
)

chart_data.columns = [
    "media_type",
    "cantidad"
]

fig = px.bar(
    chart_data,
    x="media_type",
    y="cantidad",
    title="Distribución de media types"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================
# VISUALIZACIÓN IMÁGENES
# =========================

st.subheader("🖼️ Imágenes NASA")

for _, row in filtered_df.iterrows():

    st.markdown(f"## {row['title']}")

    if row["media_type"] == "image":

        st.image(
            row["url"],
            use_container_width=True
        )

    st.write(
        row["explanation"]
    )

    st.divider()