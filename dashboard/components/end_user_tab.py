from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from database import get_recent_sensor_data, get_historical_data
import datetime

# Chart template for consistent dark styling
CHART_TEMPLATE = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#f1f5f9', 'family': 'Inter'},
    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40}
}

def render_end_user_tab():
    return dbc.Container([
        # Top Row: Real-time Metrics
        dbc.Row([
            # Stress Gauge
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("⚡", style={'fontSize': '1.2rem'}),
                        " Real-time Stress Level"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='stress-gauge', style={'height': '220px'}, config={'displayModeBar': False})
                    ])
                ], className="h-100")
            ], lg=4, md=6, className="mb-4"),
            
            # Posture Status Card
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🧘", style={'fontSize': '1.2rem'}),
                        " Posture Status"
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div(id='posture-status-icon', className="posture-indicator"),
                        ], className="text-center mb-3"),
                        html.H4(id='posture-score-text', className="text-center mb-3", 
                               style={'background': 'linear-gradient(135deg, #6366f1, #8b5cf6)', 
                                      '-webkit-background-clip': 'text', 
                                      '-webkit-text-fill-color': 'transparent'}),
                        dbc.Progress(id='posture-progress', value=0, striped=True, animated=True, 
                                   className="mb-2", style={'height': '12px'})
                    ])
                ], className="h-100")
            ], lg=4, md=6, className="mb-4"),
            
            # Daily Sitting Duration
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("⏰", style={'fontSize': '1.2rem'}),
                        " Daily Sitting Duration"
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div(className="icon-container warning", children="🪑"),
                            html.H2(id='sitting-duration-text', className="text-center mb-2",
                                   style={'color': '#f59e0b', 'fontWeight': '700'}),
                            dbc.Progress(id='sitting-progress', value=0, max=8, className="mb-3",
                                       style={'height': '12px'}),
                            html.Div([
                                html.Small("🎯 Goal: < 6 hours/day", className="text-muted")
                            ], className="text-center")
                        ])
                    ])
                ], className="h-100")
            ], lg=4, md=12, className="mb-4"),
        ]),

        # Middle Row: Alerts & Coaching
        dbc.Row([
            # Live Alerts
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🔔", style={'fontSize': '1.2rem'}),
                        " Live Alerts & Notifications",
                        html.Span(id='alert-count-badge', className="status-badge warning ms-auto", 
                                 style={'fontSize': '0.75rem'})
                    ]),
                    dbc.CardBody([
                        html.Div(id='live-alerts-box', className="overflow-auto", 
                                style={'height': '180px', 'paddingRight': '10px'})
                    ])
                ], className="h-100")
            ], lg=6, className="mb-4"),

            # Coaching Suggestions
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("💡", style={'fontSize': '1.2rem'}),
                        " Smart Coaching Tips"
                    ]),
                    dbc.CardBody([
                        html.Div(id='coaching-suggestions-list', className="overflow-auto",
                                style={'height': '180px'})
                    ])
                ], className="h-100")
            ], lg=6, className="mb-4"),
        ]),

        # Bottom Row: Weekly Progress
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📈", style={'fontSize': '1.2rem'}),
                        " Weekly Progress Overview",
                        html.Div([
                            dbc.Badge("7 Days", color="primary", className="ms-auto")
                        ], className="ms-auto")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='weekly-progress-graph', style={'height': '320px'}, 
                                 config={'displayModeBar': False})
                    ])
                ])
            ], width=12)
        ])
    ], fluid=True, className="p-3 animate-fade-in")

