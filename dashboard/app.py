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

# Initialize app
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server

# Professional Header
def create_header():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1("NeuroChair Analytics", className="dashboard-title"),
                html.P("Real-time Posture & Wellness Monitoring", className="dashboard-subtitle")
            ], width="auto"),
            dbc.Col([
                html.Div([
                    html.Span(className="status-dot"),
                    html.Span("Live")
                ], className="status-indicator")
            ], width="auto", className="ms-auto d-flex align-items-center")
        ], className="align-items-center")
    ], className="dashboard-header")

# Tab configuration
TABS = [
    {"label": "User Dashboard", "tab_id": "end-user"},
    {"label": "Clinical View", "tab_id": "therapist"},
    {"label": "Alerts", "tab_id": "emergency"},
    {"label": "Analytics", "tab_id": "employer"},
]

# Layout
app.layout = dbc.Container([
    create_header(),
    
    dbc.Tabs(
        [dbc.Tab(label=tab["label"], tab_id=tab["tab_id"]) for tab in TABS],
        id="tabs",
        active_tab="end-user"
    ),
    
    html.Div(id="tab-content", className="mt-3"),
    
    html.Div([
        html.Small([
            "NeuroChair Analytics • Last updated: ",
            html.Span(id="current-time")
        ])
    ], className="dashboard-footer"),
    
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
], fluid=True, className="p-3")

@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "end-user":
        return render_end_user_tab()
    elif active_tab == "therapist":
        return render_therapist_tab()
    elif active_tab == "emergency":
        return render_emergency_tab()
    elif active_tab == "employer":
        return render_employer_tab()
    return html.P("Tab not found")

@app.callback(Output("current-time", "children"), Input("interval-component", "n_intervals"))
def update_time(n):
    return datetime.now().strftime("%H:%M:%S")

register_end_user_callbacks(app)
register_therapist_callbacks(app)
register_emergency_callbacks(app)
register_employer_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
