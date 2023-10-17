import plotly.express as px
import pandas as pd

def plot_zipfs_law(df: pd.DataFrame):
    if not set(("count", "token")).issubset(set(df.columns)):
        raise ValueError("df must have columns 'count' and 'token'")
    df = df.sort_values("count", ascending=False)
    # Disable control panel
    # https://plotly.com/python/configuration-options/
    fig = px.bar(df, x="token", y="count", log_y=True, title="Prawo Zipfa")
    return fig
