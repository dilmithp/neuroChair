from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
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
                html.Small("Anonymized wellness metrics across organization", className="text-muted")
            ], lg=6),
            dbc.Col([
                dbc.Row([
                    dbc.Col([dcc.Dropdown(id='dept-filter', options=[
                        {'label': 'All Departments', 'value': 'all'},
                        {'label': 'Engineering', 'value': 'eng'},
                        {'label': 'Sales', 'value': 'sales'},
                        {'label': 'HR', 'value': 'hr'},
                    ], value='all', style={'fontSize': '12px'})], width=4),
                    dbc.Col([
                        dbc.ButtonGroup([
                            dbc.Button("7D", outline=True, color="secondary", size="sm", id="btn-7d"),
                            dbc.Button("30D", color="primary", size="sm", id="btn-30d"),
                            dbc.Button("90D", outline=True, color="secondary", size="sm", id="btn-90d"),
                        ])
                    ], width=4),
                    dbc.Col([dbc.Button("Download Report", size="sm", outline=True, color="secondary")], width=4)
                ])
            ], lg=6)
        ], className="mb-3 align-items-center"),
        
        # KPIs Row
        dbc.Row([
            dbc.Col([create_kpi('emp-wellness', 'WELLNESS SCORE')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_kpi('emp-stress', 'AVG STRESS')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_kpi('emp-posture', 'GOOD POSTURE')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_kpi('emp-sitting', 'AVG SITTING')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_kpi('emp-active', 'ACTIVE USERS')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_kpi('emp-alerts', 'ALERTS TODAY')], lg=2, md=4, className="mb-3"),
        ]),

        # Row 1: Main Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("ORGANIZATION STRESS INDEX"),
                    dbc.CardBody([dcc.Graph(id='org-gauge', style={'height': '200px'}, config={'displayModeBar': False})])
                ])
            ], lg=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("WELLNESS TREND (30 DAYS)"),
                    dbc.CardBody([dcc.Graph(id='wellness-trend', style={'height': '200px'}, config={'displayModeBar': False})])
                ])
            ], lg=5, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("DEPARTMENT COMPARISON"),
                    dbc.CardBody([dcc.Graph(id='dept-chart', style={'height': '200px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
        ]),

        # Row 2: Analysis Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("STRESS BY HOUR OF DAY"),
                    dbc.CardBody([dcc.Graph(id='hour-chart', style={'height': '180px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("SITTING TIME VS POSTURE"),
                    dbc.CardBody([dcc.Graph(id='scatter-chart', style={'height': '180px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("POSTURE DISTRIBUTION"),
                    dbc.CardBody([dcc.Graph(id='posture-dist', style={'height': '180px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
        ]),

        # Row 3: Insights & Rankings
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("DEPARTMENT RANKINGS"),
                    dbc.CardBody([html.Div(id='dept-rankings')])
                ])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("KEY INSIGHTS"),
                    dbc.CardBody([html.Div(id='key-insights')])
                ])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("ACTION ITEMS"),
                    dbc.CardBody([html.Div(id='action-items')])
                ])
            ], lg=4, className="mb-3"),
        ]),
    ], fluid=True)

def create_kpi(div_id, label):
    return dbc.Card([dbc.CardBody([html.Div(id=div_id)], className="py-2")])

