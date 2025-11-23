from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from database import get_historical_data
import datetime
import numpy as np

def render_therapist_tab():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4("Patient Analysis Dashboard"),
                dcc.Dropdown(
                    id='patient-selector',
                    options=[
                        {'label': 'John Doe (ID: 123)', 'value': '123'},
                        {'label': 'Jane Smith (ID: 456)', 'value': '456'}
                    ],
                    value='123',
                    className="mb-3"
                )
            ], width=8),
            dbc.Col([
                dbc.Button("Download Report (PDF)", id="btn-download-report", color="info", className="float-end")
            ], width=4)
        ], className="mb-3"),

        dbc.Row([
            # Left Sidebar: History Timeline
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Session History"),
                    dbc.CardBody([
                        html.Div(id='session-history-list', style={'height': '600px', 'overflow-y': 'scroll'})
                    ])
                ], className="h-100")
            ], width=3),

            # Main Area
            dbc.Col([
                # Top: Stress vs Time
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Stress Analysis (30 Days)"),
                            dbc.CardBody([
                                dcc.Graph(id='therapist-stress-graph', style={'height': '250px'})
                            ])
                        ])
                    ], width=12, className="mb-3")
                ]),

                # Middle: Posture Heatmap
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Posture Pressure Heatmap"),
                            dbc.CardBody([
                                dcc.Graph(id='posture-heatmap', style={'height': '300px'})
                            ])
                        ])
                    ], width=12, className="mb-3")
                ]),

                # Bottom: Abnormal Behavior & Recommendations
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Abnormal Events"),
                            dbc.CardBody([
                                html.Div(id='abnormal-events-table')
                            ])
                        ])
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Recommended Plan"),
                            dbc.CardBody([
                                html.Div(id='treatment-plan')
                            ])
                        ])
                    ], width=6),
                ])
            ], width=9)
        ])
    ], fluid=True, className="p-3")

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
        # Mock data generation based on patient_id
        # In real app, query DB with patient_id
        
        # 1. Session History
        sessions = []
        for i in range(10):
            date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            sessions.append(dbc.ListGroupItem(
                [
                    html.Div(f"Session {10-i}", className="fw-bold"),
                    html.Small(f"Date: {date}"),
                    html.Br(),
                    html.Small("Duration: 4h 20m", className="text-muted")
                ],
                action=True
            ))
        session_list = dbc.ListGroup(sessions)

        # 2. Stress Graph
        dates = pd.date_range(end=datetime.datetime.now(), periods=30).tolist()
        stress_values = np.random.randint(1, 9, size=30)
        # Add some spikes
        stress_values[5] = 9
        stress_values[15] = 8
        
        stress_fig = px.line(x=dates, y=stress_values, title="Stress Levels Over Time")
        stress_fig.add_hline(y=7, line_dash="dash", line_color="red", annotation_text="High Stress Threshold")
        stress_fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

        # 3. Posture Heatmap
        # Mock 10x10 grid for seat pressure
        heatmap_data = np.random.rand(10, 10)
        # Create a "bad posture" hot spot
        heatmap_data[7:9, 7:9] += 0.5
        
        heatmap_fig = px.imshow(heatmap_data, color_continuous_scale='RdBu_r', title="Seat Pressure Distribution")
        heatmap_fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

        # 4. Abnormal Events Table
        events_data = {
            "Date": ["2023-10-25", "2023-10-22", "2023-10-18"],
            "Event": ["High Stress", "Prolonged Sitting", "Poor Posture"],
            "Duration": ["45 min", "5 hours", "2 hours"]
        }
        events_df = pd.DataFrame(events_data)
        events_table = dbc.Table.from_dataframe(events_df, striped=True, bordered=True, hover=True)

        # 5. Treatment Plan
        plan = html.Div([
            html.H6("AI Recommendations:", className="text-primary"),
            html.Ul([
                html.Li("Prescribe lumbar support exercises."),
                html.Li("Suggest mindfulness breaks every 2 hours."),
                html.Li("Review workspace ergonomics (monitor height).")
            ])
        ])

        return session_list, stress_fig, heatmap_fig, events_table, plan
