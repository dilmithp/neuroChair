from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np

def render_employer_tab():
    return dbc.Container([
        html.H4("Workplace Wellness Analytics (Anonymous)", className="mb-4"),
        
        dbc.Row([
            # Top Left: Organization Stress Index
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Organization Stress Index"),
                    dbc.CardBody([
                        dcc.Graph(id='org-stress-gauge', style={'height': '250px'})
                    ])
                ], className="h-100")
            ], width=6),

            # Top Right: Posture Trends
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Workplace Posture Trends (30 Days)"),
                    dbc.CardBody([
                        dcc.Graph(id='org-posture-trend', style={'height': '250px'})
                    ])
                ], className="h-100")
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            # Middle Left: Productivity vs Posture
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Posture vs. Sitting Duration"),
                    dbc.CardBody([
                        dcc.Graph(id='prod-posture-scatter', style={'height': '300px'})
                    ])
                ], className="h-100")
            ], width=6),

            # Middle Right: Stress by Hour
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Average Stress by Hour of Day"),
                    dbc.CardBody([
                        dcc.Graph(id='stress-by-hour', style={'height': '300px'})
                    ])
                ], className="h-100")
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            # Bottom Left: Group Comparison
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Team Comparison"),
                    dbc.CardBody([
                        dcc.Graph(id='team-comparison', style={'height': '300px'})
                    ])
                ], className="h-100")
            ], width=6),

            # Bottom Right: Summary Card
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Wellness Summary"),
                    dbc.CardBody([
                        html.Div(id='wellness-summary-stats')
                    ])
                ], className="h-100")
            ], width=6),
        ])
    ], fluid=True, className="p-3")

def register_employer_callbacks(app):
    @app.callback(
        [Output('org-stress-gauge', 'figure'),
         Output('org-posture-trend', 'figure'),
         Output('prod-posture-scatter', 'figure'),
         Output('stress-by-hour', 'figure'),
         Output('team-comparison', 'figure'),
         Output('wellness-summary-stats', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_employer_view(n):
        # Mock Aggregated Data
        
        # 1. Org Stress Gauge
        avg_stress = 5.2
        gauge_fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_stress,
            title = {'text': "Avg Stress"},
            gauge = {
                'axis': {'range': [0, 10]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, 3], 'color': "lightgreen"},
                    {'range': [3, 7], 'color': "lightyellow"},
                    {'range': [7, 10], 'color': "salmon"}
                ],
            }
        ))
        gauge_fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

        # 2. Posture Trend
        dates = pd.date_range(end=pd.Timestamp.now(), periods=30).tolist()
        posture_scores = np.linspace(60, 75, 30) + np.random.normal(0, 2, 30)
        trend_fig = px.line(x=dates, y=posture_scores, title="Avg Posture Score")
        trend_fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

        # 3. Scatter
        n_points = 50
        sitting_hours = np.random.uniform(2, 9, n_points)
        posture_vals = 100 - (sitting_hours * 5) + np.random.normal(0, 5, n_points)
        scatter_fig = px.scatter(x=sitting_hours, y=posture_vals, labels={'x': 'Sitting Hours', 'y': 'Posture Score'})
        scatter_fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

        # 4. Stress by Hour
        hours = list(range(9, 19))
        stress_hourly = [3, 4, 5, 6, 5, 4, 3, 4, 5, 6]
        bar_fig = px.bar(x=hours, y=stress_hourly, labels={'x': 'Hour', 'y': 'Avg Stress'})
        bar_fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

        # 5. Team Comparison
        teams = ['Engineering', 'Sales', 'HR']
        team_stress = [6, 7, 4]
        team_posture = [50, 60, 80]
        
        team_fig = go.Figure(data=[
            go.Bar(name='Stress', x=teams, y=team_stress),
            go.Bar(name='Posture', x=teams, y=team_posture)
        ])
        team_fig.update_layout(barmode='group', margin=dict(l=20, r=20, t=30, b=20))

        # 6. Summary Stats
        stats = html.Div([
            html.H3("54 Employees Monitored", className="text-primary"),
            html.Hr(),
            html.P(["Avg Sitting Time: ", html.Strong("6.2 hours")]),
            html.P(["Good Posture Rate: ", html.Strong("65%")]),
            html.P(["Stress Improvement: ", html.Strong("+12%"), " vs last week", html.Span(" ▲", className="text-success")])
        ])

        return gauge_fig, trend_fig, scatter_fig, bar_fig, team_fig, stats
