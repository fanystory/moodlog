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
import datetime as dt
import postpaging

ca = certifi.where()
#client = MongoClient('mongodb+srv://test:sparta@cluster0.2xioe.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
client = MongoClient('mongodb+srv://test:sparta@cluster0.ixw8e.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
#db = client.sparta
db = client.moodlog

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'


#################################################################################
## INDEX INIT
#################################################################################

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:

        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user_db.find_one({"id": payload['id']})

        docPostFirstPage = postpaging.getPostList(1, 0)


        return render_template('index.html', user_id=user_info["id"], user_nick=user_info["nick"], user_pro=user_info["pro"], docPosts=docPostFirstPage)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


#################################################################################
## 포스트 더 불러오기
#################################################################################
@app.route("/api/ppstLoadMore", methods=["POST"])
def post_load_more():
    try:
        current_page = request.form['page_give']
        current_mode = request.form['mode_give']
        docPost = postpaging.getPostList(int(current_page), int(current_mode))

        if(len(docPost)!=0):
            return jsonify({'doc': docPost, 'msg': 'success'})
        else:
            return jsonify({'doc': docPost, 'msg': 'last'})


    except:
        print('페이지 더이상 로드 실패')
        doc = {'msg': 'fail'}
        return jsonify(doc)


#################################################################################
## RANK INIT
#################################################################################
@app.route('/rank')
def rank():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user_db.find_one({"id": payload['id']})

        mood_list = list(db.moods_db.find({}, {'_id': False}).sort('mood_like', -1))

        return render_template('rank.html', user_id=user_info["id"], user_nick=user_info["nick"], user_pro=user_info["pro"], give_moods = mood_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


#################################################################################
## 로그인 관련
#################################################################################

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user_db.find_one({'id': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nick_receive = request.form['nick_give']
    mail_receive = request.form['mail_give']

    print(username_receive, password_receive, nick_receive, mail_receive)

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%M-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/profile_pics/{filename}.{extension}'
    file.save(save_to)

    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "id": username_receive,                               # 아이디
        "pw": password_hash,                                  # 비밀번호
        "nick": nick_receive,
        "mail": mail_receive,
        'pro': f'{filename}.{extension}'

    }
    db.user_db.insert_one(doc)
    return jsonify({'result': 'success'})



@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.user_db.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/check_dupp', methods=['POST'])
def check_dupp():
    nick_receive = request.form['nick_give']
    exists = bool(db.user_db.find_one({"nick": nick_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/check_dup2', methods=['POST'])
def check_dup2():
    mail_receive = request.form['mail_give']
    exists = bool(db.user_db.find_one({"mail": mail_receive}))
    return jsonify({'result': 'success', 'exists': exists})


#################################################################################
## 무드 불러오기
#################################################################################

@app.route("/api/loadMoods", methods=["GET"])
def moods_get():
    mood_list = list(db.moods_db.find({}, {'_id': False}))

    return jsonify({'moods': mood_list})

#################################################################################
## 사운드 클라우드에서 음악 가져오기
#################################################################################

@app.route("/api/findSongUrlAndTitle", methods=["POST"])
def findme():
    try:
        url_receive = request.form['url_give']
        url_receive = url_receive
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)
        data.encoding = 'utf-8'
        html_temp = data.text
        soup = BeautifulSoup(html_temp, 'html.parser')

        title_give = soup.select_one('meta[property="twitter:title"]')['content']
        url_give = soup.select_one('meta[property="twitter:player"]')['content']

        doc = {'title':title_give, 'url':url_give, 'msg':'success'}
        return jsonify(doc)

    except:
        print('음악 로드 실패')
        doc = {'title': '404', 'url': '404', 'msg': 'fail'}
        return jsonify(doc)


#################################################################################
## 포스팅 업로드 / 리스트 전달 API
#################################################################################
@app.route("/api/postUpload", methods=["POST"])
def postUploadToServer():

    try:

        post_title = request.form['give_post_title']
        post_con = request.form['give_post_con']
        post_user = request.form['give_post_user']
        post_date = dt.datetime.now()
        post_mood = request.form['give_post_mood']
        post_url = request.form['give_post_link']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(post_url, headers=headers)
        data.encoding = 'utf-8'
        html_temp = data.text
        soup = BeautifulSoup(html_temp, 'html.parser')
        post_image = soup.select_one('meta[property="twitter:image"]')['content']

        post_num = post_user + str(post_date.year) + str(post_date.month) + str(post_date.day) + str(post_date.hour) + str(post_date.minute) + str(post_date.second) + str(post_date.microsecond)

        return_doc = {
            'post_title':post_title,
            'post_con':post_con,
            'post_num':post_num,
            'post_user':post_user,
            'post_date':post_date,
            'post_mood':post_mood,
            'post_link':post_url,
            'post_image': post_image,
            'msg':'success'
        }
        saveDoc = {
            'post_title': post_title,
            'post_con': post_con,
            'post_num': post_num,
            'post_user': post_user,
            'post_date': post_date,
            'post_mood': post_mood,
            'post_image': post_image,
            'post_link': post_url,
        }

        db.post_db.insert_one(saveDoc)

        #여기서 부터는 무드 개수 올림
        thismood = db.moods_db.find_one({"mood_num": int(post_mood)})
        thismoodMount = thismood["mood_like"]
        thismoodMount+=1
        db.moods_db.update_one({'mood_num': int(post_mood)}, {'$set': {'mood_like': thismoodMount}})


        return jsonify(return_doc)
    except:
        return_doc = {'msg':'fail'}
        print('포스팅 실패')
        return jsonify(return_doc)


#################################################################################
## 유저 페이지
#################################################################################
@app.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user_db.find_one({"id": payload['id']})
        this_page_user_info = db.user_db.find_one({"id": username})

        docthisUsersPost = list(db.post_db.find({"post_user": username}))

        thisPagesPostArray = []

        for doc in docthisUsersPost:
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

        return render_template('user.html', user_info=user_info, this_page_user_info=this_page_user_info, thisUsersPost=thisPagesPostArray)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))



if __name__ == '__main__':
    app.run('0.0.0.0', port=7777, debug=True)