from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import datetime

COLORS = {'blue': '#4e79a7', 'orange': '#f28e2c', 'red': '#e15759', 'green': '#59a14f', 'teal': '#76b7b2'}

def render_emergency_tab():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H5("Emergency Monitoring Center", style={'fontWeight': '600', 'color': COLORS['red']}),
                html.Small("Real-time critical alert monitoring", className="text-muted")
            ], lg=6),
            dbc.Col([
                html.Div([
                    html.Span(className="status-dot"),
                    html.Span("System Active", style={'marginLeft': '6px'})
                ], className="status-indicator float-end")
            ], lg=6)
        ], className="mb-3 align-items-center"),

        # Stats Row
        dbc.Row([
            dbc.Col([create_stat_card('em-monitored', 'MONITORED')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_stat_card('em-active', 'ACTIVE ALERTS')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_stat_card('em-critical', 'CRITICAL')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_stat_card('em-resolved', 'RESOLVED TODAY')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_stat_card('em-response', 'AVG RESPONSE')], lg=2, md=4, className="mb-3"),
            dbc.Col([create_stat_card('em-uptime', 'UPTIME')], lg=2, md=4, className="mb-3"),
        ]),

        # Main Content
        dbc.Row([
            # Active Alerts
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        "ACTIVE ALERTS",
                        dbc.Badge(id='alert-badge', children="1", color="danger", className="ms-2")
                    ]),
                    dbc.CardBody([html.Div(id='alerts-container', style={'maxHeight': '320px', 'overflowY': 'auto'})])
                ])
            ], lg=8, className="mb-3"),
            
            # Quick Actions
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("QUICK ACTIONS"),
                    dbc.CardBody([
                        dbc.Button("Broadcast Alert", color="danger", className="w-100 mb-2"),
                        dbc.Button("Contact All Responders", color="warning", className="w-100 mb-2"),
                        dbc.Button("Acknowledge All", outline=True, color="secondary", className="w-100 mb-2"),
                        html.Hr(),
                        dbc.Button("Alert Settings", outline=True, color="secondary", className="w-100 mb-2"),
                        dbc.Button("View Reports", outline=True, color="secondary", className="w-100"),
                    ])
                ])
            ], lg=4, className="mb-3"),
        ]),

        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("ALERTS TODAY (24H)"),
                    dbc.CardBody([dcc.Graph(id='alerts-timeline', style={'height': '150px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("ALERTS BY TYPE"),
                    dbc.CardBody([dcc.Graph(id='alerts-type', style={'height': '150px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("RESPONSE TIME TREND"),
                    dbc.CardBody([dcc.Graph(id='response-trend', style={'height': '150px'}, config={'displayModeBar': False})])
                ])
            ], lg=4, className="mb-3"),
        ]),

        # Notification Log
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("NOTIFICATION LOG"),
                    dbc.CardBody([html.Div(id='notif-log', style={'maxHeight': '150px', 'overflowY': 'auto'})])
                ])
            ], lg=8, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("RESPONDER STATUS"),
                    dbc.CardBody([html.Div(id='responder-status')])
                ])
            ], lg=4, className="mb-3"),
        ]),
    ], fluid=True)

def create_stat_card(div_id, label):
    return dbc.Card([dbc.CardBody([html.Div(id=div_id)], className="py-2")])

