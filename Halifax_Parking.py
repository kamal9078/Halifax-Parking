import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Accessible Parking Spots"
server = app.server


# Initialize data frame
df = pd.read_csv("Accessible_Parking_Spots.csv")

df = df.dropna(axis=0, subset=['ADJSURFMAT'])
df = df.reset_index()
df['ADJSURFMAT'] = df['ADJSURFMAT'].astype(str)


dict1= {}
for i, j in zip(df['STREET_NAME'],df['STREET_NAME']):
    dict1[i] = j

options=[{'label': i, 'value': j} for i, j in zip(dict1.keys(), dict1.values())]


# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.png")
                        ),
                        html.H2("ACCESSIBLE PARKING SPOTS"),
                        html.P(
                            """Select streets to loacte the parking spots."""
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="streets",
                                            options=options,
                                            placeholder="Select a street",
                                            search_value="BARRINGTON ST",
                                            value=["BARRINGTON ST", "CHARLES ST"],
                                            multi=True,
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                "Source: [OpenDataHalifax](https://catalogue-hrm.opendata.arcgis.com/datasets/90be8d1040e54793a29a80d1f94d942e_0/explore?showTable=true)"
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                    ],
                ),
            ],
        )
    ]
)


@app.callback(
        [Output('streets', 'options')],
        [Input('streets', 'search_value'),
         Input('streets','value')]

)
def update_options(search_value,val):
    return [i for i in options if search_value in i['label']],


@app.callback(
        [Output('map-graph', 'figure')],
        [Input('streets', 'value')]

)
def update_points(search_value):
    df2 = df[(df['STREET_NAME'].isin(search_value))]

    df2['COMMENTS'] = df2['FROM_STR'] + ', ' + df2['TO_STR'] + ', ' + df2['STREET_NAME'] + '' + ' Number of Spots: ' + df2['NUMSPOTS'].astype(str)

    fig = px.scatter_mapbox(df2, lat=df2['Y'], lon=df2['X'], hover_name=df2['COMMENTS'], color=df2['ADJSURFMAT'],
                            color_discrete_map={"CONCRETE": "gray", "GRASS": "green", "CONGRAS": "blue",
                                                "GRAVEL": "black"}, zoom=12, height=750)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig,


def update_map(search_value):
    df2 = df[df['STREET_NAME'] == search_value]

    df2['COMMENTS'] = df2['FROM_STR'] + '' + df2['TO_STR'] + ', ' + df2['STREET_NAME'] + '' + ' Number of Spots: ' + df2['NUMSPOTS'].astype(str)

    fig = go.Figure(data=go.Scattergeo(
        lon=df2['X'],
        lat=df2['Y'],
        text=df2['COMMENTS'],
        mode='markers',
        marker_color=df2['ADJSURFMAT'],
    ))

    fig.update_layout(
        title='Accessible Parking Spots',
        geo_scope='north america',
    )

    return fig,


if __name__ == "__main__":
    app.run_server(debug=True)