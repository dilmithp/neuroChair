from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
import data_loader

# Tableau Colors
COLORS = {
    'blue': '#4e79a7', 'orange': '#f28e2c', 'red': '#e15759',
    'green': '#59a14f', 'teal': '#76b7b2', 'purple': '#b07aa1', 'gray': '#79706e'
}

LAYOUT = {
    'paper_bgcolor': 'white', 'plot_bgcolor': 'white',
    'font': {'family': 'Helvetica Neue, Arial', 'size': 11, 'color': '#555'},
    'margin': {'l': 40, 'r': 20, 't': 30, 'b': 30}
}

def render_end_user_tab():
    return dbc.Container([
        # Row 1: Key Metrics (4 KPIs)
        dbc.Row([
            dbc.Col([create_kpi_card("stress-kpi", "CURRENT STRESS")], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi_card("posture-kpi", "POSTURE SCORE")], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi_card("sitting-kpi", "SITTING TIME")], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi_card("breaks-kpi", "BREAKS TAKEN")], lg=3, md=6, className="mb-3"),
        ]),
        
        # Row 2: Main Charts
        dbc.Row([
            # Stress Gauge + Heart Rate
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("STRESS LEVEL"),
                    dbc.CardBody([dcc.Graph(id='stress-gauge', style={'height': '180px'}, config={'displayModeBar': False})])
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardHeader("HEART RATE VARIABILITY"),
                    dbc.CardBody([dcc.Graph(id='hrv-chart', style={'height': '140px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            
            # Weekly Trends
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("WEEKLY STRESS & POSTURE TRENDS"),
                    dbc.CardBody([dcc.Graph(id='weekly-chart', style={'height': '340px'}, config={'displayModeBar': False})])
                ])
            ], lg=8, className="mb-3"),
        ]),
        
        # Row 3: Activity & Alerts
        dbc.Row([
            # Today's Activity Timeline
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("TODAY'S ACTIVITY"),
                    dbc.CardBody([dcc.Graph(id='activity-timeline', style={'height': '160px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            
            # Posture Distribution
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("POSTURE DISTRIBUTION"),
                    dbc.CardBody([dcc.Graph(id='posture-pie', style={'height': '160px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            
            # GSR (Skin Conductance)
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("SKIN CONDUCTANCE (GSR)"),
                    dbc.CardBody([dcc.Graph(id='gsr-chart', style={'height': '160px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
        ]),
        
        # Row 4: Notifications & Goals
        dbc.Row([
            # Alerts
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        "NOTIFICATIONS",
                        dbc.Badge(id='alert-count', children="0", color="danger", className="ms-2")
                    ]),
                    dbc.CardBody([html.Div(id='notifications-list', style={'maxHeight': '200px', 'overflowY': 'auto'})])
                ])
            ], lg=4, className="mb-3"),
            
            # Daily Goals
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("DAILY GOALS PROGRESS"),
                    dbc.CardBody([html.Div(id='goals-progress')])
                ])
            ], lg=4, className="mb-3"),
            
            # Recommendations
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("SMART RECOMMENDATIONS"),
                    dbc.CardBody([html.Div(id='recommendations-list', style={'maxHeight': '200px', 'overflowY': 'auto'})])
                ])
            ], lg=4, className="mb-3"),
        ]),
    ], fluid=True)

def create_kpi_card(div_id, label):
    return dbc.Card([
        dbc.CardBody([
            html.Div(id=div_id, className="kpi-metric")
        ])
    ])

