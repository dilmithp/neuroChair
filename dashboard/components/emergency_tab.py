from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from database import get_recent_sensor_data
import datetime

def render_emergency_tab():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2("🚨 Emergency Monitor", className="text-danger text-center my-4")
            ])
        ]),

        # Active Alerts Area
        dbc.Row([
            dbc.Col([
                html.Div(id='active-alerts-container')
            ])
        ]),

        # Notification Status Footer
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Notification Log", className="card-title"),
                        html.Div(id='notification-log')
                    ])
                ], className="mt-4")
            ])
        ])
    ], fluid=True, className="p-3")

def register_emergency_callbacks(app):
    @app.callback(
        [Output('active-alerts-container', 'children'),
         Output('notification-log', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_emergency_view(n):
        # Logic: Check for critical conditions
        # In a real app, we might query a specific 'alerts' collection or check recent sensor data
        # For this demo, we'll check the latest sensor data and simulate alerts
        
        alerts = []
        notifications = []
        
        # Mock data or fetch real
        # Let's simulate an alert if n is odd, or just random, or based on real data if available
        # We'll use the get_recent_sensor_data but we need to simulate "sustained" conditions.
        # For the purpose of the UI demo, we will generate a mock alert.
        
        # Mock Alert Data
        mock_alerts = [
            {
                "type": "High Stress",
                "user": "John Doe",
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "value": "9.5/10",
                "severity": "CRITICAL",
                "desc": "Sustained high stress > 15 mins"
            }
        ]
        
        if len(mock_alerts) > 0:
            for alert in mock_alerts:
                card = dbc.Card([
                    dbc.CardHeader(f"ALERT: {alert['type']}", className="bg-danger text-white"),
                    dbc.CardBody([
                        html.H4(f"User: {alert['user']}", className="card-title"),
                        html.P(f"Time: {alert['time']}", className="card-text"),
                        html.P(f"Current Reading: {alert['value']}", className="card-text fw-bold"),
                        html.P(f"Condition: {alert['desc']}", className="card-text"),
                        dbc.Button("Acknowledge & Dismiss", color="secondary", size="sm")
                    ])
                ], className="mb-3 border-danger")
                alerts.append(card)
                
                notifications.append(
                    html.Div([
                        html.Span(f"[{alert['time']}] ", className="text-muted"),
                        html.Span(f"SMS sent to Emergency Contact for {alert['user']}", className="fw-bold")
                    ], className="border-bottom py-2")
                )
        else:
            alerts.append(
                dbc.Alert("No active critical alerts.", color="success")
            )
            notifications.append(html.Div("No recent notifications."))

        return alerts, notifications
