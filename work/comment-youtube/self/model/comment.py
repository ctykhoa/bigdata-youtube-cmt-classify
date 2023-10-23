import json

class Comment:
    def __init__(self, cmtObj = None):
    # cmt-id, video-id, cmt-text, publish-at, is-toxic
        if cmtObj:
            self.cmtId = cmtObj[0]
            self.videoId = cmtObj[1]
            self.cmtText = cmtObj[2]
            self.publishedAt = cmtObj[3]
            self.isToxic = cmtObj[4]


    def convertCommentToDict(self):
        return {
            'commentId': self.cmtId,
            'videoId': self.videoId,
            'commentText': self.cmtText,
            'publishedAt': self.publishedAt,
            'isToxic': 'Yes' if self.isToxic == 1 else 'No'
        }