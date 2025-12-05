from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np

# Chart template for dark theme
CHART_TEMPLATE = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#f1f5f9', 'family': 'Inter'},
    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40}
}

def render_employer_tab():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4([
                        html.Span("📊", style={'marginRight': '10px'}),
                        "Workplace Wellness Analytics"
                    ], className="mb-1"),
                    html.Small([
                        html.Span("🔒", style={'marginRight': '6px'}),
                        "All data is anonymized and aggregated for privacy compliance"
                    ], className="text-muted")
                ])
            ], lg=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("7D", id="btn-7d", color="primary", outline=True, size="sm"),
                    dbc.Button("30D", id="btn-30d", color="primary", size="sm"),
                    dbc.Button("90D", id="btn-90d", color="primary", outline=True, size="sm"),
                ], className="float-end")
            ], lg=4, className="d-flex align-items-center justify-content-end")
        ], className="mb-4 align-items-center"),
        
        # Executive KPI Cards
        dbc.Row([
            dbc.Col([
                create_kpi_card("Wellness Score", "78", "/100", "↑ 5%", "positive", "🎯")
            ], lg=3, md=6, className="mb-4"),
            dbc.Col([
                create_kpi_card("Avg Stress Level", "5.2", "/10", "↓ 8%", "positive", "😌")
            ], lg=3, md=6, className="mb-4"),
            dbc.Col([
                create_kpi_card("Good Posture Rate", "65", "%", "↑ 12%", "positive", "🧘")
            ], lg=3, md=6, className="mb-4"),
            dbc.Col([
                create_kpi_card("Active Users", "54", "", "of 60", "neutral", "👥")
            ], lg=3, md=6, className="mb-4"),
        ]),

        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📈", style={'fontSize': '1.1rem'}),
                        " Organization Stress Index",
                        dbc.Badge("Real-time", color="success", className="ms-auto")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='org-stress-gauge', style={'height': '220px'},
                                 config={'displayModeBar': False})
                    ])
                ], className="h-100")
            ], lg=4, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📊", style={'fontSize': '1.1rem'}),
                        " Posture Trends (30 Days)"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='org-posture-trend', style={'height': '220px'},
                                 config={'displayModeBar': False})
                    ])
                ], className="h-100")
            ], lg=8, className="mb-4"),
        ]),

        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("⏰", style={'fontSize': '1.1rem'}),
                        " Stress by Hour of Day"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='stress-by-hour', style={'height': '250px'},
                                 config={'displayModeBar': False})
                    ])
                ], className="h-100")
            ], lg=6, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🪑", style={'fontSize': '1.1rem'}),
                        " Sitting Duration vs Posture"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='prod-posture-scatter', style={'height': '250px'},
                                 config={'displayModeBar': False})
                    ])
                ], className="h-100")
            ], lg=6, className="mb-4"),
        ]),

        # Charts Row 3
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🏢", style={'fontSize': '1.1rem'}),
                        " Department Comparison"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='team-comparison', style={'height': '280px'},
                                 config={'displayModeBar': False})
                    ])
                ], className="h-100")
            ], lg=7, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📋", style={'fontSize': '1.1rem'}),
                        " Executive Summary"
                    ]),
                    dbc.CardBody([
                        html.Div(id='wellness-summary-stats')
                    ])
                ], className="h-100")
            ], lg=5, className="mb-4"),
        ])
    ], fluid=True, className="p-3 animate-fade-in")

