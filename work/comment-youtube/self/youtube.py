import time
from datetime import datetime
from googleapiclient.discovery import build

class Youtube:
    def __init__(self):
        # Get credentials
        DEVELOPER_KEY = ''
        if not DEVELOPER_KEY:
            print("insert key")
        else:
            # # Create YouTube API client
            self.youtube = build('youtube', 'v3', developerKey = DEVELOPER_KEY)

    def getTop5MusicTrendingVideos(self):
        # Cats query
        top5TrendingMusicVideos = self.youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode="US",
            videoCategoryId="10",
            maxResults=5
        ).execute()

        videos = []
        for trendingVideo in top5TrendingMusicVideos['items']:
            print(trendingVideo['id'] + " " + trendingVideo['snippet']['title'])
            trendingVideo['snippet']['publishedAt'] = datetime.strptime(trendingVideo['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")

            video = (trendingVideo['id'], trendingVideo['snippet']['title'], trendingVideo['snippet']['publishedAt'])
            videos.append(video)

        return videos

    def getCommentsOfVideos(self, videoId):
        # get comment
        comments = self.youtube.commentThreads().list(
            part="snippet",
            order="time",
            textFormat="plainText",
            maxResults=5,
            videoId=videoId
        ).execute()

        results = []
        for item in comments['items']:
            publishedAt = datetime.strptime(item['snippet']['topLevelComment']['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_id = item['id']
            results.append((comment_text, publishedAt, comment_id))

        return results