def register_end_user_callbacks(app):
    @app.callback(
        [Output('stress-gauge', 'figure'),
         Output('posture-status-icon', 'children'),
         Output('posture-status-icon', 'className'),
         Output('posture-score-text', 'children'),
         Output('posture-progress', 'value'),
         Output('posture-progress', 'color'),
         Output('sitting-duration-text', 'children'),
         Output('sitting-progress', 'value'),
         Output('sitting-progress', 'color'),
         Output('live-alerts-box', 'children'),
         Output('coaching-suggestions-list', 'children'),
         Output('weekly-progress-graph', 'figure')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_end_user_metrics(n):
        # Fetch latest data
        recent_data = get_recent_sensor_data(limit=1)
        if not recent_data:
            # Return empty/default values if no data
            empty_gauge = create_stress_gauge(0)
            empty_weekly = create_weekly_chart([], [], [])
            return (empty_gauge, "❓", "posture-indicator", "No Data", 0, "secondary", 
                   "0h 0m", 0, "secondary", 
                   [create_alert_item("info", "Waiting for data...", "Connecting to sensors")],
                   [], empty_weekly)

        latest = recent_data[0]
        stress = latest.get('stress_level', 0)
        posture = latest.get('posture_score', 0)
        
        # 1. Stress Gauge
        stress_fig = create_stress_gauge(stress)

        # 2. Posture Status
        if posture >= 80:
            posture_icon = "✅"
            posture_class = "posture-indicator good"
        elif posture >= 50:
            posture_icon = "⚠️"
            posture_class = "posture-indicator"
        else:
            posture_icon = "❌"
            posture_class = "posture-indicator bad"
            
        posture_text = f"Score: {posture}/100"
        posture_color = "success" if posture >= 80 else "warning" if posture >= 50 else "danger"

        # 3. Sitting Duration
        sitting_hours = 4.5  # Mock value
        sitting_text = f"{sitting_hours} hours"
        sitting_color = "success" if sitting_hours < 4 else "warning" if sitting_hours < 6 else "danger"
        
        # 4. Live Alerts
        alerts = []
        if stress > 7:
            alerts.append(create_alert_item("danger", "High Stress Detected!", 
                                           "Take a deep breath and consider a short break"))
        if posture < 50:
            alerts.append(create_alert_item("warning", "Poor Posture Detected", 
                                           "Straighten your back and adjust your seating"))
        if sitting_hours > 6:
            alerts.append(create_alert_item("warning", "Prolonged Sitting", 
                                           "You've been sitting for over 6 hours. Time to stand!"))
        if not alerts:
            alerts.append(create_alert_item("success", "All Systems Normal", 
                                           "Great job maintaining good habits!"))

        # 5. Coaching Suggestions
        suggestions = create_coaching_suggestions(stress, posture)

        # 6. Weekly Progress Graph
        dates = pd.date_range(end=datetime.datetime.now(), periods=7).strftime('%a').tolist()
        mock_stress = [3, 4, 5, 3, 6, 4, stress]
        mock_posture = [80, 75, 60, 85, 70, 80, posture]
        weekly_fig = create_weekly_chart(dates, mock_stress, mock_posture)

        return (stress_fig, posture_icon, posture_class, posture_text, posture, posture_color,
                sitting_text, sitting_hours, sitting_color, alerts, suggestions, weekly_fig)

def create_stress_gauge(stress):
    """Create a stylized stress gauge"""
    if stress <= 3:
        bar_color = "#10b981"
    elif stress <= 6:
        bar_color = "#f59e0b"
    else:
        bar_color = "#ef4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stress,
        number={'font': {'size': 48, 'color': '#f1f5f9'}},
        gauge={
            'axis': {'range': [0, 10], 'tickcolor': '#64748b', 'tickwidth': 2},
            'bar': {'color': bar_color, 'thickness': 0.75},
            'bgcolor': 'rgba(255,255,255,0.05)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 3], 'color': 'rgba(16, 185, 129, 0.2)'},
                {'range': [3, 7], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [7, 10], 'color': 'rgba(239, 68, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#ef4444", 'width': 2},
                'thickness': 0.8,
                'value': 7
            }
        }
    ))
    fig.update_layout(**CHART_TEMPLATE)
    return fig

