let currentPage = 1;
let currentMode = 0;

$(document).ready(function () {
    $('#post_soundCloudUrl').change(function () {
        let myUrl = $(this).val();
        findSong(myUrl);
    });
});

/* #################################################################################
로그인 관련 메소드 모음
################################################################################# */


function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href = '/login'
}

/* #################################################################################
프론트엔드 동작 메소드 모음
################################################################################# */

function onTop(){
    $("html, body").animate({scrollTop: 0}, "slow");
    return false;
}

/* #################################################################################
포스트 업로드
################################################################################# */

function uploadPost(){
    let doc_user_id = $('#post_userId').val();
    let doc_post_title = $('#post_title').val();
    let doc_post_url = $('#post_soundCloudUrl').val();
    let doc_post_message = $('#post_message').val();
    let doc_post_mood = $('#post_selectMood').val();

    if (doc_post_url.length == 0){
        alert('사운드 클라우드 URL을 입력해주세요.');
        return;
    }

    if (doc_post_message.length < 10 || doc_post_message.length > 100){
        alert('포스트 메시지는 10자이상 100자 이하로 입력해주세요.');
        return;
    }

    $.ajax({
        type: "POST",
        url: "/api/postUpload",
        data: {give_post_title: doc_post_title, give_post_con: doc_post_message, give_post_user: doc_user_id, give_post_mood: doc_post_mood, give_post_link: doc_post_url},
        success: function (response) {
            if (response["msg"] == "success"){
                alert('포스트가 공유되었어요!');
                window.location.reload();
            }else{
                alert('포스트 게시 실패');
            }
        }
    });

    console.log(doc_user_id, doc_post_title, doc_post_url, doc_post_message, doc_post_mood);
}

function findSong(para_url){
    $.ajax({
        type: "POST",
        url: "/api/findSongUrlAndTitle",
        data: {url_give: para_url},
        success: function (response) {
            if (response["msg"] == "success"){
                let temp_html = `<iframe width="100%" height="300" scrolling="no" frameborder="no" allow="autoplay" src="${response["url"]}"></iframe>`;
                $('#div_previewMusic').empty();
                $('#div_previewMusic').append(temp_html);

                $('#post_title').val(response["title"]);
            }else{
                alert('정확한 주소를 붙여 넣어주세요.');
                $('#post_soundCloudUrl').val('');
                $('#post_title').val('');
                $('#div_previewMusic').empty();
            }
        }
    });
}

/* #################################################################################
무드 불러오기
################################################################################# */
let mood_list = []; //무드 리스트 전역변수

function loadMoodListForIndex(){
    $.ajax({
        type: "GET",
        url: "/api/loadMoods",
        data: {},
        success: function (response) {
            //console.log(response["buckets"])
            let moods = response["moods"];
            let temp;
            for (let i=0; i<moods.length; i++){
                let mood_num = moods[i]['mood_num'];
                let mood_name = moods[i]['mood_name'];
                temp = `<option value=${mood_num}>${mood_name}</option>`;
                $('#selectMoodList').append(temp); //index>상단 무드 고르기에 리스트 주기
                $('#post_selectMood').append(temp); //index>등록 modal창에 리스트 주기
                mood_list.push(mood_name)
            }
        }
    });
}


function playMusic(para_url){
    window.open(para_url);
}

/* #################################################################################
무드 변경
################################################################################# */
function changeMode(){
    let mode_num = $('#div_selectMood option:selected').val();
    $('#section_mainbody').empty();

    currentMode = mode_num;
    currentPage = 0;

    loadMorePost();
}

