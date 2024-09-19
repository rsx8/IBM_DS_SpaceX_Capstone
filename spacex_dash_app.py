# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

print(f"min payload is: {min_payload} and max payload is: {max_payload}")

# Create a dash application
app = dash.Dash(__name__)

dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]
for i in spacex_df['Launch Site'].unique():
    dropdown_options.append({'label': i, 'value': i})
#dropdown_options.append([{'label': i, 'value': i} for i in spacex_df['Launch Site'].unique()])
#dropdown_options.append({'label': 'All Sites', 'value': 'ALL'})
print(dropdown_options)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=dropdown_options, 
                                    #multi=True,
                                    searchable=True,
                                    placeholder='Select a Launch Site'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    #marks={0: '0', 100: '100'}
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
                Input(component_id='site-dropdown',component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Total Success Launches By Site')
    elif entered_site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        fig = px.pie(filtered_df,
        names='class',
        title='Total Success for site CCAFS LC-40')
    elif entered_site == 'VAFB SLC-4E':
        filtered_df = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        fig = px.pie(filtered_df,
        names='class',
        title='Total Success for site VAFB SLC-4E')
    elif entered_site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        fig = px.pie(filtered_df,
        names='class',
        title='Total Success for site KSC LC-39A')
    elif entered_site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        fig = px.pie(filtered_df,
        names='class',
        title='Total Success for site CCAFS SLC-40')  
    else:
        #return all as default
        filtered_df = spacex_df[spacex_df['class']==1]
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Total Success Launches By Site')
    return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site,payload_values):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_values[0], payload_values[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites')
    elif entered_site == 'CCAFS LC-40':
        filtered_df = filtered_df[filtered_df['Launch Site']=='CCAFS LC-40']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for Launch Site CCAFS LC-40')
    elif entered_site == 'VAFB SLC-4E':
        filtered_df = filtered_df[filtered_df['Launch Site']=='VAFB SLC-4E']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for Launch Site VAFB SLC-4E')
    elif entered_site == 'KSC LC-39A':
        filtered_df = filtered_df[filtered_df['Launch Site']=='KSC LC-39A']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for Launch Site KSC LC-39A')
    elif entered_site == 'CCAFS SLC-40':
        filtered_df = filtered_df[filtered_df['Launch Site']=='CCAFS SLC-40']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for Launch Site CCAFS SLC-40')
    else:
        #Default to All
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites')
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
