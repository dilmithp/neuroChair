from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from database import get_recent_sensor_data
import datetime

def render_emergency_tab():
    return dbc.Container([
        # Header with Emergency Status
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2([
                        html.Span("🚨", style={'marginRight': '12px'}),
                        "Emergency Monitor"
                    ], className="emergency-header text-danger text-center mb-2"),
                    html.Div([
                        html.Div([
                            html.Span(className="live-dot"),
                            html.Span("System Active", style={'marginLeft': '8px'})
                        ], className="live-indicator mx-auto")
                    ], className="text-center")
                ], className="py-4")
            ])
        ]),

        # Quick Stats Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H3(id='monitored-users-count', children="54", 
                                   style={'fontSize': '2.5rem', 'fontWeight': '700', 'color': '#6366f1'}),
                            html.Small("Users Monitored", className="text-muted")
                        ], className="text-center")
                    ])
                ], style={'background': 'rgba(99, 102, 241, 0.1)', 'border': '1px solid rgba(99, 102, 241, 0.3)'})
            ], lg=3, md=6, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H3(id='active-alerts-count', children="1", 
                                   style={'fontSize': '2.5rem', 'fontWeight': '700', 'color': '#ef4444'}),
                            html.Small("Active Alerts", className="text-muted")
                        ], className="text-center")
                    ])
                ], style={'background': 'rgba(239, 68, 68, 0.1)', 'border': '1px solid rgba(239, 68, 68, 0.3)'})
            ], lg=3, md=6, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H3(id='resolved-today', children="12", 
                                   style={'fontSize': '2.5rem', 'fontWeight': '700', 'color': '#10b981'}),
                            html.Small("Resolved Today", className="text-muted")
                        ], className="text-center")
                    ])
                ], style={'background': 'rgba(16, 185, 129, 0.1)', 'border': '1px solid rgba(16, 185, 129, 0.3)'})
            ], lg=3, md=6, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H3(id='avg-response-time', children="2.3", 
                                   style={'fontSize': '2.5rem', 'fontWeight': '700', 'color': '#f59e0b'}),
                            html.Small("Avg Response (min)", className="text-muted")
                        ], className="text-center")
                    ])
                ], style={'background': 'rgba(245, 158, 11, 0.1)', 'border': '1px solid rgba(245, 158, 11, 0.3)'})
            ], lg=3, md=6, className="mb-4"),
        ]),

        # Active Alerts Area
        dbc.Row([
            dbc.Col([
                html.H5([
                    html.Span("⚡", style={'marginRight': '8px'}),
                    "Active Alerts"
                ], className="mb-3"),
                html.Div(id='active-alerts-container')
            ], lg=8, className="mb-4"),
            
            # Quick Actions
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🎛️", style={'fontSize': '1.1rem'}),
                        " Quick Actions"
                    ]),
                    dbc.CardBody([
                        dbc.Button([
                            html.Span("📢", style={'marginRight': '8px'}),
                            "Broadcast Alert"
                        ], color="danger", className="w-100 mb-2"),
                        dbc.Button([
                            html.Span("📞", style={'marginRight': '8px'}),
                            "Contact All Responders"
                        ], color="warning", className="w-100 mb-2"),
                        dbc.Button([
                            html.Span("✅", style={'marginRight': '8px'}),
                            "Mark All Resolved"
                        ], color="success", outline=True, className="w-100 mb-2"),
                        html.Hr(style={'borderColor': 'rgba(255,255,255,0.1)'}),
                        dbc.Button([
                            html.Span("⚙️", style={'marginRight': '8px'}),
                            "Alert Settings"
                        ], color="secondary", outline=True, className="w-100"),
                    ])
                ])
            ], lg=4, className="mb-4")
        ]),

        # Notification Log
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📋", style={'fontSize': '1.1rem'}),
                        " Notification Log",
                        html.Small(" (Last 24 hours)", className="text-muted ms-2")
                    ]),
                    dbc.CardBody([
                        html.Div(id='notification-log', style={'maxHeight': '250px', 'overflowY': 'auto'})
                    ])
                ])
            ], width=12)
        ])
    ], fluid=True, className="p-3 animate-fade-in")

