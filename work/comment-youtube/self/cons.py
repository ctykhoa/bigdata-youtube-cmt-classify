from kafka import KafkaConsumer
import json
import pandas as pd
import dash
from dash import Dash, Input, Output, callback, dash_table
from dash import dcc
import plotly.express as px
import mysql.connector
from dash import html
import dash_bootstrap_components as dbc

from sqlalchemy import create_engine, text

sqlEngine = create_engine('mysql+pymysql://cons:pass@mysql/final_project?autocommit=true')
conn = sqlEngine.connect()

consumer = KafkaConsumer('youtube_comments', bootstrap_servers='kafka:9092', value_deserializer=lambda v: json.loads(v))

# for message in consumer:
#     print (message.value)



# Connect to the mysql database
# conn = mysql.connector.connect(
#           host ="mysql",
#           user ="root",
#           passwd ="password",
#           database = "final_project"
#         )

# Retrieve data from the materialized view using pandas
commentQueryText = "SELECT VIDEOs.videoTitle , COMMENTS.commentText, COMMENTS.publishedAt, CASE when isToxic = 1 then 'Yes' else 'No' END as isToxicComment FROM COMMENTS JOIN VIDEOs on comments.videoId = videos.videoId ORDER BY publishedAt DESC"
 # LIMIT 10"
df = pd.read_sql(text(commentQueryText), conn)
# df['isToxicComment'] = 'Yes' if df['isToxic'] == 1 else 'No'

# Create a Dash application
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
app = dash.Dash(__name__)
# Define layout
app.layout = html.Div(
    className="container",children=[
    html.H1("Video comments"),
    dash_table.DataTable(
        id="youtube_video_comments_tbl",
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_cell={
            'maxWidth': '300px',
            'whiteSpace': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        }),
    dbc.Alert(id='youtube_video_comments_tbl_out'),
    dcc.Interval(
        id='interval_component',
        interval=1*60000, # in milliseconds
        n_intervals=0
    ),
    html.H1("Video comments Graph"),
    dcc.Graph(
        id="youtube_video_comments_graph",
        figure = px.histogram(df, x="videoTitle", y="commentText", color="isToxicComment", barmode="group", histfunc='count')
    )
])

@callback(Output('youtube_video_comments_tbl_out', 'children'), Input('youtube_video_comments_tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else ""


@app.callback(Output(component_id='youtube_video_comments_tbl', component_property='data'),
            [Input(component_id='interval_component', component_property='n_intervals')])
def update_table(n):
    df = pd.read_sql(text(commentQueryText), conn)
    return df.to_dict("records")

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port="8945")
