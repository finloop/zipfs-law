import streamlit as st

from zipfs_law.graphs import histogram, network
from zipfs_law.parse import split, clean

config = {'displayModeBar': False}
st.set_page_config(layout="wide")

text = st.text_area("Tekst do przeanalizowania", "Wpisz tekst do analizy")
tokens = split(clean(text))

cols = st.columns(2)

with cols[0]:
    barchart_fig = histogram(tokens)
    st.plotly_chart(barchart_fig,config=config, use_container_width=True)

with cols[1]:
    network_fig = network(tokens)
    st.plotly_chart(network_fig,config=config, use_container_width=True)
