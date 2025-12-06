from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np

COLORS = {'blue': '#4e79a7', 'orange': '#f28e2c', 'red': '#e15759', 'green': '#59a14f', 'teal': '#76b7b2', 'purple': '#b07aa1'}
LAYOUT = {'paper_bgcolor': 'white', 'plot_bgcolor': 'white', 'font': {'family': 'Helvetica Neue', 'size': 11, 'color': '#555'}, 'margin': {'l': 40, 'r': 20, 't': 30, 'b': 30}}

def render_employer_tab():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H5("Workplace Analytics", style={'fontWeight': '600', 'color': '#333', 'marginBottom': '4px'}),
                html.Small("Anonymized aggregate wellness data", className="text-muted")
            ], lg=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("7D", outline=True, color="secondary", size="sm"),
                    dbc.Button("30D", color="primary", size="sm"),
                    dbc.Button("90D", outline=True, color="secondary", size="sm"),
                ], className="float-end")
            ], lg=4)
        ], className="mb-3 align-items-center"),
        
        # KPIs
        dbc.Row([
            dbc.Col([create_kpi("78", "Wellness Score", "/100", "+5%", "up", COLORS['blue'])], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi("5.2", "Avg Stress", "/10", "-8%", "up", COLORS['teal'])], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi("65", "Good Posture", "%", "+12%", "up", COLORS['green'])], lg=3, md=6, className="mb-3"),
            dbc.Col([create_kpi("54", "Active Users", "", "of 60", "neutral", COLORS['purple'])], lg=3, md=6, className="mb-3"),
        ]),

        # Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([dbc.CardHeader("ORG STRESS INDEX"), dbc.CardBody([dcc.Graph(id='org-gauge', style={'height': '180px'}, config={'displayModeBar': False})])])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([dbc.CardHeader("POSTURE TREND (30D)"), dbc.CardBody([dcc.Graph(id='trend-chart', style={'height': '180px'}, config={'displayModeBar': False})])])
            ], lg=8, className="mb-3"),
        ]),

        # Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([dbc.CardHeader("STRESS BY HOUR"), dbc.CardBody([dcc.Graph(id='hour-chart', style={'height': '200px'}, config={'displayModeBar': False})])])
            ], lg=6, className="mb-3"),
            dbc.Col([
                dbc.Card([dbc.CardHeader("SITTING VS POSTURE"), dbc.CardBody([dcc.Graph(id='scatter-chart', style={'height': '200px'}, config={'displayModeBar': False})])])
            ], lg=6, className="mb-3"),
        ]),

        # Row 3
        dbc.Row([
            dbc.Col([
                dbc.Card([dbc.CardHeader("DEPARTMENT COMPARISON"), dbc.CardBody([dcc.Graph(id='dept-chart', style={'height': '220px'}, config={'displayModeBar': False})])])
            ], lg=7, className="mb-3"),
            dbc.Col([
                dbc.Card([dbc.CardHeader("INSIGHTS"), dbc.CardBody([html.Div(id='insights')])])
            ], lg=5, className="mb-3"),
        ])
    ], fluid=True)

def create_kpi(value, label, suffix, change, direction, color):
    change_class = "kpi-change up" if direction == "up" else "kpi-change down" if direction == "down" else "kpi-change"
    arrow = "▲" if direction == "up" and change.startswith("+") else "▼" if direction == "up" and change.startswith("-") else ""
    return dbc.Card([
        dbc.CardBody([
            html.Div([html.Span(value, className="kpi-value", style={'color': color}), html.Span(suffix, style={'fontSize': '14px', 'color': '#999'})]),
            html.Div(label, className="kpi-label"),
            html.Div([arrow, " ", change], className=change_class) if change else None
        ], className="kpi-metric")
    ])

