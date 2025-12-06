from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import datetime
import numpy as np

COLORS = {'blue': '#4e79a7', 'orange': '#f28e2c', 'red': '#e15759', 'green': '#59a14f', 'teal': '#76b7b2', 'purple': '#b07aa1'}
LAYOUT = {'paper_bgcolor': 'white', 'plot_bgcolor': 'white', 'font': {'family': 'Helvetica Neue', 'size': 11, 'color': '#555'}, 'margin': {'l': 40, 'r': 20, 't': 30, 'b': 30}}

def render_therapist_tab():
    return dbc.Container([
        # Header Row
        dbc.Row([
            dbc.Col([
                html.H5("Clinical Analysis", style={'fontWeight': '600', 'color': '#333', 'marginBottom': '4px'}),
                html.Small("Patient monitoring and treatment planning", className="text-muted")
            ], lg=5),
            dbc.Col([
                dbc.Row([
                    dbc.Col([dcc.Dropdown(id='patient-selector', options=[
                        {'label': 'John Doe (ID: 123)', 'value': '123'},
                        {'label': 'Jane Smith (ID: 456)', 'value': '456'},
                        {'label': 'Mike Wilson (ID: 789)', 'value': '789'},
                    ], value='123', style={'fontSize': '12px'})], width=5),
                    dbc.Col([dcc.DatePickerRange(id='date-range', start_date=datetime.date.today() - datetime.timedelta(days=30),
                                                 end_date=datetime.date.today(), style={'fontSize': '11px'})], width=5),
                    dbc.Col([dbc.Button("Export", size="sm", outline=True, color="secondary")], width=2)
                ])
            ], lg=7)
        ], className="mb-3 align-items-center"),

        # Patient Summary Row
        dbc.Row([
            dbc.Col([create_summary_card('patient-stress-avg', 'AVG STRESS', COLORS['red'])], lg=2, md=4, className="mb-3"),
            dbc.Col([create_summary_card('patient-posture-avg', 'AVG POSTURE', COLORS['blue'])], lg=2, md=4, className="mb-3"),
            dbc.Col([create_summary_card('patient-sessions', 'SESSIONS', COLORS['teal'])], lg=2, md=4, className="mb-3"),
            dbc.Col([create_summary_card('patient-improvement', 'IMPROVEMENT', COLORS['green'])], lg=2, md=4, className="mb-3"),
            dbc.Col([create_summary_card('patient-compliance', 'COMPLIANCE', COLORS['purple'])], lg=2, md=4, className="mb-3"),
            dbc.Col([create_summary_card('patient-risk', 'RISK LEVEL', COLORS['orange'])], lg=2, md=4, className="mb-3"),
        ]),

        # Main Charts Row
        dbc.Row([
            # Left Column - Timeline
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("SESSION HISTORY"),
                    dbc.CardBody([html.Div(id='session-list', style={'height': '400px', 'overflowY': 'auto'})])
                ])
            ], lg=3, className="mb-3"),
            
            # Center Column - Charts
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("STRESS TREND (30 DAYS)"),
                            dbc.CardBody([dcc.Graph(id='stress-trend', style={'height': '150px'}, config={'displayModeBar': False})])
                        ])
                    ], lg=6, className="mb-3"),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("POSTURE TREND (30 DAYS)"),
                            dbc.CardBody([dcc.Graph(id='posture-trend', style={'height': '150px'}, config={'displayModeBar': False})])
                        ])
                    ], lg=6, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("PRESSURE HEATMAP"),
                            dbc.CardBody([dcc.Graph(id='heatmap', style={'height': '160px'}, config={'displayModeBar': False})])
                        ])
                    ], lg=6, className="mb-3"),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("STRESS BY HOUR"),
                            dbc.CardBody([dcc.Graph(id='stress-hour', style={'height': '160px'}, config={'displayModeBar': False})])
                        ])
                    ], lg=6, className="mb-3"),
                ])
            ], lg=6),
            
            # Right Column - Details
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("ABNORMAL EVENTS"),
                    dbc.CardBody([html.Div(id='events-table', style={'height': '160px', 'overflowY': 'auto'})])
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardHeader("TREATMENT RECOMMENDATIONS"),
                    dbc.CardBody([html.Div(id='treatment-plan')])
                ])
            ], lg=3, className="mb-3")
        ])
    ], fluid=True)

