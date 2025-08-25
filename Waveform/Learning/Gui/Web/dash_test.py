import dash
from dash import html, dcc
import numpy as np
import plotly.graph_objs as go

app = dash.Dash(__name__)

bits = np.random.randint(0, 2, 100)
symbols = 2*bits - 1 + 0.1*np.random.randn(100)

fig = go.Figure(data=go.Scatter(x=np.real(symbols), y=np.imag(symbols), mode='markers'))

app.layout = html.Div([
    html.H1("BPSK Constellation"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)