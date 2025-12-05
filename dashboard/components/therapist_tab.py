from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from database import get_historical_data
import datetime
import numpy as np

# Chart template for dark theme
CHART_TEMPLATE = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#f1f5f9', 'family': 'Inter'},
    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40}
}

def render_therapist_tab():
    return dbc.Container([
        # Header Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4([
                        html.Span("⚕️", style={'marginRight': '10px'}),
                        "Patient Analysis Dashboard"
                    ], className="mb-0 d-flex align-items-center"),
                    html.Small("Clinical insights and treatment recommendations", className="text-muted")
                ])
            ], lg=6),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id='patient-selector',
                            options=[
                                {'label': '👤 John Doe (ID: 123)', 'value': '123'},
                                {'label': '👤 Jane Smith (ID: 456)', 'value': '456'},
                                {'label': '👤 Mike Johnson (ID: 789)', 'value': '789'}
                            ],
                            value='123',
                            className="mb-0",
                            style={'backgroundColor': 'rgba(255,255,255,0.05)'}
                        )
                    ], lg=8),
                    dbc.Col([
                        dbc.Button([
                            html.Span("📄", style={'marginRight': '6px'}),
                            "Export PDF"
                        ], id="btn-download-report", color="info", className="w-100")
                    ], lg=4)
                ])
            ], lg=6)
        ], className="mb-4 align-items-center"),

        dbc.Row([
            # Left Sidebar: Session History
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📅", style={'fontSize': '1.1rem'}),
                        " Session History"
                    ]),
                    dbc.CardBody([
                        html.Div(id='session-history-list', 
                                style={'height': '550px', 'overflowY': 'auto', 'paddingRight': '8px'})
                    ])
                ], className="h-100")
            ], lg=3, md=4, className="mb-4"),

            # Main Content Area
            dbc.Col([
                # Stress Analysis
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Span("📊", style={'fontSize': '1.1rem'}),
                                " Stress Analysis (30 Days)",
                                dbc.Badge("Trend ↑", color="warning", className="ms-auto")
                            ]),
                            dbc.CardBody([
                                dcc.Graph(id='therapist-stress-graph', style={'height': '200px'},
                                         config={'displayModeBar': False})
                            ])
                        ])
                    ], width=12, className="mb-4")
                ]),

                # Posture Heatmap
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Span("🔥", style={'fontSize': '1.1rem'}),
                                " Seat Pressure Distribution",
                                html.Small(" (Real-time)", className="text-muted ms-2")
                            ]),
                            dbc.CardBody([
                                dcc.Graph(id='posture-heatmap', style={'height': '250px'},
                                         config={'displayModeBar': False})
                            ])
                        ])
                    ], width=12, className="mb-4")
                ]),

                # Bottom Row: Events & Treatment Plan
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Span("⚠️", style={'fontSize': '1.1rem'}),
                                " Abnormal Events",
                                dbc.Badge(id='event-count', children="3", color="danger", className="ms-auto")
                            ]),
                            dbc.CardBody([
                                html.Div(id='abnormal-events-table', style={'maxHeight': '200px', 'overflowY': 'auto'})
                            ])
                        ], className="h-100")
                    ], lg=6, className="mb-4"),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Span("💊", style={'fontSize': '1.1rem'}),
                                " AI Treatment Recommendations"
                            ]),
                            dbc.CardBody([
                                html.Div(id='treatment-plan')
                            ])
                        ], className="h-100")
                    ], lg=6, className="mb-4")
                ])
            ], lg=9, md=8)
        ])
    ], fluid=True, className="p-3 animate-fade-in")

