from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import datetime

COLORS = {'blue': '#4e79a7', 'orange': '#f28e2c', 'red': '#e15759', 'green': '#59a14f'}

def render_emergency_tab():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H5("Emergency Alerts", style={'fontWeight': '600', 'color': COLORS['red']}),
                html.Span("Monitoring active", className="status-indicator", style={'marginLeft': '12px'})
            ], className="d-flex align-items-center")
        ], className="mb-4"),

        # Stats
        dbc.Row([
            dbc.Col([create_stat("54", "Monitored", COLORS['blue'])], lg=3, md=6, className="mb-3"),
            dbc.Col([create_stat("1", "Active Alerts", COLORS['red'])], lg=3, md=6, className="mb-3"),
            dbc.Col([create_stat("12", "Resolved Today", COLORS['green'])], lg=3, md=6, className="mb-3"),
            dbc.Col([create_stat("2.3m", "Avg Response", COLORS['orange'])], lg=3, md=6, className="mb-3"),
        ]),

        # Alerts & Actions
        dbc.Row([
            dbc.Col([
                html.H6("Active Alerts", style={'fontWeight': '600', 'marginBottom': '12px'}),
                html.Div(id='alerts-container')
            ], lg=8, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("QUICK ACTIONS"),
                    dbc.CardBody([
                        dbc.Button("Broadcast Alert", color="danger", size="sm", className="w-100 mb-2"),
                        dbc.Button("Contact Responders", color="warning", size="sm", className="w-100 mb-2"),
                        dbc.Button("Mark All Resolved", outline=True, color="success", size="sm", className="w-100"),
                    ])
                ])
            ], lg=4, className="mb-3")
        ]),

        # Log
        dbc.Card([
            dbc.CardHeader("NOTIFICATION LOG"),
            dbc.CardBody([html.Div(id='notif-log', style={'maxHeight': '180px', 'overflowY': 'auto'})])
        ])
    ], fluid=True)

def create_stat(value, label, color):
    return dbc.Card([
        dbc.CardBody([
            html.Div(value, style={'fontSize': '32px', 'fontWeight': '300', 'color': color}),
            html.Div(label, style={'fontSize': '11px', 'color': '#888', 'textTransform': 'uppercase'})
        ], className="text-center", style={'borderLeft': f'3px solid {color}', 'paddingLeft': '16px'})
    ])

def register_emergency_callbacks(app):
    @app.callback([Output('alerts-container', 'children'), Output('notif-log', 'children')],
                  [Input('interval-component', 'n_intervals')])
    def update(n):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        
        alert = dbc.Card([
            dbc.CardHeader([
                html.Span("CRITICAL", className="status-pill critical", style={'marginRight': '10px'}),
                html.Span("Sustained High Stress", style={'fontWeight': '600'})
            ], style={'background': 'rgba(225,87,89,0.05)', 'borderBottom': f'2px solid {COLORS["red"]}'}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div("John Doe", style={'fontWeight': '600', 'fontSize': '14px'}),
                        html.Div("Office - Floor 3", style={'fontSize': '12px', 'color': '#888'})
                    ], md=4),
                    dbc.Col([
                        html.Table([
                            html.Tr([html.Td("Reading:", style={'color': '#888'}), html.Td("9.5/10", style={'fontWeight': '600'})]),
                            html.Tr([html.Td("Duration:", style={'color': '#888'}), html.Td("18 min", style={'fontWeight': '600'})])
                        ], style={'fontSize': '12px'})
                    ], md=4),
                    dbc.Col([
                        dbc.ButtonGroup([
                            dbc.Button("Acknowledge", color="success", size="sm"),
                            dbc.Button("Contact", color="primary", size="sm"),
                        ])
                    ], md=4, className="text-end")
                ])
            ])
        ], style={'border': f'1px solid {COLORS["red"]}', 'marginBottom': '12px'})
        
        logs = [
            html.Div([html.Span(f"[{now}]", style={'color': '#999', 'marginRight': '12px', 'fontFamily': 'monospace', 'fontSize': '11px'}),
                     html.Span("SMS sent to emergency contact")], className="alert-item success"),
            html.Div([html.Span(f"[{(datetime.datetime.now()-datetime.timedelta(minutes=2)).strftime('%H:%M:%S')}]", 
                     style={'color': '#999', 'marginRight': '12px', 'fontFamily': 'monospace', 'fontSize': '11px'}),
                     html.Span("Alert triggered for John Doe")], className="alert-item warning"),
        ]
        
        return [alert], logs
