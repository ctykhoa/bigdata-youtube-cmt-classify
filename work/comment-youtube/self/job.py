from youtube import Youtube
from DB import db
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
#for text pre-processing
import re, string
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from pyspark.sql import Row
from pyspark.sql import SparkSession
import pandas as pd
from pyspark.ml.feature import StringIndexer, VectorIndexer, StringIndexerModel, IndexToString
from pyspark.ml.feature import VectorAssembler
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import json
from kafka import KafkaProducer
from model.comment import Comment

class Job:

    def __init__(self):
        self.myspark = SparkSession.builder.appName("FinalApp").getOrCreate()
        file_path = './worked_trained_model/trained_lrmodel'
        self.myDb = db()
        self.myYoutube = Youtube()
        self.loadedLRModel = LogisticRegressionModel.load(file_path) #LogisticRegressionModel.load(file_path)
        self.producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))
        #LEMMATIZATION
        # Initialize the lemmatizer
        self.wl = WordNetLemmatizer()

        self.myDb.insertVideos(self.myYoutube.getTop5MusicTrendingVideos())

    def insertNewCommentFromTopVideos(self):
        rowsToInsert = []
        rowsToDisplay = []
        for id in self.myDb.getTop5VideoIdsFromDb():
            # get latest comment timestamp of video
            latestCommentTimestamp = self.myDb.getLatestCommentTimestamp(id)
            comments = self.myYoutube.getCommentsOfVideos(id)

            for cmt in comments:
                if latestCommentTimestamp is None or cmt[1] > latestCommentTimestamp:
                    cmt_text = cmt[0]
                    predictionObj = self.get_prediction(cmt_text)
                    predictedLabel = int(predictionObj.collect()[0][1])
                    newCmt = (cmt[2], id, cmt_text, cmt[1], predictedLabel)
                    # cmt-id, video-id, cmt-text, publish-at, is-toxic
                    rowsToInsert.append(newCmt)
                    topic = 'youtube_comments'
                    self.producer.send(topic, {'newAddedComment': Comment(newCmt).convertCommentToDict()})
#                     while (True):
#                         self.producer.send(topic, newCmt)
#                         time.sleep(5)

        if rowsToInsert:
            self.myDb.insertComments(rowsToInsert)
            return rowsToInsert
        return []

    # define a function to compute sentiments of the received tweets
    def get_prediction(self, cmt_text):
    	try:
            cmt_text = self.finalpreprocess(cmt_text)
            wordsDataFrame = self.myspark.createDataFrame(pd.DataFrame([{'comment_text': cmt_text}]))
            commentIndexer = StringIndexer(inputCol="comment_text", outputCol="comment_text_id")
            wordsDataFrame=commentIndexer.fit(wordsDataFrame).transform(wordsDataFrame)
            assembler = VectorAssembler(inputCols=['comment_text_id'], outputCol="features")
            wordsDataFrame = assembler.transform(wordsDataFrame)

            return self.loadedLRModel.transform(wordsDataFrame).select('comment_text','prediction')

    	except:
    		print('No data')

    #convert to lowercase, strip and remove punctuations
    def preprocess(self, text):
        text = text.lower()
        text =text.strip()
        text =re.compile('<.*?>').sub('', text)
        text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
        text = re.sub('\s+', ' ', text)
        text = re.sub(r'\[[0-9]*\]',' ',text)
        text=re.sub(r'[^\w\s]', '', str(text).lower().strip())
        text = re.sub(r'\d',' ',text)
        text = re.sub(r'\s+',' ',text)
        return text

    # STOPWORD REMOVAL
    def stopword(self, string):
        a= [i for i in string.split() if i not in stopwords.words('english')]
        return ' '.join(a)


    # This is a helper function to map NTLK position tags
    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
    # Tokenize the sentence
    def lemmatizer(self, string):
        word_pos_tags = nltk.pos_tag(word_tokenize(string)) # Get position tags
        a=[self.wl.lemmatize(tag[0], self.get_wordnet_pos(tag[1])) for idx, tag in enumerate(word_pos_tags)] # Map the position tag and lemmatize the word/token
        return " ".join(a)

    def finalpreprocess(self, string):
        return self.lemmatizer(self.stopword(self.preprocess(string)))


    def getCommentsFromDb(self):
        return self.myDb.readCommentPandas()