def register_therapist_callbacks(app):
    @app.callback(
        [Output('session-history-list', 'children'),
         Output('therapist-stress-graph', 'figure'),
         Output('posture-heatmap', 'figure'),
         Output('abnormal-events-table', 'children'),
         Output('treatment-plan', 'children')],
        [Input('patient-selector', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_therapist_view(patient_id, n):
        # 1. Session History with Timeline Design
        sessions = []
        for i in range(8):
            date = (datetime.datetime.now() - datetime.timedelta(days=i*2)).strftime('%b %d, %Y')
            is_recent = i == 0
            sessions.append(
                html.Div([
                    html.Div([
                        html.Div(style={
                            'width': '12px', 'height': '12px', 
                            'borderRadius': '50%',
                            'background': '#6366f1' if is_recent else 'rgba(255,255,255,0.2)',
                            'boxShadow': '0 0 10px rgba(99, 102, 241, 0.5)' if is_recent else 'none'
                        }),
                        html.Div(style={
                            'width': '2px', 'height': '40px', 
                            'background': 'rgba(255,255,255,0.1)',
                            'margin': '4px 0 4px 5px'
                        }) if i < 7 else None
                    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
                    html.Div([
                        html.Strong(f"Session {8-i}", style={'color': '#f1f5f9' if is_recent else '#94a3b8'}),
                        html.Br(),
                        html.Small(date, className="text-muted"),
                        html.Br(),
                        html.Small([
                            html.Span("Duration: ", className="text-muted"),
                            f"{np.random.randint(1, 5)}h {np.random.randint(0, 59)}m"
                        ], style={'color': '#6366f1'})
                    ], style={'marginLeft': '12px', 'flex': 1})
                ], style={
                    'display': 'flex', 
                    'padding': '8px 12px',
                    'background': 'rgba(99, 102, 241, 0.1)' if is_recent else 'transparent',
                    'borderRadius': '8px',
                    'cursor': 'pointer',
                    'marginBottom': '4px'
                })
            )
        session_list = html.Div(sessions)

        # 2. Stress Graph with Threshold Line
        dates = pd.date_range(end=datetime.datetime.now(), periods=30).tolist()
        stress_values = np.random.uniform(2, 7, size=30)
        stress_values[5] = 9.2
        stress_values[15] = 8.5
        stress_values[22] = 8.8
        
        stress_fig = go.Figure()
        stress_fig.add_trace(go.Scatter(
            x=dates, y=stress_values,
            mode='lines+markers',
            line={'color': '#6366f1', 'width': 2},
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.1)',
            marker={'size': 4},
            name='Stress Level'
        ))
        stress_fig.add_hline(y=7, line_dash="dash", line_color="#ef4444", 
                           annotation_text="Critical Threshold", annotation_font_color="#ef4444")
        stress_fig.update_layout(**CHART_TEMPLATE, 
                                yaxis={'range': [0, 10], 'gridcolor': 'rgba(255,255,255,0.05)'},
                                xaxis={'gridcolor': 'rgba(255,255,255,0.05)'},
                                showlegend=False)

        # 3. Posture Heatmap - Body Pressure Distribution
        heatmap_data = np.random.rand(8, 8) * 0.5 + 0.2
        heatmap_data[5:7, 5:7] += 0.4  # Hot spot
        heatmap_data[1:3, 1:3] += 0.3
        
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            colorscale=[
                [0, 'rgba(99, 102, 241, 0.2)'],
                [0.5, 'rgba(245, 158, 11, 0.6)'],
                [1, 'rgba(239, 68, 68, 0.9)']
            ],
            showscale=True,
            colorbar={'title': 'Pressure', 'tickfont': {'color': '#94a3b8'}}
        ))
        heatmap_fig.update_layout(**CHART_TEMPLATE,
                                 xaxis={'showticklabels': False, 'showgrid': False},
                                 yaxis={'showticklabels': False, 'showgrid': False})

        # 4. Abnormal Events Table
        events = [
            {'date': 'Dec 04', 'event': 'High Stress Spike', 'duration': '45 min', 'severity': 'critical'},
            {'date': 'Dec 02', 'event': 'Prolonged Sitting', 'duration': '5h 20m', 'severity': 'warning'},
            {'date': 'Nov 28', 'event': 'Poor Posture', 'duration': '2h 15m', 'severity': 'warning'}
        ]
        
        events_list = [
            html.Div([
                html.Div([
                    html.Span("🔴" if e['severity'] == 'critical' else "🟡", 
                             style={'marginRight': '10px'}),
                    html.Div([
                        html.Strong(e['event']),
                        html.Br(),
                        html.Small([
                            html.Span(e['date'], className="text-muted"),
                            " • ",
                            html.Span(e['duration'], style={'color': '#f59e0b'})
                        ])
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style={
                'padding': '10px 12px',
                'borderLeft': f"3px solid {'#ef4444' if e['severity'] == 'critical' else '#f59e0b'}",
                'background': 'rgba(255,255,255,0.02)',
                'borderRadius': '0 8px 8px 0',
                'marginBottom': '8px'
            }) for e in events
        ]
        events_html = html.Div(events_list)

        # 5. Treatment Plan
        plan = html.Div([
            html.Div([
                html.Span("🎯", style={'fontSize': '1.5rem', 'marginRight': '12px'}),
                html.Div([
                    html.Strong("Priority: Stress Management", style={'color': '#ef4444'}),
                    html.Br(),
                    html.Small("3 high-stress events this month", className="text-muted")
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '16px'}),
            
            html.H6("Recommended Actions:", className="text-muted mb-3"),
            
            html.Div([
                create_recommendation("🧘", "Prescribe daily mindfulness exercises", "10-15 min sessions"),
                create_recommendation("🪑", "Ergonomic assessment recommended", "Lumbar support needed"),
                create_recommendation("⏰", "Implement break reminders", "Every 45 minutes"),
                create_recommendation("📊", "Schedule follow-up in 2 weeks", "Review progress")
            ])
        ])
        
        return session_list, stress_fig, heatmap_fig, events_html, plan

def create_recommendation(icon, title, subtitle):
    return html.Div([
        html.Span(icon, style={'fontSize': '1.2rem', 'marginRight': '10px'}),
        html.Div([
            html.Span(title, style={'fontWeight': '500'}),
            html.Br(),
            html.Small(subtitle, className="text-muted")
        ])
    ], style={
        'display': 'flex',
        'alignItems': 'flex-start',
        'padding': '8px 0',
        'borderBottom': '1px solid rgba(255,255,255,0.05)'
    })
