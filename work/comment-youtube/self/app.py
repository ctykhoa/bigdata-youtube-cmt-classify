import os
from job import Job

# get videos and save db every 5 min
myJob = Job()
#
# ## get comments of each video + predict --> save to db
myJob.insertNewCommentFromTopVideos()

### kafka producer -> send comment [video-id, comment-id, comment-text, prediction] to kafka topic "youtube_comments"

#### another webserver use kafka consumer get data and display to dashboard, chart