/* #################################################################################
포스트 더 불러오기
################################################################################# */
function loadMorePost(){
    currentPage ++;

    $.ajax({
        type: "POST",
        url: "/api/ppstLoadMore",
        data: {page_give: currentPage, mode_give: currentMode},
        success: function (response) {
            if (response['msg']=="success"){
                let rows = response['doc']

                for (i=0;i<rows.length;i++){

                    temp_html = `<article class="media">
                                    <figure class="media-left">
                                        <p class="image is-64x64">
                                            <a href="./user/${rows[i]['post_user_id']}"><img src="./static/profile_pics/${rows[i]['post_user_pro']}" class="is-rounded"></a>
                                        </p>
                                    </figure>
                                    <div class="media-content">
                                        <div class="content" >
                                            <p>
                                                <strong>${rows[i]['post_user_nick']}</strong> <small>${rows[i]['post_user_id']}</small>
                    
                                            </p>
                                            <span class="tag is-info is-light">${rows[i]['post_mood']}</span>
                    
                                            <!-- 큰일났다 사운드 클라우드가 jinja를 막았다... js로 우회해야함 -->
                                            <div id="${rows[i]['post_link']}" class="iHateSoundCloud">
                    
                                            </div>
                    
                                            <div class="box" style="width:100%; margin-top: 5px;">
                    
                    
                                                <div class="columns is-mobile">
                                                    <div class="column is-one-quarter">
                                                        <img src="${rows[i]['post_image']}">
                                                    </div>
                                                    <div class="column">
                                                        <h4>${rows[i]['post_title']}</h4>
                                                        <p>
                                                            ${rows[i]['post_con']}
                                                        </p>
                    
                                                        <div style="width:100%; text-align: right">
                                                            <div>
                                                                <button class="button is-danger" onclick="playMusic('${rows[i]['post_link']}')">
                                                                    <span class="icon">
                                                                       <i class="fa-solid fa-play"></i>
                                                                    </span>
                                                                    <span>재생</span>
                                                                </button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <nav class="level is-mobile" style="margin-top:20px; margin-bottom:20px;">
                                            <div class="level-left">
                                                <a class="level-item">
                                                </a>
                                            </div>
                                        </nav>
                                    </div>
                                    <div class="media-right">
                                    </div>
                                </article>`;
                    $('#section_mainbody').append(temp_html);

                }
            }else if (response['msg']=="last"){
                alert('더 이상 불러올 포스트가 없습니다.')
            }else{
                alert('서버와의 연결에 실패했습니다.');
            }
        }
    });

}

/* #################################################################################
시간 관련
################################################################################# */

function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    return parseInt(time) + "일 전"
}

function get_posts(username) {
    if (username == undefined) {
        username = ""
    }
    $("#post-box").empty()
    $.ajax({
        type: "GET",
        url: `/get_posts?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    let time_post = new Date(post["date"])
                    let time_before = time2str(time_post)
                    let html_temp = `<div class="box" id="${post["_id"]}">
                                        <article class="media">
                                            <div class="media-left">
                                                <a class="image is-64x64" href="/user/${post['username']}">
                                                    <img class="is-rounded" src="/static/${post['profile_pic_real']}"
                                                         alt="Image">
                                                </a>
                                            </div>
                                            <div class="media-content">
                                                <div class="content">
                                                    <p>
                                                        <strong>${post['profile_name']}</strong> <small>@${post['username']}</small> <small>${time_before}</small>
                                                        <br>
                                                        ${post['comment']}
                                                    </p>
                                                </div>
                                                <nav class="level is-mobile">
                                                    <div class="level-left">
                                                        <a class="level-item is-sparta" aria-label="heart" onclick="toggle_like('${post['_id']}', 'heart')">
                                                            <span class="icon is-small"><i class="fa fa-heart"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span class="like-num">2.7k</span>
                                                        </a>
                                                    </div>

                                                </nav>
                                            </div>
                                        </article>
                                    </div>`
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
}
/* #################################################################################
라이브러리 호출 관련
################################################################################# */

document.addEventListener('DOMContentLoaded', () => {
// Functions to open and close a modal
    function openModal($el) {
        $el.classList.add('is-active');
    }

    function closeModal($el) {
        $el.classList.remove('is-active');
    }

    function closeAllModals() {
        (document.querySelectorAll('.modal') || []).forEach(($modal) => {
            closeModal($modal);
        });
    }

// Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
        const modal = $trigger.dataset.target;
        const $target = document.getElementById(modal);

        $trigger.addEventListener('click', () => {
            openModal($target);
        });
    });

// Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
        });
    });

// Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
        const e = event || window.event;

        if (e.keyCode === 27) { // Escape key
            closeAllModals();
        }
    });
});