def register_emergency_callbacks(app):
    @app.callback(
        [Output('active-alerts-container', 'children'),
         Output('notification-log', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_emergency_view(n):
        alerts = []
        notifications = []
        
        # Mock Alert Data - Critical Alert
        mock_alerts = [
            {
                "type": "Sustained High Stress",
                "user": "John Doe",
                "location": "Office - Floor 3",
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "value": "9.5/10",
                "duration": "18 minutes",
                "severity": "CRITICAL",
                "desc": "Stress level above threshold for extended period"
            }
        ]
        
        if len(mock_alerts) > 0:
            for alert in mock_alerts:
                card = dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.Span("🔴", style={'marginRight': '10px', 'animation': 'pulse 1s infinite'}),
                            html.Strong(f"CRITICAL: {alert['type']}", style={'color': '#ef4444'}),
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                        dbc.Badge(alert['severity'], color="danger", className="ms-auto")
                    ], style={'background': 'rgba(239, 68, 68, 0.2)', 'borderBottom': '2px solid #ef4444'}),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Div([
                                        html.Span("👤", style={'fontSize': '2rem', 'marginRight': '12px'}),
                                        html.Div([
                                            html.H5(alert['user'], className="mb-0"),
                                            html.Small(alert['location'], className="text-muted")
                                        ])
                                    ], style={'display': 'flex', 'alignItems': 'center'})
                                ])
                            ], md=6),
                            dbc.Col([
                                html.Div([
                                    create_stat_item("📊", "Reading", alert['value']),
                                    create_stat_item("⏱️", "Duration", alert['duration']),
                                    create_stat_item("🕐", "Detected", alert['time']),
                                ])
                            ], md=6)
                        ]),
                        html.Hr(style={'borderColor': 'rgba(255,255,255,0.1)', 'margin': '16px 0'}),
                        html.P([
                            html.Span("ℹ️", style={'marginRight': '8px'}),
                            alert['desc']
                        ], className="text-muted mb-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button([
                                    html.Span("✅", style={'marginRight': '6px'}),
                                    "Acknowledge"
                                ], color="success", size="sm", className="me-2")
                            ], width="auto"),
                            dbc.Col([
                                dbc.Button([
                                    html.Span("📞", style={'marginRight': '6px'}),
                                    "Contact User"
                                ], color="primary", size="sm", className="me-2")
                            ], width="auto"),
                            dbc.Col([
                                dbc.Button([
                                    html.Span("🚑", style={'marginRight': '6px'}),
                                    "Call Emergency"
                                ], color="danger", outline=True, size="sm")
                            ], width="auto"),
                        ])
                    ])
                ], className="alert-card-critical mb-3")
                alerts.append(card)
                
                # Notification log entries
                notifications.extend([
                    create_notification_entry(alert['time'], "SMS sent to Emergency Contact", "success"),
                    create_notification_entry(
                        (datetime.datetime.now() - datetime.timedelta(minutes=2)).strftime("%H:%M:%S"),
                        f"Alert triggered for {alert['user']}", "warning"
                    ),
                    create_notification_entry(
                        (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%H:%M:%S"),
                        "Stress threshold exceeded - monitoring initiated", "info"
                    )
                ])
        else:
            alerts.append(
                dbc.Alert([
                    html.Span("✅", style={'marginRight': '10px', 'fontSize': '1.5rem'}),
                    html.Strong("All Clear - No active critical alerts")
                ], color="success", className="d-flex align-items-center")
            )
            notifications.append(
                html.Div("No recent notifications.", className="text-muted text-center py-4")
            )

        return alerts, notifications

def create_stat_item(icon, label, value):
    return html.Div([
        html.Span(icon, style={'marginRight': '8px'}),
        html.Small(label + ": ", className="text-muted"),
        html.Span(value, style={'fontWeight': '600', 'color': '#f1f5f9'})
    ], style={'marginBottom': '6px'})

def create_notification_entry(time, message, status):
    colors = {'success': '#10b981', 'warning': '#f59e0b', 'info': '#06b6d4', 'danger': '#ef4444'}
    icons = {'success': '✅', 'warning': '⚠️', 'info': 'ℹ️', 'danger': '🚨'}
    
    return html.Div([
        html.Span(icons.get(status, 'ℹ️'), style={'marginRight': '10px'}),
        html.Span(f"[{time}]", style={'color': '#64748b', 'marginRight': '10px', 'fontFamily': 'monospace'}),
        html.Span(message, style={'color': colors.get(status, '#94a3b8')})
    ], style={
        'padding': '10px 12px',
        'borderLeft': f"3px solid {colors.get(status, '#64748b')}",
        'background': 'rgba(255,255,255,0.02)',
        'borderRadius': '0 6px 6px 0',
        'marginBottom': '6px'
    })
