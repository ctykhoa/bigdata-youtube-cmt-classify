import mysql.connector
import pandas as pd

class db:
    def __init__(self):
        try:
            print("connecting db")
            self.connect()
        except:
            print("init db")
            self.dataBase = mysql.connector.connect(
              host ="mysql",
              user ="root",
              passwd ="password"
            )

            self.cursor = self.dataBase.cursor()
            # creating database
            self.cursor.execute("CREATE DATABASE final_project")

            # creating table
            self.dataBase.database  = "final_project"

            commentRecord = """CREATE TABLE comments (
                               commentId  VARCHAR(30) PRIMARY KEY NOT NULL,
                               videoId VARCHAR(30),
                               commentText TEXT,
                               isToxic INT,
                               publishedAt TIMESTAMP DEFAULT NOW(),
                               AddedToDbdAt TIMESTAMP DEFAULT NOW()
                               )"""
            videoRecord = """CREATE TABLE videos (
                               videoId VARCHAR(30) PRIMARY KEY NOT NULL,
                               videoTitle TEXT,
                               currentRank INT,
                               predictedRank INT,
                               publishedAt TIMESTAMP DEFAULT NOW(),
                               AddedToDbdAt TIMESTAMP DEFAULT NOW()
                               )"""

            # table created
            self.cursor.execute(commentRecord)
            self.cursor.execute(videoRecord)
            self.cursor.execute("SET NAMES 'UTF8MB4'")
            self.cursor.execute("SET CHARACTER SET UTF8MB4")

    def connect(self):
        self.dataBase = mysql.connector.connect(
          host ="mysql",
          user ="root",
          passwd ="password",
          database = "final_project"
        )

        try:
            self.cursor = self.dataBase.cursor()
            self.cursor.execute("SET NAMES 'UTF8MB4'")
            self.cursor.execute("SET CHARACTER SET UTF8MB4")
        except Exception as e:
            raise Exception(e)

    def insertVideos(self, videos):
        sql = "INSERT IGNORE INTO videos (videoId, videoTitle, publishedAt)\
        VALUES (%s, %s, %s)"
        self.cursor.executemany(sql, videos)
        self.dataBase.commit()

    def insertComments(self, commentObjects):
        sql = "INSERT INTO comments (commentId, videoId, commentText, publishedAt, IsToxic)\
        VALUES (%s, %s, %s, %s, %s)"
        self.cursor.executemany(sql, commentObjects)
        self.dataBase.commit()

    def test(self):
#         cursor = self.dataBase.cursor()
        self.cursor.execute("SELECT * from comments")
        results = self.cursor.fetchall()
        for x in results:
            print(x)

    def getTop5VideoIdsFromDb(self):
        videoIds = []
        self.cursor.execute("SELECT videoId from videos")
        results = self.cursor.fetchall()
        for row in results:
            videoIds.append(row[0])

        return videoIds

    def getLatestCommentTimestamp(self, videoId):
        timestamp = self.cursor.execute("SELECT publishedAt FROM comments WHERE videoId = %s ORDER BY publishedAt DESC LIMIT 1", (videoId,))
        rows = self.cursor.fetchall()

        try:
            return rows[0][0]
        except:
            return None

    def readCommentPandas(self):
        return pd.read_sql("SELECT comments.*, videos.videoTitle FROM COMMENTS JOIN VIDEOs on comments.videoId = videos.videoId", self.dataBase)