def register_employer_callbacks(app):
    @app.callback(
        [Output('emp-wellness', 'children'), Output('emp-stress', 'children'),
         Output('emp-posture', 'children'), Output('emp-sitting', 'children'),
         Output('emp-active', 'children'), Output('emp-alerts', 'children'),
         Output('org-gauge', 'figure'), Output('wellness-trend', 'figure'),
         Output('dept-chart', 'figure'), Output('hour-chart', 'figure'),
         Output('scatter-chart', 'figure'), Output('posture-dist', 'figure'),
         Output('dept-rankings', 'children'), Output('key-insights', 'children'),
         Output('action-items', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update(n):
        # KPIs
        kpis = [
            create_kpi_content("78", "/100", "WELLNESS SCORE", "+5%", COLORS['blue']),
            create_kpi_content("5.2", "/10", "AVG STRESS", "-8%", COLORS['teal']),
            create_kpi_content("65", "%", "GOOD POSTURE", "+12%", COLORS['green']),
            create_kpi_content("5.8", "h", "AVG SITTING", "-0.5h", COLORS['orange']),
            create_kpi_content("54", "/60", "ACTIVE USERS", "", COLORS['purple']),
            create_kpi_content("3", "", "ALERTS TODAY", "-2", COLORS['red']),
        ]
        
        # Gauge
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=5.2, number={'suffix': '/10', 'font': {'size': 28}},
            gauge={'axis': {'range': [0, 10]}, 'bar': {'color': COLORS['orange'], 'thickness': 0.6}, 'bgcolor': '#f5f5f5',
                   'steps': [{'range': [0, 3], 'color': 'rgba(89,161,79,0.15)'}, {'range': [3, 7], 'color': 'rgba(242,142,44,0.15)'}, {'range': [7, 10], 'color': 'rgba(225,87,89,0.15)'}]}))
        gauge.update_layout(**LAYOUT)
        
        # Wellness Trend
        dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
        wellness = np.linspace(70, 78, 30) + np.random.normal(0, 2, 30)
        stress = np.linspace(6, 5.2, 30) + np.random.normal(0, 0.5, 30)
        
        trend = go.Figure()
        trend.add_trace(go.Scatter(x=dates, y=wellness, name='Wellness', fill='tozeroy', line={'color': COLORS['blue'], 'width': 2}, fillcolor='rgba(78,121,167,0.1)'))
        trend.add_trace(go.Scatter(x=dates, y=stress*10, name='Stress (x10)', line={'color': COLORS['red'], 'width': 2, 'dash': 'dot'}))
        trend.update_layout(**LAYOUT, showlegend=True, legend={'orientation': 'h', 'y': 1.15, 'font': {'size': 9}}, yaxis={'range': [0, 100], 'gridcolor': '#eee'}, xaxis={'gridcolor': '#eee'})
        
        # Department Chart
        depts = ['Engineering', 'Sales', 'HR', 'Marketing', 'Finance']
        scores = [72, 65, 85, 78, 70]
        dept_colors = [COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['teal'], COLORS['purple']]
        
        dept = go.Figure(go.Bar(x=depts, y=scores, marker_color=dept_colors, text=[f'{s}%' for s in scores], textposition='outside', textfont={'size': 10}))
        dept.add_hline(y=75, line_dash="dash", line_color=COLORS['green'], annotation_text="Goal", annotation_font_size=9)
        dept.update_layout(**LAYOUT, yaxis={'range': [0, 100], 'gridcolor': '#eee'})
        
        # Hour Chart
        hours = [f"{h}:00" for h in range(9, 18)]
        hour_stress = [3.2, 4.1, 5.2, 6.1, 5.8, 4.2, 3.5, 4.8, 5.9]
        colors = [COLORS['green'] if s < 4 else COLORS['orange'] if s < 6 else COLORS['red'] for s in hour_stress]
        hour = go.Figure(go.Bar(x=hours, y=hour_stress, marker_color=colors))
        hour.update_layout(**LAYOUT, yaxis={'range': [0, 8], 'gridcolor': '#eee'})
        
        # Scatter
        sitting = np.random.uniform(3, 8, 50)
        posture = 95 - sitting * 5 + np.random.normal(0, 8, 50)
        scatter = go.Figure(go.Scatter(x=sitting, y=posture, mode='markers',
            marker={'color': sitting, 'colorscale': [[0, COLORS['green']], [0.5, COLORS['orange']], [1, COLORS['red']]], 'size': 7}))
        scatter.update_layout(**LAYOUT, xaxis={'title': 'Sitting (hrs)', 'gridcolor': '#eee'}, yaxis={'title': 'Posture %', 'gridcolor': '#eee'})
        
        # Posture Distribution
        categories = ['Excellent', 'Good', 'Fair', 'Poor']
        values = [15, 35, 30, 20]
        dist_colors = [COLORS['green'], COLORS['blue'], COLORS['orange'], COLORS['red']]
        dist = go.Figure(go.Pie(values=values, labels=categories, marker={'colors': dist_colors}, hole=0.5, textinfo='percent', textfont={'size': 10}))
        dist.update_layout(**LAYOUT, showlegend=True, legend={'font': {'size': 9}})
        
        # Rankings
        rankings = html.Div([html.Table([
            html.Tbody([
                html.Tr([html.Td("1"), html.Td("HR"), html.Td("85%", style={'color': COLORS['green'], 'fontWeight': '600'}), html.Td("▲", style={'color': COLORS['green']})]),
                html.Tr([html.Td("2"), html.Td("Marketing"), html.Td("78%", style={'color': COLORS['blue']})]),
                html.Tr([html.Td("3"), html.Td("Engineering"), html.Td("72%", style={'color': COLORS['blue']})]),
                html.Tr([html.Td("4"), html.Td("Finance"), html.Td("70%", style={'color': COLORS['orange']})]),
                html.Tr([html.Td("5"), html.Td("Sales"), html.Td("65%", style={'color': COLORS['orange']}), html.Td("▼", style={'color': COLORS['red']})]),
            ])
        ], className="data-table")])
        
        # Insights
        insights = html.Div([
            html.Div("HR department exceeds wellness target", className="insight-item", style={'borderColor': COLORS['green']}),
            html.Div("Peak stress occurs at 12-1 PM", className="insight-item", style={'borderColor': COLORS['orange']}),
            html.Div("Sitting time correlates with poor posture", className="insight-item", style={'borderColor': COLORS['blue']}),
            html.Div("Overall wellness improved 12% this month", className="insight-item", style={'borderColor': COLORS['green']}),
        ])
        
        # Actions
        actions = html.Div([
            html.Div([html.Strong("High Priority"), html.Br(), "Ergonomic review for Sales team"], className="alert-item critical"),
            html.Div([html.Strong("Medium Priority"), html.Br(), "Implement lunch-time break reminders"], className="alert-item warning"),
            html.Div([html.Strong("Completed"), html.Br(), "Standing desk pilot program launched"], className="alert-item success"),
        ])
        
        return (*kpis, gauge, trend, dept, hour, scatter, dist, rankings, insights, actions)

def create_kpi_content(value, suffix, label, change, color):
    return html.Div([
        html.Div([html.Span(value, style={'fontSize': '24px', 'fontWeight': '300', 'color': color}),
                 html.Span(suffix, style={'fontSize': '12px', 'color': '#999'})], className="text-center"),
        html.Div(label, style={'fontSize': '9px', 'color': '#888', 'textTransform': 'uppercase', 'textAlign': 'center'}),
        html.Div(change, style={'fontSize': '10px', 'color': COLORS['green'] if change.startswith('+') or change.startswith('-') else '#999', 'textAlign': 'center'}) if change else None
    ])