def register_emergency_callbacks(app):
    @app.callback(
        [Output('em-monitored', 'children'), Output('em-active', 'children'),
         Output('em-critical', 'children'), Output('em-resolved', 'children'),
         Output('em-response', 'children'), Output('em-uptime', 'children'),
         Output('alerts-container', 'children'), Output('alert-badge', 'children'),
         Output('alerts-timeline', 'figure'), Output('alerts-type', 'figure'),
         Output('response-trend', 'figure'), Output('notif-log', 'children'),
         Output('responder-status', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update(n):
        now = datetime.datetime.now()
        
        # Stats
        stats = [
            create_stat_content("54", "MONITORED", COLORS['blue']),
            create_stat_content("1", "ACTIVE ALERTS", COLORS['red']),
            create_stat_content("1", "CRITICAL", COLORS['red']),
            create_stat_content("12", "RESOLVED TODAY", COLORS['green']),
            create_stat_content("2.3m", "AVG RESPONSE", COLORS['orange']),
            create_stat_content("99.9%", "UPTIME", COLORS['green']),
        ]
        
        # Active Alert
        alert = dbc.Card([
            dbc.CardHeader([
                html.Span("CRITICAL", className="status-pill critical", style={'marginRight': '12px'}),
                html.Span("Sustained High Stress", style={'fontWeight': '600'}),
                html.Span(now.strftime("%H:%M:%S"), style={'float': 'right', 'color': '#888', 'fontSize': '11px'})
            ], style={'background': 'rgba(225,87,89,0.08)', 'borderBottom': f'2px solid {COLORS["red"]}'}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div("John Doe", style={'fontWeight': '600', 'fontSize': '14px'}),
                        html.Div("Office - Floor 3, Desk 42", style={'fontSize': '12px', 'color': '#888'}),
                        html.Div("Employee ID: 12345", style={'fontSize': '11px', 'color': '#aaa'})
                    ], md=3),
                    dbc.Col([
                        html.Table([
                            html.Tr([html.Td("Stress Level:", style={'color': '#888', 'fontSize': '11px'}), 
                                    html.Td("9.5/10", style={'fontWeight': '600', 'color': COLORS['red']})]),
                            html.Tr([html.Td("Duration:", style={'color': '#888', 'fontSize': '11px'}), 
                                    html.Td("18 min", style={'fontWeight': '600'})]),
                            html.Tr([html.Td("Heart Rate:", style={'color': '#888', 'fontSize': '11px'}), 
                                    html.Td("95 bpm", style={'fontWeight': '600', 'color': COLORS['orange']})]),
                        ], style={'fontSize': '12px'})
                    ], md=3),
                    dbc.Col([
                        html.Div("Emergency Contact:", style={'fontSize': '10px', 'color': '#888', 'textTransform': 'uppercase'}),
                        html.Div("Jane Doe (Spouse)", style={'fontSize': '12px'}),
                        html.Div("+1 555-123-4567", style={'fontSize': '12px', 'color': COLORS['blue']})
                    ], md=3),
                    dbc.Col([
                        dbc.Button("Acknowledge", color="success", size="sm", className="w-100 mb-2"),
                        dbc.Button("Contact", color="primary", size="sm", className="w-100 mb-2"),
                        dbc.Button("Escalate", color="danger", outline=True, size="sm", className="w-100"),
                    ], md=3)
                ])
            ])
        ], style={'border': f'1px solid {COLORS["red"]}', 'marginBottom': '12px'})
        
        # Charts
        LAYOUT = {'paper_bgcolor': 'white', 'plot_bgcolor': 'white', 'font': {'size': 10, 'color': '#555'}, 'margin': {'l': 30, 'r': 20, 't': 20, 'b': 30}}
        
        # Timeline
        hours = [f"{h}:00" for h in range(8, 20)]
        alerts = [0, 0, 1, 2, 1, 0, 1, 3, 2, 1, 0, 1]
        timeline = go.Figure(go.Bar(x=hours, y=alerts, marker_color=[COLORS['red'] if a > 1 else COLORS['orange'] if a == 1 else '#ddd' for a in alerts]))
        timeline.update_layout(**LAYOUT, yaxis={'gridcolor': '#eee'})
        
        # Type pie
        types = go.Figure(go.Pie(values=[5, 3, 2, 2], labels=['High Stress', 'Poor Posture', 'Long Sitting', 'Other'],
                                marker={'colors': [COLORS['red'], COLORS['orange'], COLORS['blue'], '#ddd']}, hole=0.5, textinfo='percent', textfont={'size': 9}))
        types.update_layout(**LAYOUT, showlegend=True, legend={'font': {'size': 9}})
        
        # Response trend
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        response = [3.1, 2.8, 2.5, 2.3, 2.0, 2.2, 2.3]
        resp_fig = go.Figure(go.Scatter(x=days, y=response, mode='lines+markers', line={'color': COLORS['teal'], 'width': 2}, fill='tozeroy', fillcolor='rgba(118,183,178,0.1)'))
        resp_fig.update_layout(**LAYOUT, yaxis={'title': 'min', 'gridcolor': '#eee'})
        
        # Notification log
        logs = [
            create_log_entry(now.strftime("%H:%M:%S"), "SMS sent to emergency contact", "success"),
            create_log_entry((now - datetime.timedelta(minutes=2)).strftime("%H:%M:%S"), "Alert triggered - High stress detected", "warning"),
            create_log_entry((now - datetime.timedelta(minutes=5)).strftime("%H:%M:%S"), "Threshold exceeded (9.5/10)", "critical"),
            create_log_entry((now - datetime.timedelta(hours=1)).strftime("%H:%M:%S"), "Previous alert resolved", "success"),
        ]
        
        # Responder Status
        responders = html.Div([html.Table([
            html.Tbody([
                html.Tr([html.Td("Dr. Smith"), html.Td(html.Span("Online", className="status-pill normal"))]),
                html.Tr([html.Td("Nurse Johnson"), html.Td(html.Span("Online", className="status-pill normal"))]),
                html.Tr([html.Td("HR Manager"), html.Td(html.Span("Away", className="status-pill warning"))]),
            ])
        ], className="data-table")])
        
        return (*stats, [alert], "1", timeline, types, resp_fig, logs, responders)

def create_stat_content(value, label, color):
    return html.Div([
        html.Div(value, style={'fontSize': '24px', 'fontWeight': '300', 'color': color}),
        html.Div(label, style={'fontSize': '9px', 'color': '#888', 'textTransform': 'uppercase'})
    ], className="text-center")

def create_log_entry(time, message, level):
    border_colors = {'success': COLORS['green'], 'warning': COLORS['orange'], 'critical': COLORS['red']}
    return html.Div([
        html.Span(f"[{time}]", style={'color': '#999', 'marginRight': '12px', 'fontFamily': 'monospace', 'fontSize': '11px'}),
        html.Span(message, style={'fontSize': '12px'})
    ], className=f"alert-item {level}", style={'borderColor': border_colors.get(level, '#ddd')})
