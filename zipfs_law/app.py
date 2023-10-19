import streamlit as st
import streamlit.components.v1 as components

from zipfs_law.graphs import histogram, network
from zipfs_law.parse import split, clean

config = {'displayModeBar': True}
st.set_page_config(layout="wide")

st.write("# Prawo Zipfa")

text = st.text_area("Tekst do przeanalizowania", "Prawo Zipfa mówi, że w tekście występującym najczęściej słowo występuje dwukrotnie częściej niż drugie najczęściej występujące słowo, trzykrotnie częściej niż trzecie najczęściej występujące słowo itd. W tym notebooku zobaczymy, czy prawo Zipfa faktycznie zachodzi dla różnych tekstów.")
tokens = split(clean(text))

cols = st.columns(2)

with cols[0]:
    barchart_fig = histogram(tokens)
    st.plotly_chart(barchart_fig,config=config, use_container_width=True)

with cols[1]:
    network_html = network(tokens)
    components.html(network_html, height=1200)
