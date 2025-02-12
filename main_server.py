import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import pandas as pd

# Load sample data
df = px.data.gapminder()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with inputs
app.layout = html.Div([
    html.H1("Interactive Dashboard with Inputs"),
    
    # Numeric Input
    html.Label("Enter a minimum life expectancy:"),
    dcc.Input(id="life-exp-input", type="number", value=50, step=1),
    
    # Dropdown Input
    html.Label("Select a Continent:"),
    dcc.Dropdown(
        id="continent-dropdown",
        options=[{"label": c, "value": c} for c in df["continent"].unique()],
        value="Asia",
        clearable=False
    ),
    
    # Output Graph
    dcc.Graph(id="scatter-plot"),
])

# Callback to update graph based on inputs
@app.callback(
    Output("scatter-plot", "figure"),
    Input("life-exp-input", "value"),
    Input("continent-dropdown", "value"),
)
def update_graph(min_life_exp, selected_continent):
    filtered_df = df[(df["year"] == 2007) & 
                     (df["lifeExp"] >= min_life_exp) & 
                     (df["continent"] == selected_continent)]
    
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", size="pop", 
                     hover_name="country", log_x=True, size_max=60,
                     title=f"Countries in {selected_continent} with Life Expectancy ≥ {min_life_exp}")
    
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