def register_employer_callbacks(app):
    @app.callback(
        [Output('org-gauge', 'figure'), Output('trend-chart', 'figure'),
         Output('hour-chart', 'figure'), Output('scatter-chart', 'figure'),
         Output('dept-chart', 'figure'), Output('insights', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update(n):
        # Gauge
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=5.2, number={'suffix': '/10', 'font': {'size': 32}},
            gauge={'axis': {'range': [0, 10]}, 'bar': {'color': COLORS['orange'], 'thickness': 0.6}, 'bgcolor': '#f0f0f0',
                   'steps': [{'range': [0, 3], 'color': 'rgba(89,161,79,0.1)'}, {'range': [3, 7], 'color': 'rgba(242,142,44,0.1)'}, {'range': [7, 10], 'color': 'rgba(225,87,89,0.1)'}]}))
        gauge.update_layout(**LAYOUT)
        
        # Trend
        dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
        vals = np.linspace(60, 75, 30) + np.random.normal(0, 3, 30)
        trend = go.Figure()
        trend.add_trace(go.Scatter(x=dates, y=vals, fill='tozeroy', line={'color': COLORS['blue'], 'width': 1.5}, fillcolor='rgba(78,121,167,0.1)'))
        trend.add_hline(y=70, line_dash="dash", line_color=COLORS['green'], annotation_text="Target", annotation_font_size=10)
        trend.update_layout(**LAYOUT, yaxis={'range': [40, 100], 'gridcolor': '#eee'}, xaxis={'gridcolor': '#eee'})
        
        # Hour
        hours = [f"{h}:00" for h in range(9, 18)]
        stress = [3.2, 4.1, 5.2, 6.1, 5.8, 4.2, 3.5, 4.8, 5.9]
        colors = [COLORS['green'] if s < 4 else COLORS['orange'] if s < 6 else COLORS['red'] for s in stress]
        hour = go.Figure(go.Bar(x=hours, y=stress, marker_color=colors))
        hour.update_layout(**LAYOUT, yaxis={'range': [0, 8], 'gridcolor': '#eee'})
        
        # Scatter
        sitting = np.random.uniform(2, 9, 40)
        posture = 100 - sitting * 5 + np.random.normal(0, 8, 40)
        scatter = go.Figure(go.Scatter(x=sitting, y=posture, mode='markers', 
            marker={'color': sitting, 'colorscale': [[0, COLORS['green']], [0.5, COLORS['orange']], [1, COLORS['red']]], 'size': 8}))
        scatter.update_layout(**LAYOUT, xaxis={'title': 'Sitting (hrs)', 'gridcolor': '#eee'}, yaxis={'title': 'Posture', 'gridcolor': '#eee'})
        
        # Dept
        depts = ['Engineering', 'Sales', 'HR', 'Marketing', 'Finance']
        scores = [72, 65, 85, 78, 70]
        dept_colors = [COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['teal'], COLORS['purple']]
        dept = go.Figure(go.Bar(x=depts, y=scores, marker_color=dept_colors, text=[f'{s}%' for s in scores], textposition='outside'))
        dept.add_hline(y=75, line_dash="dash", line_color=COLORS['green'], annotation_text="Goal", annotation_font_size=10)
        dept.update_layout(**LAYOUT, yaxis={'range': [0, 100], 'gridcolor': '#eee'})
        
        # Insights
        insights = html.Div([
            html.Div("HR leads in wellness metrics", className="insight-item", style={'borderColor': COLORS['green']}),
            html.Div("Sales team requires attention", className="insight-item", style={'borderColor': COLORS['orange']}),
            html.Div("+12% improvement this month", className="insight-item", style={'borderColor': COLORS['blue']}),
            html.Hr(style={'margin': '16px 0', 'borderColor': '#eee'}),
            html.Div("Recommendations", style={'fontWeight': '600', 'fontSize': '11px', 'color': '#888', 'textTransform': 'uppercase', 'marginBottom': '8px'}),
            html.Ul([
                html.Li("Ergonomic assessments for Sales"),
                html.Li("Company-wide break reminders"),
            ], style={'paddingLeft': '18px', 'fontSize': '12px', 'color': '#555', 'lineHeight': '1.8'})
        ])
        
        return gauge, trend, hour, scatter, dept, insights
