import streamlit as st
import streamlit.components.v1 as components

from zipfs_law.graphs import histogram, network
from zipfs_law.parse import split, clean

config = {'displayModeBar': True}
st.set_page_config(layout="wide")

with st.sidebar:
    st.write("## O projekcie")
    st.write("Prawo Zipfa mówi, że w tekście występującym najczęściej słowo występuje dwukrotnie częściej niż drugie najczęściej występujące słowo, trzykrotnie częściej niż trzecie najczęściej występujące słowo itd. W tym notebooku zobaczymy, czy prawo Zipfa faktycznie zachodzi dla różnych tekstów.")
    st.write("## Kontrolki")
    prc = st.slider("Procent tekstu do analizy", 0, 100, 100, 1)
    prune_network = st.checkbox("Przytnij sieć powiązań", help="Przytnij sieć, przydatne dla długich tekstów")
    st.write("## Autorzy")
    st.write("Piotr Krawiec, Patryk Gronkiewicz")
    st.write("## Źródła")
    st.write("https://pl.wikipedia.org/wiki/Prawo_Zipfa")
    st.video("https://www.youtube.com/watch?v=fCn8zs912OE")


st.write("# Prawo Zipfa")

text = st.text_area("Tekst do przeanalizowania", "Prawo Zipfa mówi, że w tekście występującym najczęściej słowo występuje dwukrotnie częściej niż drugie najczęściej występujące słowo, trzykrotnie częściej niż trzecie najczęściej występujące słowo itd. W tym notebooku zobaczymy, czy prawo Zipfa faktycznie zachodzi dla różnych tekstów.", height=150)

tokens = split(clean(text[:int(len(text) * prc / 100)]))

cols = st.columns(2)

with cols[0]:
    st.write("##### Histogram częstości występowania wyrazów")
    barchart_fig = histogram(tokens)
    st.plotly_chart(barchart_fig,config=config, use_container_width=True)

with cols[1]:
    st.write("##### Sieć powiązań wyrazów")
    network_html = network(tokens, prune=prune_network)
    components.html(network_html, height=1200)
