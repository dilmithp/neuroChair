import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import components
from components.end_user_tab import render_end_user_tab, register_end_user_callbacks
from components.therapist_tab import render_therapist_tab, register_therapist_callbacks
from components.emergency_tab import render_emergency_tab, register_emergency_callbacks
from components.employer_tab import render_employer_tab, register_employer_callbacks

# Initialize app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Main layout with tabs
app.layout = dbc.Container([
    html.H1("NeuroChair Dashboard", className="text-center my-4"),
    
    dbc.Tabs([
        dbc.Tab(label="👤 End User", tab_id="end-user"),
        dbc.Tab(label="⚕️ Therapist", tab_id="therapist"),
        dbc.Tab(label="🚨 Emergency", tab_id="emergency"),
        dbc.Tab(label="📊 Employer", tab_id="employer"),
    ], id="tabs", active_tab="end-user"),
    
    html.Div(id="tab-content", className="mt-4"),
    
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
], fluid=True)

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

# Register callbacks for all tabs
register_end_user_callbacks(app)
register_therapist_callbacks(app)
register_emergency_callbacks(app)
register_employer_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
