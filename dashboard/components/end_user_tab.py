from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
from database import get_recent_sensor_data
import datetime

# Tableau Colors
COLORS = {
    'blue': '#4e79a7', 'orange': '#f28e2c', 'red': '#e15759',
    'green': '#59a14f', 'teal': '#76b7b2', 'gray': '#79706e'
}

LAYOUT = {
    'paper_bgcolor': 'white', 'plot_bgcolor': 'white',
    'font': {'family': 'Helvetica Neue, Arial', 'size': 11, 'color': '#555'},
    'margin': {'l': 40, 'r': 20, 't': 30, 'b': 30}
}

def render_end_user_tab():
    return dbc.Container([
        # KPI Row
        dbc.Row([
            dbc.Col([create_kpi_card("stress-value", "STRESS LEVEL", "stress-color")], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi_card("posture-value", "POSTURE SCORE", "posture-color")], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi_card("sitting-value", "SITTING TIME", "sitting-color")], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi_card("status-value", "STATUS", "status-color")], lg=3, md=6, className="mb-3"),
        ]),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("STRESS GAUGE"),
                    dbc.CardBody([dcc.Graph(id='stress-gauge', style={'height': '200px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("WEEKLY TRENDS"),
                    dbc.CardBody([dcc.Graph(id='weekly-chart', style={'height': '200px'}, config={'displayModeBar': False})])
                ])
            ], lg=8, className="mb-3"),
        ]),
        
        # Alerts & Tips
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("NOTIFICATIONS"),
                    dbc.CardBody([html.Div(id='notifications-list', style={'maxHeight': '180px', 'overflowY': 'auto'})])
                ])
            ], lg=6, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("RECOMMENDATIONS"),
                    dbc.CardBody([html.Div(id='recommendations-list', style={'maxHeight': '180px', 'overflowY': 'auto'})])
                ])
            ], lg=6, className="mb-3"),
        ])
    ], fluid=True)

def create_kpi_card(value_id, label, color_id):
    return dbc.Card([
        dbc.CardBody([
            html.Div(id=value_id, className="kpi-value"),
            html.Div(label, className="kpi-label"),
            html.Div(id=color_id, style={'display': 'none'})
        ], className="kpi-metric")
    ])

def register_end_user_callbacks(app):
    @app.callback(
        [Output('stress-value', 'children'), Output('stress-value', 'className'),
         Output('posture-value', 'children'), Output('posture-value', 'className'),
         Output('sitting-value', 'children'), Output('sitting-value', 'className'),
         Output('status-value', 'children'), Output('status-value', 'className'),
         Output('stress-gauge', 'figure'), Output('weekly-chart', 'figure'),
         Output('notifications-list', 'children'), Output('recommendations-list', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_dashboard(n):
        data = get_recent_sensor_data(limit=1)
        
        if not data:
            return ("--", "kpi-value", "--", "kpi-value", "--", "kpi-value", "--", "kpi-value",
                   create_gauge(0), create_weekly_chart([], [], []), [], [])
        
        d = data[0]
        stress = d.get('stress_level', 0)
        posture = d.get('posture_score', 0)
        sitting = 4.5
        
        # KPI values and colors
        stress_class = "kpi-value success" if stress <= 3 else "kpi-value warning" if stress <= 6 else "kpi-value danger"
        posture_class = "kpi-value success" if posture >= 80 else "kpi-value warning" if posture >= 50 else "kpi-value danger"
        sitting_class = "kpi-value success" if sitting < 4 else "kpi-value warning" if sitting < 6 else "kpi-value danger"
        status = "Good" if stress <= 5 and posture >= 60 else "Fair" if stress <= 7 else "Poor"
        status_class = "kpi-value success" if status == "Good" else "kpi-value warning" if status == "Fair" else "kpi-value danger"
        
        # Charts
        gauge = create_gauge(stress)
        dates = pd.date_range(end=datetime.datetime.now(), periods=7).strftime('%a').tolist()
        weekly = create_weekly_chart(dates, [3, 4, 5, 3, 6, 4, stress], [80, 75, 60, 85, 70, 80, posture])
        
        # Notifications
        notifs = []
        if stress > 7:
            notifs.append(create_alert("High stress detected", "Consider taking a break", "critical"))
        if posture < 50:
            notifs.append(create_alert("Poor posture", "Adjust your seating position", "warning"))
        if not notifs:
            notifs.append(create_alert("All metrics normal", "Keep up the good work", "success"))
        
        # Recommendations
        recs = [
            create_insight("Stand up and stretch every 30 minutes"),
            create_insight("Keep your monitor at eye level"),
            create_insight("Maintain proper lumbar support"),
        ]
        
        return (f"{stress}/10", stress_class, f"{posture}%", posture_class,
               f"{sitting}h", sitting_class, status, status_class,
               gauge, weekly, notifs, recs)

def create_gauge(value):
    color = COLORS['green'] if value <= 3 else COLORS['orange'] if value <= 6 else COLORS['red']
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'font': {'size': 36, 'color': '#333'}},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': '#ddd'},
            'bar': {'color': color, 'thickness': 0.6},
            'bgcolor': '#f0f0f0',
            'steps': [
                {'range': [0, 3], 'color': 'rgba(89,161,79,0.1)'},
                {'range': [3, 7], 'color': 'rgba(242,142,44,0.1)'},
                {'range': [7, 10], 'color': 'rgba(225,87,89,0.1)'}
            ]
        }
    ))
    fig.update_layout(**LAYOUT)
    return fig

def create_weekly_chart(dates, stress, posture):
    fig = go.Figure()
    if dates:
        fig.add_trace(go.Bar(x=dates, y=posture, name='Posture', marker_color=COLORS['blue'], opacity=0.7, yaxis='y2'))
        fig.add_trace(go.Scatter(x=dates, y=stress, name='Stress', line={'color': COLORS['red'], 'width': 2}, mode='lines+markers'))
    fig.update_layout(**LAYOUT, showlegend=True, legend={'orientation': 'h', 'y': 1.1, 'x': 0, 'font': {'size': 10}},
                     yaxis={'title': 'Stress', 'range': [0, 10], 'gridcolor': '#eee'},
                     yaxis2={'title': 'Posture', 'range': [0, 100], 'overlaying': 'y', 'side': 'right'},
                     xaxis={'gridcolor': '#eee'}, bargap=0.3)
    return fig

def create_alert(title, desc, level):
    return html.Div([
        html.Div(title, className="alert-title"),
        html.Div(desc, className="alert-desc")
    ], className=f"alert-item {level}")

def create_insight(text):
    return html.Div(text, className="insight-item")