def create_summary_card(div_id, label, color):
    return dbc.Card([
        dbc.CardBody([
            html.Div(id=div_id, style={'fontSize': '24px', 'fontWeight': '300', 'color': color}),
            html.Div(label, style={'fontSize': '9px', 'color': '#888', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'})
        ], className="text-center py-2")
    ])

def register_therapist_callbacks(app):
    @app.callback(
        [Output('patient-stress-avg', 'children'), Output('patient-posture-avg', 'children'),
         Output('patient-sessions', 'children'), Output('patient-improvement', 'children'),
         Output('patient-compliance', 'children'), Output('patient-risk', 'children'),
         Output('session-list', 'children'), Output('stress-trend', 'figure'),
         Output('posture-trend', 'figure'), Output('heatmap', 'figure'),
         Output('stress-hour', 'figure'), Output('events-table', 'children'),
         Output('treatment-plan', 'children')],
        [Input('patient-selector', 'value'), Input('interval-component', 'n_intervals')]
    )
    def update(patient, n):
        # Summary metrics
        stress_avg, posture_avg, sessions = "5.2", "68%", "12"
        improvement, compliance, risk = "+15%", "82%", "Medium"
        
        # Sessions
        sessions_list = [html.Div([
            html.Div(f"Session {12-i}", className="timeline-title"),
            html.Div(f"{(datetime.datetime.now() - datetime.timedelta(days=i*2)).strftime('%b %d')} • {np.random.randint(1,4)}h {np.random.randint(0,59)}m", className="timeline-meta"),
            html.Div([
                html.Span(f"Stress: {np.random.randint(3,8)}", style={'fontSize': '10px', 'color': COLORS['red'], 'marginRight': '10px'}),
                html.Span(f"Posture: {np.random.randint(50,90)}%", style={'fontSize': '10px', 'color': COLORS['blue']})
            ])
        ], className=f"timeline-item{' active' if i==0 else ''}") for i in range(12)]
        
        # Stress Trend
        dates = pd.date_range(end=datetime.datetime.now(), periods=30)
        vals = np.random.uniform(3, 7, 30); vals[5], vals[15], vals[22] = 9, 8.5, 8
        stress_fig = go.Figure()
        stress_fig.add_trace(go.Scatter(x=dates, y=vals, fill='tozeroy', line={'color': COLORS['red'], 'width': 1.5}, fillcolor='rgba(225,87,89,0.1)'))
        stress_fig.add_hline(y=7, line_dash="dash", line_color=COLORS['red'], annotation_text="Threshold", annotation_font_size=9)
        stress_fig.update_layout(**LAYOUT, yaxis={'range': [0, 10], 'gridcolor': '#eee'}, xaxis={'gridcolor': '#eee'})
        
        # Posture Trend
        posture_vals = np.linspace(55, 75, 30) + np.random.normal(0, 5, 30)
        posture_fig = go.Figure()
        posture_fig.add_trace(go.Scatter(x=dates, y=posture_vals, fill='tozeroy', line={'color': COLORS['blue'], 'width': 1.5}, fillcolor='rgba(78,121,167,0.1)'))
        posture_fig.add_hline(y=70, line_dash="dash", line_color=COLORS['green'], annotation_text="Target", annotation_font_size=9)
        posture_fig.update_layout(**LAYOUT, yaxis={'range': [40, 100], 'gridcolor': '#eee'}, xaxis={'gridcolor': '#eee'})
        
        # Heatmap
        heat = np.random.rand(6, 6) * 0.4 + 0.2; heat[3:5, 3:5] += 0.4
        heatmap_fig = go.Figure(go.Heatmap(z=heat, colorscale=[[0, '#f0f7ff'], [0.5, COLORS['orange']], [1, COLORS['red']]], showscale=False))
        heatmap_fig.update_layout(**LAYOUT, xaxis={'showticklabels': False}, yaxis={'showticklabels': False})
        
        # Stress by Hour
        hours = [f"{h}:00" for h in range(9, 18)]
        hour_stress = [3.5, 4.2, 5.8, 6.5, 5.2, 4.0, 3.8, 5.5, 6.2]
        colors = [COLORS['green'] if s < 4 else COLORS['orange'] if s < 6 else COLORS['red'] for s in hour_stress]
        hour_fig = go.Figure(go.Bar(x=hours, y=hour_stress, marker_color=colors))
        hour_fig.update_layout(**LAYOUT, yaxis={'range': [0, 8], 'gridcolor': '#eee'})
        
        # Events
        events = html.Div([html.Table([
            html.Thead([html.Tr([html.Th("Date"), html.Th("Event"), html.Th("Duration"), html.Th("")])]),
            html.Tbody([
                html.Tr([html.Td("Dec 04"), html.Td("High Stress"), html.Td("45m"), html.Td(html.Span("Critical", className="status-pill critical"))]),
                html.Tr([html.Td("Dec 02"), html.Td("Long Sitting"), html.Td("5h"), html.Td(html.Span("Warning", className="status-pill warning"))]),
                html.Tr([html.Td("Nov 28"), html.Td("Poor Posture"), html.Td("2h"), html.Td(html.Span("Warning", className="status-pill warning"))]),
            ])
        ], className="data-table")])
        
        # Treatment
        plan = html.Div([
            html.Div([html.Span("Priority:", style={'color': '#888'}), html.Span(" Stress Management", style={'fontWeight': '600', 'color': COLORS['red']})], style={'marginBottom': '12px'}),
            html.Div("Recommended Actions:", style={'fontSize': '11px', 'color': '#888', 'marginBottom': '8px', 'textTransform': 'uppercase'}),
            html.Ul([
                html.Li("Daily mindfulness exercises (15 min)"),
                html.Li("Ergonomic workspace review"),
                html.Li("Hourly break reminders"),
                html.Li("Follow-up in 2 weeks")
            ], style={'paddingLeft': '16px', 'fontSize': '12px', 'color': '#555', 'lineHeight': '1.8'})
        ])
        
        return (stress_avg, posture_avg, sessions, improvement, compliance, risk,
                sessions_list, stress_fig, posture_fig, heatmap_fig, hour_fig, events, plan)
