import streamlit as st

from zipfs_law.parse import split, clean, count_tokens, histogram
from zipfs_law.graphs import plot_zipfs_law

config = {'displayModeBar': False}

text = """
If you have set up the virtual env that you want already, take care that it is activated when you run the install command. If you don't, poetry will try to create a new virtual env and use that, which is probably not what you want.
"""

text = clean(text)
tokens = split(text, words=True)
token_counts = count_tokens(tokens)
df = histogram(token_counts)
fig = plot_zipfs_law(df)

st.plotly_chart(fig,config=config)