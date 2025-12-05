import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import datetime

# Import components
from components.end_user_tab import render_end_user_tab, register_end_user_callbacks
from components.therapist_tab import render_therapist_tab, register_therapist_callbacks
from components.emergency_tab import render_emergency_tab, register_emergency_callbacks
from components.employer_tab import render_employer_tab, register_employer_callbacks

# Initialize app with Dark Bootstrap theme + custom CSS
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.DARKLY,
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
    ],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
server = app.server

# Professional Header Component
def create_header():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1([
                    "🪑 NeuroChair",
                    html.Span(" Dashboard", style={'fontWeight': '400'})
                ], className="mb-0"),
                html.P("Smart Posture & Wellness Monitoring System", className="subtitle mb-0 opacity-75")
            ], width="auto"),
            dbc.Col([
                html.Div([
                    html.Span(className="live-dot"),
                    html.Span("Live Monitoring")
                ], className="live-indicator")
            ], width="auto", className="ms-auto d-flex align-items-center")
        ], className="align-items-center")
    ], className="dashboard-header")

# Tab configuration with icons
TABS_CONFIG = [
    {"label": "👤 End User", "tab_id": "end-user", "icon": "👤"},
    {"label": "⚕️ Therapist", "tab_id": "therapist", "icon": "⚕️"},
    {"label": "🚨 Emergency", "tab_id": "emergency", "icon": "🚨"},
    {"label": "📊 Employer", "tab_id": "employer", "icon": "📊"},
]

# Main layout with professional styling
app.layout = dbc.Container([
    # Header
    create_header(),
    
    # Navigation Tabs
    dbc.Tabs(
        [dbc.Tab(label=tab["label"], tab_id=tab["tab_id"]) for tab in TABS_CONFIG],
        id="tabs",
        active_tab="end-user",
        className="mb-4"
    ),
    
    # Tab Content Area
    html.Div(id="tab-content", className="animate-fade-in"),
    
    # Footer
    html.Footer([
        html.Hr(style={'borderColor': 'rgba(255,255,255,0.1)', 'margin': '2rem 0 1rem'}),
        dbc.Row([
            dbc.Col([
                html.Small([
                    "© 2024 NeuroChair • ",
                    html.Span(id="current-time", className="text-muted")
                ])
            ], className="text-center text-muted")
        ])
    ]),
    
    # Interval for real-time updates
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
], fluid=True, className="py-4 px-4")

# Callback to switch tab content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "end-user":
        return render_end_user_tab()
    elif active_tab == "therapist":
        return render_therapist_tab()
    elif active_tab == "emergency":
        return render_emergency_tab()
    elif active_tab == "employer":
        return render_employer_tab()
    return html.P("This tab is not yet implemented.")

# Callback to update time
@app.callback(
    Output("current-time", "children"),
    Input("interval-component", "n_intervals")
)
def update_time(n):
    return datetime.now().strftime("%H:%M:%S")

# Register callbacks for all tabs
register_end_user_callbacks(app)
register_therapist_callbacks(app)
register_emergency_callbacks(app)
register_employer_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
