import plotly.express as px
from pyvis.network import Network
import pandas as pd
import networkx as nx
from collections import Counter
from .parse import count_tokens, count_to_dataframe
import math
import numpy as np

def barchart(df: pd.DataFrame):
    if not set(("count", "token")).issubset(set(df.columns)):
        raise ValueError("df must have columns 'count' and 'token'")
    df = df.sort_values("count", ascending=False)
    # Disable control panel
    # https://plotly.com/python/configuration-options/
    fig = px.bar(df, x="token", y="count", log_y=True, labels={"token": "Słowo", "count": "Liczba wystąpień"})
    return fig


def generate_nx_graph(tokens: list[str], prune=False) -> nx.Graph:
    nodes = list(set(tokens))
    edges = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]
    edge_counter = Counter(edges)
    print(edge_counter)
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    
    for edge in edge_counter:
        G.add_edge(edge[0], edge[1], weight=edge_counter[edge]*10)
        
    # Prune graph
    if prune:
        # Remove nodes with degree less than 3
        nodes_to_remove = [node for node in G.nodes if G.degree[node] < 3]
        G.remove_nodes_from(nodes_to_remove)

    
    # Add text to nodes
    for node in G.nodes:
        G.nodes[node]["text"] = node
        
    # Add size to nodes
    scale = 10
    d = dict(G.degree)
    d = {k: v * scale for k, v in d.items()}
    nx.set_node_attributes(G, d, "size")
    print(G.edges.data())
        
    return G


def network(tokens: list[str], prune: bool=False):
    G: nx.Graph = generate_nx_graph(tokens, prune=prune)
    
    nt = Network("450px", "100%")
    nt.from_nx(G)
    
    # Generate network with specific layout settings
    nt.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.70,
                        damping=0.35
                       )
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        nt.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        nt.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    return HtmlFile.read()


def histogram(tokens: list[str]):
    token_counts = count_tokens(tokens)
    df = count_to_dataframe(token_counts)
    fig = barchart(df)
    return fig, df

def histogram_log(df: pd.DataFrame):
    df["Liczba wystąpień [log]"] = df["Liczba wystąpień"].apply(math.log)
    df["index"] = np.log(df.index+1)
    fig = px.scatter(df, x="index", y="Liczba wystąpień [log]", labels={"index": "Ranga [log]", "Liczba wystąpień [log]": "Liczba wystąpień [log]"})
    return fig, df