import os
from job import Job
import streamlit as st
import pandas as pd
import numpy as np
import time  # to simulate a real time data, time loop

import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts

# thread to store comments to db
myJob = Job()

st.title('Classifying Comments')
st.markdown('Comment model to play to classify Comments into \
toxic or non-toxic')

st.header("Comment Features")
col1, col2 = st.columns(2)
with col1:
    cmt_text = st.text_input('Comment in text')

if st.button("Classify comment"):
    result = myJob.get_prediction(cmt_text)
    st.text("Toxic" if result.collect()[0][1] == 1.0 else "Non-toxic")


def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
    'Classification': ['Toxic', 'Non-toxic'],
    'Number of comments': ( len(df[(df['isToxic']>0)]), len(df[(df['isToxic']<=0)]))
    })
    return total_dataframe


select_status = st.sidebar.radio("Classification", ('Toxic',
'Non-toxic'))

while True:
    myJob.insertNewCommentFromTopVideos()
    df = myJob.getCommentsFromDb()

    select = st.sidebar.selectbox('Select a Video', df['videoId'].unique())
    #get the state selected in the selectbox
    video_data = df[df['videoId'] == select]

    video_total = get_total_dataframe(video_data)

    st.markdown("## **Comment analysis**")
    st.markdown("### Overall Toxic, non-toxic in video %s yet" % (select))
    video_total_graph = px.bar(
                video_total,
                x='Classification',
                y='Number of comments',
                labels={'Number of comments':'Number of comments in video %s' % (select)},
                color='Classification')
    st.plotly_chart(video_total_graph)
    time.sleep(10)
