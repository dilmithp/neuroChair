import dash
from dash import dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import datetime

# Import components
from components.end_user_tab import render_end_user_tab, register_end_user_callbacks
from components.therapist_tab import render_therapist_tab, register_therapist_callbacks
from components.emergency_tab import render_emergency_tab, register_emergency_callbacks
from components.employer_tab import render_employer_tab, register_employer_callbacks

# Initialize app with Bootstrap theme + custom CSS
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server

# Professional Header Component
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
                ], className="status-indicator"),
                dbc.Button("Logout", id="logout-btn", color="link", size="sm", className="ms-3 text-muted", style={'textDecoration': 'none'})
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

# Login Layout
login_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H2("NeuroChair", className="text-center mb-4", style={'color': '#4e79a7', 'fontWeight': '600'}),
                        html.P("Please sign in to continue", className="text-center text-muted mb-4"),
                        
                        dbc.Label("Username"),
                        dbc.Input(id="username-box", type="text", placeholder="Enter username", className="mb-3"),
                        
                        dbc.Label("Password"),
                        dbc.Input(id="password-box", type="password", placeholder="Enter password", className="mb-3"),
                        
                        dbc.Button("Login", id="login-btn", color="primary", className="w-100"),
                        html.Div(id="login-alert", className="mt-3"),
                        # Hidden logout button to prevent callback errors
                        dbc.Button(id="logout-btn", style={"display": "none"})
                    ])
                ])
            ], className="shadow-sm border-0", style={'maxWidth': '400px', 'margin': '0 auto'})
        ], width=12, className="d-flex align-items-center justify-content-center", style={'minHeight': '100vh'})
    ])
], fluid=True, style={'background': '#f3f3f3'})

# Main Dashboard Layout
def dashboard_layout():
    return dbc.Container([
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
        
        # Hidden login button to prevent callback errors on dashboard page
        dbc.Button(id="login-btn", style={"display": "none"}),
        html.Div(id="login-alert", style={"display": "none"}),
        # Hidden inputs for callback state
        dbc.Input(id="username-box", style={"display": "none"}),
        dbc.Input(id="password-box", style={"display": "none"}),
        
        dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
    ], fluid=True, className="p-3")

# App Root Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', storage_type='session'),  # Stores user session
    html.Div(id='page-content')
])

# Callbacks
@app.callback(
    [Output('url', 'pathname'), Output('session-store', 'data'), Output('login-alert', 'children')],
    [Input('login-btn', 'n_clicks'), Input('logout-btn', 'n_clicks')],
    [State('username-box', 'value'), State('password-box', 'value'), State('url', 'pathname')],
    prevent_initial_call=True
)
def manage_login(login_clicks, logout_clicks, username, password, current_path):
    ctx = callback_context
    if not ctx.triggered:
        return current_path, dash.no_update, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'login-btn':
        if username == 'U01' and password == '1234':  # Hardcoded Demo User
            return '/dashboard', {'user': 'U01', 'role': 'user'}, ""
        else:
            return dash.no_update, dash.no_update, dbc.Alert("Invalid credentials", color="danger")
            
    elif button_id == 'logout-btn':
        return '/login', None, ""
    
    return current_path, dash.no_update, ""

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname'), Input('session-store', 'data')])
def display_page(pathname, session_data):
    if session_data and session_data.get('user'):
        if pathname == '/login':
            return dashboard_layout() # Redirect to dashboard if logged in
        return dashboard_layout()
    else:
        return login_layout

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

# Register callbacks for all tabs
register_end_user_callbacks(app)
register_therapist_callbacks(app)
register_emergency_callbacks(app)
register_employer_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
