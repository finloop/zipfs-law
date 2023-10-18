import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx

from .parse import count_tokens, count_to_dataframe

def barchart(df: pd.DataFrame):
    if not set(("count", "token")).issubset(set(df.columns)):
        raise ValueError("df must have columns 'count' and 'token'")
    df = df.sort_values("count", ascending=False)
    # Disable control panel
    # https://plotly.com/python/configuration-options/
    fig = px.bar(df, x="token", y="count", log_y=True, title="Prawo Zipfa", labels={"token": "Słowo", "count": "Liczba wystąpień"})
    return fig


def generate_nx_graph(tokens: list[str]) -> nx.Graph:
    nodes = list(set(tokens))
    edges = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.set_node_attributes(G, pos, "pos")
    # Add text to nodes
    for node in G.nodes:
        G.nodes[node]["text"] = node
    return G


def network(tokens: list[str]):
    G: nx.Graph = generate_nx_graph(tokens)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        #hoverinfo="text",
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale="YlGnBu",
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="Liczba sąsiadów",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
        textposition="top center",
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_label =  G.nodes[adjacencies[0]]["text"]
        node_text.append(node_label)

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Graf zależności między słowami",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig


def histogram(tokens: list[str]):
    token_counts = count_tokens(tokens)
    df = count_to_dataframe(token_counts)
    fig = barchart(df)
    return fig
