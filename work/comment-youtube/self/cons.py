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

   # dash.exceptions.invalidcallbackreturnvalue: The callback for `<Output `youtube_video_comments_tbl.data`>` returned a value having type
    #`DataFrame` which is not JSON serializable. The value in question is either the only value returned,
     #or is in the top level of the returned list, and has string representation
     #` commentId videoId ... AddedToDbdAt videoTitle 0 Ugw-iY32u8oNbyqmjt14AaABAg b_rpj_nMWBI ... 2023-10-22 09:33:50 Lil Mabu x ChriseanRock - MR. TAKE YA B*TCH (O... 1 Ugw0UYEgBniITnSzIgp4AaABAg 83Lv790h79k ... 2023-10-21 15:55:13 The Kid LAROI, Jung Kook, Central Cee - TOO MU... 2 Ugw11y6C652TmkPfWEV4AaABAg b_rpj_nMWBI ... 2023-10-21 15:15:43 Lil Mabu x ChriseanRock - MR. TAKE YA B*TCH (O... 3 Ugw2r4CbtbOQJW6-Hfl4AaABAg qWL7Iy7jhKc ... 2023-10-21 15:55:13 BAD BUNNY - NADIE SABE (Visualizer) | nadie s... 4 Ugw35UG9ce2DZlkkA1d4AaABAg _PJvpq8uOZM ... 2023-10-21 15:15:43 BAD BUNNY - MONACO (Official Video) | nadie sa... .. ... ... ... ... ... 120 UgzlqPUAKc3C6XbZgBd4AaABAg 83Lv790h79k ... 2023-10-21 15:21:37 The Kid LAROI, Jung Kook, Central Cee - TOO MU... 121 UgzMoou3YBtc002YpIB4AaABAg 83Lv790h79k ... 2023-10-21 15:15:43 The Kid LAROI, Jung Kook, Central Cee - TOO MU... 122 UgzmtA6DADrPyRyfU054AaABAg 83Lv790h79k ... 2023-10-21 15:21:37 The Kid LAROI, Jung Kook, Central Cee - TOO MU... 123 Ugzs0wBKaMpGAAVB0Wl4AaABAg 83Lv790h79k ... 2023-10-22 09:36:58 The Kid LAROI, Jung Kook, Central Cee - TOO MU..
