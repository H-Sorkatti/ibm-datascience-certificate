# coding: utf-8

# In[2]:


# Import required libraries
import pandas as pd
import dash
import dash_html_components as html  # deprecated, replace with dash.html

# from dash import html
import dash_core_components as dcc  # deprecated, replace with dash.dcc

# from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# In[3]:


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")


# In[18]:


max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

launch_sites = spacex_df["Launch Site"].unique().tolist()


# In[5]:


# Create a dash application
app = dash.Dash(__name__)


# In[43]:


# Create an app layout
app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        # "alignItems": "center",
        "justifyContent": "start",
        "width": "80%",
    },
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Launch Sites", "value": "All"}]
            + [{"label": site, "value": site} for site in launch_sites],
            value="All",
            placeholder="All Launch Sites",
            searchable=False,
            style={"width": "400px"},
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=min_payload,
            max=max_payload,
            step=1000,
            # marks={0: "0", 100: "100"},
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ],
)


# In[41]:


# TASK 2:
# Add a callback function for `site-dropdown` as ireturn fignput, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(selected_site):
    if selected_site == "All":
        data = spacex_df.groupby("class")[["class"]].count()
        fig = px.pie(data, values="class", names=['0', '1'], title=selected_site)
        return fig
    else:
        data = (
            spacex_df[spacex_df["Launch Site"] == selected_site]
            .groupby("class")[["Launch Site"]]
            .count()
            .reset_index()
        )
        fig = px.pie(data, values="Launch Site", names="class", title=selected_site)
        return fig


# In[47]:


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs,
# `success-payload-scatter-chart` as output


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def payload_scatter(site, slider):
    if site == "All":
        data = spacex_df[
            (spacex_df["Payload Mass (kg)"] >= slider[0])
            & (spacex_df["Payload Mass (kg)"] <= slider[1])
        ]
        fig = px.scatter(
            data, x="Payload Mass (kg)", y="class", color="Booster Version", 
            size='Payload Mass (kg)',
            title=f'Scatter plot of {site}'
        )
        return fig
    else:
        data = spacex_df[
            (spacex_df["Payload Mass (kg)"] >= slider[0])
            & (spacex_df["Payload Mass (kg)"] <= slider[1])
        ]
        data = data[data['Launch Site'] == site]
        fig = px.scatter(
            data, x="Payload Mass (kg)", y="class", color="Booster Version",
            size='Payload Mass (kg)',
            title=f'Scatter plot of {site}'
        )
        return fig


# In[ ]:


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
