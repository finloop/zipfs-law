import streamlit as st

from zipfs_law.graphs import histogram, network
from zipfs_law.parse import split, clean

config = {'displayModeBar': False}
st.set_page_config(layout="wide")

st.write("# Prawo Zipfa")

st.write("""
Prawo Zipfa, znane również jako rozkład Zipfa, to empiryczne prawo obserwowane w wielu dziedzinach, takich jak lingwistyka, ekonomia, bibliometria, i inne. Prawo to opisuje rozkład częstotliwości elementów w zbiorze, zazwyczaj w kontekście języka naturalnego lub innych zbiorów danych tekstowych. Nazwa pochodzi od amerykańskiego lingwisty George'a Zipfa, który je opisał w latach 30. XX wieku.

Główne założenie prawa Zipfa mówi, że jeśli posortujemy elementy zbioru według częstotliwości ich występowania, to **drugi najczęściej występujący element będzie występował około dwukrotnie rzadziej niż najczęściej występujący element, trzeci będzie występował około trzy razy rzadziej niż pierwszy, i tak dalej**. Innymi słowy, częstotliwość występowania elementów maleje w sposób odwrotnie proporcjonalny do ich pozycji w rankingu popularności.
""")

text = st.text_area("Tekst do przeanalizowania", "Prawo Zipfa mówi, że w tekście występującym najczęściej słowo występuje dwukrotnie częściej niż drugie najczęściej występujące słowo, trzykrotnie częściej niż trzecie najczęściej występujące słowo itd. W tym notebooku zobaczymy, czy prawo Zipfa faktycznie zachodzi dla różnych tekstów.")
tokens = split(clean(text))

cols = st.columns(2)

with cols[0]:
    barchart_fig = histogram(tokens)
    st.plotly_chart(barchart_fig,config=config, use_container_width=True)

with cols[1]:
    network_fig = network(tokens)
    st.plotly_chart(network_fig,config=config, use_container_width=True)
