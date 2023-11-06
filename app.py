import streamlit as st
import streamlit.components.v1 as components

from zipfs_law.graphs import histogram, network, histogram_log
from zipfs_law.parse import split, clean

config = {'displayModeBar': True}
st.set_page_config(layout="wide")

with st.sidebar:
    st.write("## O projekcie")
    st.write("""
Prawo Zipfa mówi, że w tekście występującym najczęściej słowo występuje dwukrotnie 
częściej niż drugie najczęściej występujące słowo, trzykrotnie częściej niż trzecie 
najczęściej występujące słowo itd. Zadaniem tej aplikacji jest sprawdzenie, czy prawo
Zipfa faktycznie zachodzi dla różnych tekstów.

Aby rozpocząć analizę, wpisz tekst w polu po prawej stronie i wciśnij przycisk "Ctrl + Enter".
""")
    st.write("## Kontrolki")
    prc = st.slider("Procent tekstu do analizy", 0, 100, 100, 1)
    prune_network = st.checkbox("Przytnij sieć powiązań", help="Przytnij sieć, przydatne dla długich tekstów")
    st.write("## Autorzy")
    st.write("Piotr Krawiec, Patryk Gronkiewicz")
    st.write("## Źródła")
    st.write("https://pl.wikipedia.org/wiki/Prawo_Zipfa")
    st.video("https://www.youtube.com/watch?v=fCn8zs912OE")


st.write("# Prawo Zipfa")

text = st.text_area("Wpisz do przeanalizowania", "Prawo Zipfa mówi, że w tekście występującym najczęściej słowo występuje dwukrotnie częściej niż drugie najczęściej występujące słowo, trzykrotnie częściej niż trzecie najczęściej występujące słowo itd. W tym notebooku zobaczymy, czy prawo Zipfa faktycznie zachodzi dla różnych tekstów.", height=150)

st.write("lub wybierz jeden z poniższej listy")

select_result = st.selectbox("Tekst do analizy", ["","Pan Tadeusz", "Latarnik", "Model małpy uderzającej w klawiaturę"])

if select_result != "":
    if select_result == "Pan Tadeusz":
        with open("pan-tadeusz.txt", "r", encoding="utf-8") as f:
            text = f.read()
    if select_result == "Latarnik":
        with open("latarnik.txt", "r", encoding="utf-8") as f:
            text = f.read()
    if select_result == "Model małpy uderzającej w klawiaturę":
        with open("model-malpy.txt", "r", encoding="utf-8") as f:
            text = f.read()

tokens = split(clean(text[:int(len(text) * prc / 100)]))

cols = st.columns(2)

with cols[0]:
    st.write("##### Histogram częstości występowania wyrazów")
    barchart_fig, df = histogram(tokens)
    st.plotly_chart(barchart_fig,config=config, use_container_width=True)
    
    st.write("##### Tabela częstości występowania wyrazów")
    df.columns = ("Wyraz", "Liczba wystąpień")
    st.dataframe(df, use_container_width=True)
    

with cols[1]:
    st.write("##### Histogram częstości występowania wyrazów (log)")
    fig, df_log = histogram_log(df)
    st.plotly_chart(fig, config=config, use_container_width=True)
    
    st.write("##### Sieć powiązań wyrazów")
    if len(text) > 10_000:
        st.warning("Tekst jest długi, generowanie sieci może potrwać kilka minut")
    if st.button("Wygeneruj sieć", help="Może potrwać kilka minut"):

        network_html = network(tokens, prune=prune_network)
        components.html(network_html, height=1200)

st.write("## Inne miejsca, gdzie prawo Zipfa może zachodzić")
st.write("### Teksty w języku angielskim")
st.image("zipfs-law-eng.png", width=1000)

st.image("zipfs-law-unix.png", width=1000)
st.write("*Źródło: https://home.ipipan.waw.pl/l.debowski/docs/seminaria/zipf3.pdf*")