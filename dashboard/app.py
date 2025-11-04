import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
mongo_client = MongoClient('mongodb://mongodb:27017/')
db = mongo_client['neurochair']

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('NeuroChair Dashboard'),
    dcc.Graph(id='stress-graph'),
    dcc.Interval(id='interval', interval=2000)  # Update every 2 seconds
])


@app.callback(
    Output('stress-graph', 'figure'),
    Input('interval', 'n_intervals')
)
def update_graph(n):
    # Fetch latest data
    data = list(db.sensor_data.find().sort('timestamp', -1).limit(50))

    if data:
        df = pd.DataFrame(data)

        figure = go.Figure()
        figure.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df.get('stress_level', []),
            mode='lines',
            name='Stress Level'
        ))

        figure.update_layout(title='Real-Time Stress Monitoring')
        return figure

    return go.Figure()


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
