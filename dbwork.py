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


# ์๋ฃํจ
# docs = [[1, '๐ถ ๊ธธ๊ฑฐ๋ฆฌ์์ ํ๋ฌ๋์ค๋ ์์ฆ ๋ธ๋'],
#                 [2, 'โ๏ธ ์์นจ์ ๊นจ์ฐ๋ ๊ตฟ๋ชจ๋ ๋ฎค์ง'],
#                 [3, 'โ๏ธ ๋๋ฅธํ ์คํ ์นดํ์ ์จ๊ฒ๋ง ๊ฐ์ ํธ์ํ ๋ฌด๋'],
#                 [4, '๐ง๐ปโ๐ป ์ผํ๋ฉด์ ๋ฃ๊ธฐ ์ข์ ๋ธ๊ธ'],
#                 [5, '๐คฉ ๋ด์ ๋์ค ์ ๋ฐํ๋ ํ์ฐ์ค ๋ฎค์ง'],
#                 [6, '๐ ์๋ฆฌ๋ฒ๊ณ  ๋นค์ค์ง๋ฌ'],
#                 [7, '๐ ์๊ธฐ์ ์ ๊ฟ์  ์์ฝํ๋ ์์'],
#                 [8, 'โ๏ธ ๋ด ๋ง์์ ๊ตฌ๋ฆ'],
#                 [9, '๐ซ  ์๋ฌด์๊ฐ ์์๋ ๋ค์ด์'],
#                 [10, '๐คก ๋ญ์ง ๋ชจ๋ฅด๊ฒ ๋๋ฐ ์๋ฌดํผ ์ ๋'],
#                 [11, '๐ ์ ์๋ ํน์ ๋ถ์ฅ๋ ๋ชฐ๋ ๋ฃ๋ ์กฐ์ฉํ ์์'],
#                 [12, '๐โโ๏ธ ๋ง์ฌ์ง์ต์์ ๋์ฌ๊ฒ ๊ฐ์ ํ๋งํ๋ง ๋ฌด๋'],
#                 [13, '๐ช ๋๊ทผ์ฉ ๋ธ๊ธ']]
#
# for doc in docs:
#     print(doc[0], doc[1])
#     mydata = {'mood_num':doc[0], 'mood_name':doc[1]}
#     db.moods_db.insert_one(mydata)
#     print('์ ์ฅ์ฑ๊ณต')

#url_receive : request.form['url_give']