def create_weekly_chart(dates, stress_data, posture_data):
    """Create weekly progress chart with gradient fills"""
    fig = go.Figure()
    
    if dates:
        # Stress line
        fig.add_trace(go.Scatter(
            x=dates, y=stress_data,
            name='Stress Level',
            line={'color': '#ef4444', 'width': 3},
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.1)',
            mode='lines+markers',
            marker={'size': 8, 'color': '#ef4444'}
        ))
        
        # Posture bars
        fig.add_trace(go.Bar(
            x=dates, y=posture_data,
            name='Posture Score',
            marker={'color': 'rgba(99, 102, 241, 0.6)', 'line': {'color': '#6366f1', 'width': 2}},
            yaxis='y2',
            opacity=0.7
        ))
    
    fig.update_layout(
        **CHART_TEMPLATE,
        showlegend=True,
        legend={'orientation': 'h', 'y': 1.15, 'x': 0, 'font': {'size': 11}},
        yaxis={'title': 'Stress (0-10)', 'range': [0, 10], 'gridcolor': 'rgba(255,255,255,0.05)', 
               'zerolinecolor': 'rgba(255,255,255,0.1)'},
        yaxis2={'title': 'Posture Score', 'range': [0, 100], 'overlaying': 'y', 'side': 'right',
                'gridcolor': 'rgba(255,255,255,0.05)'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.05)'},
        bargap=0.4
    )
    return fig

def create_alert_item(alert_type, title, description):
    """Create a styled alert item"""
    colors = {
        'success': {'bg': 'rgba(16, 185, 129, 0.15)', 'border': '#10b981', 'icon': '✅'},
        'warning': {'bg': 'rgba(245, 158, 11, 0.15)', 'border': '#f59e0b', 'icon': '⚠️'},
        'danger': {'bg': 'rgba(239, 68, 68, 0.15)', 'border': '#ef4444', 'icon': '🚨'},
        'info': {'bg': 'rgba(6, 182, 212, 0.15)', 'border': '#06b6d4', 'icon': 'ℹ️'}
    }
    style = colors.get(alert_type, colors['info'])
    
    return html.Div([
        html.Div([
            html.Span(style['icon'], style={'fontSize': '1.2rem', 'marginRight': '10px'}),
            html.Div([
                html.Strong(title, style={'display': 'block'}),
                html.Small(description, className="text-muted")
            ])
        ], style={'display': 'flex', 'alignItems': 'flex-start'})
    ], style={
        'background': style['bg'],
        'borderLeft': f'4px solid {style["border"]}',
        'padding': '12px 16px',
        'borderRadius': '8px',
        'marginBottom': '10px'
    })

def create_coaching_suggestions(stress, posture):
    """Generate dynamic coaching suggestions based on current metrics"""
    suggestions = []
    
    # Priority suggestions based on current data
    if stress > 5:
        suggestions.append({
            'icon': '🧘',
            'title': 'Try Box Breathing',
            'desc': 'Inhale 4s, hold 4s, exhale 4s, hold 4s',
            'priority': 'high'
        })
    
    if posture < 60:
        suggestions.append({
            'icon': '🪑',
            'title': 'Adjust Your Chair',
            'desc': 'Ensure lumbar support is properly positioned',
            'priority': 'high'
        })
    
    # General suggestions
    suggestions.extend([
        {'icon': '🚶', 'title': 'Take a Walk', 'desc': 'Stand up every 30 minutes', 'priority': 'normal'},
        {'icon': '👀', 'title': 'Eye Rest', 'desc': 'Look at something 20ft away for 20 seconds', 'priority': 'normal'},
        {'icon': '💧', 'title': 'Stay Hydrated', 'desc': 'Drink water regularly', 'priority': 'normal'}
    ])
    
    return [
        html.Div([
            html.Div([
                html.Span(s['icon'], style={'fontSize': '1.5rem', 'marginRight': '12px'}),
                html.Div([
                    html.Strong(s['title']),
                    html.Br(),
                    html.Small(s['desc'], className="text-muted")
                ])
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={
            'padding': '10px 12px',
            'borderLeft': f"3px solid {'#ef4444' if s.get('priority') == 'high' else '#6366f1'}",
            'marginBottom': '8px',
            'background': 'rgba(255,255,255,0.03)',
            'borderRadius': '0 8px 8px 0'
        }) for s in suggestions[:4]  # Limit to 4 suggestions
    ]