def register_end_user_callbacks(app):
    @app.callback(
        [Output('stress-kpi', 'children'), Output('posture-kpi', 'children'),
         Output('sitting-kpi', 'children'), Output('breaks-kpi', 'children'),
         Output('stress-gauge', 'figure'), Output('hrv-chart', 'figure'),
         Output('weekly-chart', 'figure'), Output('activity-timeline', 'figure'),
         Output('posture-pie', 'figure'), Output('gsr-chart', 'figure'),
         Output('notifications-list', 'children'), Output('goals-progress', 'children'),
         Output('recommendations-list', 'children'), Output('alert-count', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_dashboard(n):
        # Fetch actual data from Data Loader (U01)
        stats = data_loader.get_user_stats("U01")
        history = data_loader.get_recent_history("U01")
        
        stress = stats['stress_avg']
        posture = stats['posture_avg']
        sitting = stats['sitting_hours']
        breaks = stats['breaks']
        
        # KPIs With Data from CSV
        stress_kpi = create_kpi_content(f"{stress}/10", "CURRENT STRESS", 
                                        "danger" if stress > 7 else "warning" if stress > 4 else "success",
                                        "Avg from history")
        posture_kpi = create_kpi_content(f"{posture}%", "POSTURE SCORE",
                                         "success" if posture >= 80 else "warning" if posture >= 50 else "danger",
                                         "Based on usage")
        sitting_kpi = create_kpi_content(f"{sitting}h", "SITTING TIME",
                                         "warning" if sitting > 4 else "success",
                                         f"Today")
        breaks_kpi = create_kpi_content(str(breaks), "BREAKS TAKEN",
                                        "success" if breaks >= 4 else "warning",
                                        f"Target: 4+")
        
        # Charts using History Data
        stress_gauge = create_gauge(stress)
        hrv_fig = create_hrv_chart(history)
        weekly_fig = create_weekly_chart(history)
        activity_fig = create_activity_timeline()
        posture_pie = create_posture_pie(posture)
        gsr_fig = create_gsr_chart(history)
        
        # Notifications
        alerts = []
        alert_count = 0
        if stress > 6:
            alerts.append(create_alert("Elevated Stress", "Your historical pattern shows high stress", "warning"))
            alert_count += 1
        if posture < 60:
            alerts.append(create_alert("Poor Posture Trend", "Consider checking your back support", "warning"))
            alert_count += 1
        
        if not alerts:
            alerts.append(create_alert("Status Normal", "Your metrics are within healthy ranges", "success"))
        
        # Goals
        goals = create_goals_progress(stress, posture, sitting, breaks)
        
        # Recommendations
        recs = create_recommendations(stress, posture, sitting)
        
        return (stress_kpi, posture_kpi, sitting_kpi, breaks_kpi,
                stress_gauge, hrv_fig, weekly_fig, activity_fig, posture_pie, gsr_fig,
                alerts, goals, recs, str(alert_count))

def create_kpi_content(value, label, status, trend):
    color_map = {'success': COLORS['green'], 'warning': COLORS['orange'], 'danger': COLORS['red']}
    return html.Div([
        html.Div(value, style={'fontSize': '32px', 'fontWeight': '300', 'color': color_map.get(status, COLORS['blue'])}),
        html.Div(label, style={'fontSize': '10px', 'color': '#888', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
        html.Div(trend, style={'fontSize': '11px', 'color': '#999', 'marginTop': '4px'})
    ], className="text-center")

def create_gauge(value):
    color = COLORS['green'] if value <= 3 else COLORS['orange'] if value <= 6 else COLORS['red']
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        number={'font': {'size': 32, 'color': '#333'}},
        gauge={'axis': {'range': [0, 10], 'tickwidth': 1}, 'bar': {'color': color, 'thickness': 0.6}, 'bgcolor': '#f5f5f5',
               'steps': [{'range': [0, 3], 'color': 'rgba(89,161,79,0.15)'}, {'range': [3, 7], 'color': 'rgba(242,142,44,0.15)'}, {'range': [7, 10], 'color': 'rgba(225,87,89,0.15)'}]}
    ))
    fig.update_layout(**LAYOUT)
    return fig

def create_hrv_chart(data):
    fig = go.Figure()
    if data:
        times = [f"-{i*5}m" for i in range(len(data))]
        hrvs = [d.get('hrv', 70) for d in data]
        fig.add_trace(go.Scatter(x=times, y=hrvs, mode='lines+markers', line={'color': COLORS['teal'], 'width': 2}, marker={'size': 5}, fill='tozeroy', fillcolor='rgba(118,183,178,0.1)'))
    fig.update_layout(**LAYOUT, yaxis={'range': [50, 100], 'gridcolor': '#eee'}, xaxis={'gridcolor': '#eee'}, showlegend=False)
    return fig

def create_weekly_chart(history):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    stress = [4, 5, 6, 4, 7, 3, 5]
    posture = [75, 70, 65, 80, 60, 85, 72]
    
    if len(history) >= 7:
        mock_days = history[-7:]
        stress = [d['stress_level'] for d in mock_days]
        posture = [d['posture_score'] for d in mock_days]

    sitting = [5, 6, 7, 4, 8, 3, 5]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=days, y=posture, name='Posture %', marker_color=COLORS['blue'], opacity=0.7, yaxis='y2'))
    fig.add_trace(go.Scatter(x=days, y=stress, name='Stress', line={'color': COLORS['red'], 'width': 2}, mode='lines+markers', marker={'size': 6}))
    fig.add_trace(go.Scatter(x=days, y=sitting, name='Sitting (h)', line={'color': COLORS['orange'], 'width': 2, 'dash': 'dot'}, mode='lines+markers', marker={'size': 5}))
    
    fig.update_layout(**LAYOUT, showlegend=True, legend={'orientation': 'h', 'y': 1.15, 'x': 0, 'font': {'size': 10}},
                     yaxis={'title': 'Stress / Hours', 'range': [0, 10], 'gridcolor': '#eee'},
                     yaxis2={'title': 'Posture %', 'range': [0, 100], 'overlaying': 'y', 'side': 'right'},
                     xaxis={'gridcolor': '#eee'}, bargap=0.4)
    return fig

def create_activity_timeline():
    hours = list(range(9, 18))
    activity = [1, 2, 2, 3, 1, 2, 1, 2, 3]  # 1=sitting, 2=active, 3=break
    colors = [COLORS['orange'] if a == 1 else COLORS['green'] if a == 2 else COLORS['teal'] for a in activity]
    
    fig = go.Figure(go.Bar(x=[f"{h}:00" for h in hours], y=[1]*len(hours), marker_color=colors, showlegend=False))
    fig.update_layout(**LAYOUT, yaxis={'visible': False}, xaxis={'gridcolor': '#eee'}, bargap=0.1)
    return fig

def create_posture_pie(current_posture):
    good = current_posture
    poor = 100 - current_posture
    fig = go.Figure(go.Pie(values=[good, poor], labels=['Good', 'Poor'], 
                          marker={'colors': [COLORS['green'], COLORS['red']]}, hole=0.6,
                          textinfo='percent', textfont={'size': 10}))
    fig.update_layout(**LAYOUT, showlegend=True, legend={'font': {'size': 9}, 'orientation': 'h', 'y': -0.1})
    return fig

def create_gsr_chart(data):
    fig = go.Figure()
    if data:
        times = [f"-{i}m" for i in range(len(data))]
        gsrs = [d.get('gsr', 1.5) for d in data]
        fig.add_trace(go.Scatter(x=times, y=gsrs, mode='lines', line={'color': COLORS['purple'], 'width': 2}, fill='tozeroy', fillcolor='rgba(176,122,161,0.1)'))
    fig.update_layout(**LAYOUT, yaxis={'range': [0, 3], 'gridcolor': '#eee'}, xaxis={'gridcolor': '#eee'}, showlegend=False)
    return fig

def create_alert(title, desc, level):
    return html.Div([
        html.Div(title, className="alert-title"),
        html.Div(desc, className="alert-desc")
    ], className=f"alert-item {level}")

def create_goals_progress(stress, posture, sitting, breaks):
    goals = [
        {"name": "Stress below 5", "current": max(0, 10 - stress), "target": 5, "color": COLORS['red']},
        {"name": "Posture above 70%", "current": posture, "target": 70, "color": COLORS['blue']},
        {"name": "Sitting under 6h", "current": max(0, 6 - sitting), "target": 6, "color": COLORS['orange']},
        {"name": "Take 4+ breaks", "current": breaks, "target": 4, "color": COLORS['green']},
    ]
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span(g["name"], style={'fontSize': '11px', 'color': '#555'}),
                html.Span(f"{min(100, int((g['current']/g['target'])*100) if g['target'] > 0 else 0)}%", 
                         style={'fontSize': '11px', 'color': g['color'], 'float': 'right'})
            ]),
            dbc.Progress(value=min(100, (g['current']/g['target'])*100 if g['target'] > 0 else 0), color="primary" if g['current'] >= g['target'] else "secondary",
                        style={'height': '4px', 'marginTop': '4px', 'marginBottom': '12px'})
        ]) for g in goals
    ])

def create_recommendations(stress, posture, sitting):
    recs = []
    if stress > 5:
        recs.append({"title": "Practice deep breathing", "desc": "4-7-8 technique for 2 minutes"})
    if posture < 70:
        recs.append({"title": "Adjust monitor height", "desc": "Screen should be at eye level"})
    if sitting > 4:
        recs.append({"title": "Stand up and stretch", "desc": "Walk for 5 minutes"})
    recs.append({"title": "Stay hydrated", "desc": "Drink 8 glasses of water daily"})
    
    return html.Div([
        html.Div([
            html.Div(r["title"], style={'fontSize': '12px', 'fontWeight': '500', 'color': '#333'}),
            html.Div(r["desc"], style={'fontSize': '11px', 'color': '#888'})
        ], className="insight-item") for r in recs[:4]
    ])
