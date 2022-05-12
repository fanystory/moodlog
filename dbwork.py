from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from pymongo import MongoClient
import certifi
from bs4 import BeautifulSoup
import requests


ca = certifi.where()
#client = MongoClient('mongodb+srv://test:sparta@cluster0.2xioe.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
client = MongoClient('mongodb+srv://test:sparta@cluster0.ixw8e.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
#db = client.sparta
db = client.moodlog

#page = 1
#all_users = list(db.post_db.find().sort('_id',-1).skip((page-1)*1).limit(1))





# for user in all_users:
#     print(user['post_title']+user['post_con'])


# 완료함
# docs = [[1, '🚶 길거리에서 흘러나오는 요즘 노래'],
#                 [2, '☀️ 아침을 깨우는 굿모닝 뮤직'],
#                 [3, '☕️ 나른한 오후 카페에 온것만 같은 편안한 무드'],
#                 [4, '🧑🏻‍💻 일하면서 듣기 좋은 브금'],
#                 [5, '🤩 내적댄스 유발하는 하우스 뮤직'],
#                 [6, '💃 소리벗고 빤스질러'],
#                 [7, '🌙 자기전에 꿀잠 예약하는 음악'],
#                 [8, '☁️ 내 마음에 구름'],
#                 [9, '🫠 아무생각 없을때 들어요'],
#                 [10, '🤡 뭔진 모르겠는데 아무튼 신나'],
#                 [11, '👀 선생님 혹은 부장님 몰래 듣는 조용한 음악'],
#                 [12, '💆‍♂️ 마사지샵에서 나올것 같은 힐링힐링 무드'],
#                 [13, '💪 득근용 브금']]
#
# for doc in docs:
#     print(doc[0], doc[1])
#     mydata = {'mood_num':doc[0], 'mood_name':doc[1]}
#     db.moods_db.insert_one(mydata)
#     print('저장성공')

#url_receive : request.form['url_give']

