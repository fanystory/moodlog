from pymongo import MongoClient
import datetime
import hashlib
import certifi
from bs4 import BeautifulSoup
import requests
import datetime as dt

ca = certifi.where()
#client = MongoClient('mongodb+srv://test:sparta@cluster0.2xioe.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
client = MongoClient('mongodb+srv://test:sparta@cluster0.ixw8e.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
#db = client.sparta
db = client.moodlog

SECRET_KEY = 'SPARTA'

def getPostList(thisPage, thismode):
    docPostCurrentPage = list(db.post_db.find().skip((thisPage - 1) * 5).sort('_id', -1).limit(5))

    if thismode == 0:
        docPostCurrentPage = list(db.post_db.find().skip((thisPage - 1) * 5).sort('_id', -1).limit(5))
    else:
        docPostCurrentPage = list(db.post_db.find({'post_mood': str(thismode)}).skip((thisPage - 1) * 5).sort('_id', -1).limit(5))

    thisPagesPostArray = []

    for doc in docPostCurrentPage:
        user = db.user_db.find_one({'id': doc['post_user']})
        mood = db.moods_db.find_one({'mood_num': int(doc['post_mood'])})

        addingList = {'post_num': doc['post_num'],
                      'post_user_id': user['id'],
                      'post_user_nick': user['nick'],
                      'post_user_pro': user['pro'],
                      'post_title': doc['post_title'],
                      'post_con': doc['post_con'],
                      'post_mood': mood['mood_name'],
                      'post_link': doc['post_link'],
                      'post_image': doc['post_image']
                      }

        thisPagesPostArray.append(addingList)

    print(thisPagesPostArray)

    return thisPagesPostArray