def create_kpi_card(title, value, suffix, trend, trend_type, icon):
    trend_colors = {
        'positive': {'bg': 'rgba(16, 185, 129, 0.15)', 'color': '#10b981'},
        'negative': {'bg': 'rgba(239, 68, 68, 0.15)', 'color': '#ef4444'},
        'neutral': {'bg': 'rgba(148, 163, 184, 0.15)', 'color': '#94a3b8'}
    }
    style = trend_colors.get(trend_type, trend_colors['neutral'])
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Span(icon, style={'fontSize': '2rem'}),
            ], className="mb-2"),
            html.Div([
                html.Span(value, style={
                    'fontSize': '2.5rem', 'fontWeight': '700',
                    'background': 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                    '-webkit-background-clip': 'text',
                    '-webkit-text-fill-color': 'transparent'
                }),
                html.Span(suffix, style={'fontSize': '1rem', 'color': '#64748b', 'marginLeft': '4px'})
            ]),
            html.Small(title, className="text-muted d-block mb-2"),
            html.Span(trend, style={
                'background': style['bg'],
                'color': style['color'],
                'padding': '4px 10px',
                'borderRadius': '12px',
                'fontSize': '0.8rem',
                'fontWeight': '500'
            })
        ], className="text-center")
    ], style={'background': 'rgba(255,255,255,0.03)', 'border': '1px solid rgba(255,255,255,0.08)'})

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
        # 1. Organization Stress Gauge
        avg_stress = 5.2
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_stress,
            delta={'reference': 5.8, 'decreasing': {'color': '#10b981'}},
            number={'font': {'size': 48, 'color': '#f1f5f9'}, 'suffix': '/10'},
            gauge={
                'axis': {'range': [0, 10], 'tickcolor': '#64748b'},
                'bar': {'color': '#f59e0b', 'thickness': 0.75},
                'bgcolor': 'rgba(255,255,255,0.05)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 3], 'color': 'rgba(16, 185, 129, 0.2)'},
                    {'range': [3, 7], 'color': 'rgba(245, 158, 11, 0.2)'},
                    {'range': [7, 10], 'color': 'rgba(239, 68, 68, 0.2)'}
                ],
            }
        ))
        gauge_fig.update_layout(**CHART_TEMPLATE)

        # 2. Posture Trend
        dates = pd.date_range(end=pd.Timestamp.now(), periods=30).tolist()
        posture_scores = np.linspace(60, 75, 30) + np.random.normal(0, 3, 30)
        
        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(
            x=dates, y=posture_scores,
            mode='lines',
            line={'color': '#6366f1', 'width': 3},
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.1)',
            name='Posture Score'
        ))
        trend_fig.add_hline(y=70, line_dash="dash", line_color="#10b981", 
                          annotation_text="Target", annotation_font_color="#10b981")
        trend_fig.update_layout(**CHART_TEMPLATE, 
                               yaxis={'range': [40, 100], 'gridcolor': 'rgba(255,255,255,0.05)'},
                               xaxis={'gridcolor': 'rgba(255,255,255,0.05)'},
                               showlegend=False)

        # 3. Scatter Plot
        n_points = 50
        sitting_hours = np.random.uniform(2, 9, n_points)
        posture_vals = 100 - (sitting_hours * 5) + np.random.normal(0, 8, n_points)
        
        scatter_fig = go.Figure()
        scatter_fig.add_trace(go.Scatter(
            x=sitting_hours, y=posture_vals,
            mode='markers',
            marker={
                'color': sitting_hours,
                'colorscale': [[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
                'size': 10,
                'line': {'color': 'white', 'width': 1}
            },
            name='Employees'
        ))
        scatter_fig.update_layout(**CHART_TEMPLATE,
                                 xaxis={'title': 'Sitting Hours', 'gridcolor': 'rgba(255,255,255,0.05)'},
                                 yaxis={'title': 'Posture Score', 'gridcolor': 'rgba(255,255,255,0.05)'},
                                 showlegend=False)

        # 4. Stress by Hour
        hours = list(range(9, 19))
        stress_hourly = [3.2, 4.1, 5.2, 6.1, 5.8, 4.2, 3.5, 4.8, 5.9, 6.5]
        colors = ['#10b981' if s < 4 else '#f59e0b' if s < 6 else '#ef4444' for s in stress_hourly]
        
        bar_fig = go.Figure()
        bar_fig.add_trace(go.Bar(
            x=[f"{h}:00" for h in hours], 
            y=stress_hourly,
            marker={'color': colors, 'line': {'color': 'rgba(255,255,255,0.2)', 'width': 1}},
            text=[f'{s:.1f}' for s in stress_hourly],
            textposition='outside',
            textfont={'color': '#94a3b8', 'size': 10}
        ))
        bar_fig.update_layout(**CHART_TEMPLATE,
                             yaxis={'range': [0, 8], 'gridcolor': 'rgba(255,255,255,0.05)'},
                             xaxis={'gridcolor': 'rgba(255,255,255,0.05)'},
                             showlegend=False)

        # 5. Team Comparison
        teams = ['Engineering', 'Sales', 'HR', 'Marketing', 'Finance']
        wellness_scores = [72, 65, 85, 78, 70]
        colors = ['#6366f1', '#8b5cf6', '#10b981', '#06b6d4', '#f59e0b']
        
        team_fig = go.Figure()
        team_fig.add_trace(go.Bar(
            x=teams, y=wellness_scores,
            marker={'color': colors, 'line': {'color': 'rgba(255,255,255,0.2)', 'width': 2}},
            text=[f'{s}%' for s in wellness_scores],
            textposition='outside',
            textfont={'color': '#f1f5f9', 'size': 12, 'family': 'Inter'}
        ))
        team_fig.add_hline(y=75, line_dash="dash", line_color="#10b981", 
                          annotation_text="Company Goal", annotation_font_color="#10b981")
        team_fig.update_layout(**CHART_TEMPLATE,
                              yaxis={'range': [0, 100], 'title': 'Wellness Score', 
                                    'gridcolor': 'rgba(255,255,255,0.05)'},
                              xaxis={'gridcolor': 'rgba(255,255,255,0.05)'},
                              showlegend=False)

        # 6. Executive Summary
        summary = html.Div([
            # Key Insights
            html.Div([
                html.H6([
                    html.Span("💡", style={'marginRight': '8px'}),
                    "Key Insights"
                ], className="mb-3"),
                create_insight_item("🏆", "HR department leads wellness metrics", "positive"),
                create_insight_item("⚠️", "Sales team needs intervention", "warning"),
                create_insight_item("📈", "Overall improvement of 12% this month", "positive"),
            ], className="mb-4"),
            
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.1)'}),
            
            # Recommendations
            html.Div([
                html.H6([
                    html.Span("🎯", style={'marginRight': '8px'}),
                    "Recommendations"
                ], className="mb-3"),
                html.Ul([
                    html.Li("Schedule ergonomic assessments for Sales", style={'marginBottom': '8px'}),
                    html.Li("Implement break reminders company-wide", style={'marginBottom': '8px'}),
                    html.Li("Consider standing desk pilot program", style={'marginBottom': '8px'})
                ], style={'paddingLeft': '20px', 'color': '#94a3b8'})
            ])
        ])
        
        return gauge_fig, trend_fig, scatter_fig, bar_fig, team_fig, summary

def create_insight_item(icon, text, status):
    colors = {'positive': '#10b981', 'warning': '#f59e0b', 'negative': '#ef4444'}
    bgs = {'positive': 'rgba(16, 185, 129, 0.1)', 'warning': 'rgba(245, 158, 11, 0.1)', 
           'negative': 'rgba(239, 68, 68, 0.1)'}
    
    return html.Div([
        html.Span(icon, style={'marginRight': '10px'}),
        html.Span(text, style={'color': '#f1f5f9'})
    ], style={
        'padding': '10px 12px',
        'background': bgs.get(status, 'rgba(255,255,255,0.05)'),
        'borderLeft': f"3px solid {colors.get(status, '#64748b')}",
        'borderRadius': '0 8px 8px 0',
        'marginBottom': '8px'
    })
