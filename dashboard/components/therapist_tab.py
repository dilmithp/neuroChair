from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import datetime
import numpy as np

COLORS = {'blue': '#4e79a7', 'orange': '#f28e2c', 'red': '#e15759', 'green': '#59a14f', 'teal': '#76b7b2'}
LAYOUT = {'paper_bgcolor': 'white', 'plot_bgcolor': 'white', 'font': {'family': 'Helvetica Neue', 'size': 11, 'color': '#555'}, 'margin': {'l': 40, 'r': 20, 't': 30, 'b': 30}}

def render_therapist_tab():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H5("Patient Analysis", style={'fontWeight': '600', 'color': '#333', 'marginBottom': '4px'}),
                html.Small("Clinical insights and treatment planning", className="text-muted")
            ], width=6),
            dbc.Col([
                dbc.Row([
                    dbc.Col([dcc.Dropdown(id='patient-selector', options=[
                        {'label': 'John Doe (123)', 'value': '123'},
                        {'label': 'Jane Smith (456)', 'value': '456'},
                    ], value='123', style={'fontSize': '13px'})], width=8),
                    dbc.Col([dbc.Button("Export PDF", id="btn-export", size="sm", outline=True, color="secondary")], width=4)
                ])
            ], width=6)
        ], className="mb-3 align-items-center"),

        dbc.Row([
            # Timeline
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("SESSION HISTORY"),
                    dbc.CardBody([html.Div(id='session-list', style={'height': '480px', 'overflowY': 'auto'})])
                ])
            ], lg=3, className="mb-3"),
            
            # Main
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("STRESS ANALYSIS (30 DAYS)"),
                    dbc.CardBody([dcc.Graph(id='stress-chart', style={'height': '160px'}, config={'displayModeBar': False})])
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardHeader("PRESSURE DISTRIBUTION"),
                    dbc.CardBody([dcc.Graph(id='heatmap', style={'height': '180px'}, config={'displayModeBar': False})])
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("ABNORMAL EVENTS"),
                            dbc.CardBody([html.Div(id='events-table')])
                        ])
                    ], lg=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("TREATMENT PLAN"),
                            dbc.CardBody([html.Div(id='treatment-plan')])
                        ])
                    ], lg=6)
                ])
            ], lg=9)
        ])
    ], fluid=True)

def register_therapist_callbacks(app):
    @app.callback(
        [Output('session-list', 'children'), Output('stress-chart', 'figure'),
         Output('heatmap', 'figure'), Output('events-table', 'children'), Output('treatment-plan', 'children')],
        [Input('patient-selector', 'value'), Input('interval-component', 'n_intervals')]
    )
    def update(patient, n):
        # Sessions
        sessions = [html.Div([
            html.Div(f"Session {8-i}", className="timeline-title"),
            html.Div(f"{(datetime.datetime.now() - datetime.timedelta(days=i*2)).strftime('%b %d')} • 2h 15m", className="timeline-meta")
        ], className=f"timeline-item{' active' if i==0 else ''}") for i in range(8)]
        
        # Stress Chart
        dates = pd.date_range(end=datetime.datetime.now(), periods=30)
        vals = np.random.uniform(2, 7, 30); vals[5], vals[15] = 9, 8.5
        stress_fig = go.Figure()
        stress_fig.add_trace(go.Scatter(x=dates, y=vals, fill='tozeroy', line={'color': COLORS['blue'], 'width': 1.5}, fillcolor='rgba(78,121,167,0.1)'))
        stress_fig.add_hline(y=7, line_dash="dash", line_color=COLORS['red'], annotation_text="Threshold", annotation_font_size=10)
        stress_fig.update_layout(**LAYOUT, yaxis={'range': [0, 10], 'gridcolor': '#eee'}, xaxis={'gridcolor': '#eee'})
        
        # Heatmap
        heat = np.random.rand(6, 6) * 0.4 + 0.2; heat[4:6, 4:6] += 0.4
        heatmap_fig = go.Figure(go.Heatmap(z=heat, colorscale=[[0, '#e8f4fc'], [0.5, COLORS['orange']], [1, COLORS['red']]], showscale=False))
        heatmap_fig.update_layout(**LAYOUT, xaxis={'showticklabels': False}, yaxis={'showticklabels': False})
        
        # Events
        events = html.Div([html.Table([
            html.Thead([html.Tr([html.Th("Date"), html.Th("Event"), html.Th("Duration"), html.Th("Status")])]),
            html.Tbody([
                html.Tr([html.Td("Dec 04"), html.Td("High Stress"), html.Td("45 min"), html.Td(html.Span("Critical", className="status-pill critical"))]),
                html.Tr([html.Td("Dec 02"), html.Td("Prolonged Sitting"), html.Td("5h"), html.Td(html.Span("Warning", className="status-pill warning"))]),
            ])
        ], className="data-table")])
        
        # Plan
        plan = html.Div([
            html.Div("Priority: Stress Management", style={'fontWeight': '600', 'color': COLORS['red'], 'marginBottom': '12px'}),
            html.Ul([
                html.Li("Daily mindfulness exercises (10-15 min)"),
                html.Li("Ergonomic workspace assessment"),
                html.Li("Break reminders every 45 minutes")
            ], style={'paddingLeft': '18px', 'color': '#555', 'fontSize': '12px', 'lineHeight': '1.8'})
        ])
        
        return sessions, stress_fig, heatmap_fig, events, plan
