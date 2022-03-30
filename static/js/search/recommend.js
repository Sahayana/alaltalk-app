
// 채팅로그 받아오기
var chat_log = [];
function get_chat_log(){
   var link = document.location.href;
    console.log(link);
    let room_id = link.split('/');
    room_id = parseInt(room_id[5]);
    
    $.ajax({
        url: "/chat/chatlog/",
        type: 'POST',
        data: JSON.stringify({"room_id": room_id}),
        enctype: 'multipart/form-data',
        async: false,
        success: function (response) {
            console.log('chat_log:', response.chat_log);
            chat_log = response.chat_log;

        },
        error: function (request, status, error) {
            alert('error')

            console.log(request, status, error)
        }

    });
}



function click_recommend_function() {
    console.log('page is onload!')

    let machin_result = '아이유'
    // let form_data = new FormData()
    // form_data.append('chat_log', chat_log);
    //
    // $.ajax({
    //     type: "POST",
    //     url: "http://127.0.0.1:5000/api/v1/textrank/",
    //     data: form_data,
    //     cache: false,
    //     processData: false,
    //     contentType: false,
    //     async: false,
    //     enctype: 'multipart/form-data',
    //     success: function (response) {
    //         // console.log(response.keyword)
    //         // console.log('추천시스템 성공!')
    //         machin_result  = response.keyword[0]
    //
    //     },
    //     error: function (request, status, error) {
    //         alert('error')
    //
    //         console.log(request, status, error)
    //     }
    //
    // });
    recommend_crawling_on(machin_result)

}

function recommend_crawling_on(data){
    $.ajax({
        type: 'POST',
        url: '/api/search/crawling',
        data: {"target": data},
        datatype: 'form',
        async: true,
        success: function (response) {
            console.log(response['all_response'])

            // 스피너 멈추기
            let spinners = document.getElementsByClassName('recommend_spinner')

            for (let k = 0; k < spinners.length; k++) {
                spinners[k].style.display = 'none';
            }

            // content 내용 붙이기
            youtube_content_add(response['all_response']['youtube'], 'crawling')
            news_content_add(response['all_response']['news'], 'crawling')
            book_content_add(response['all_response']['book'], 'crawling')
            shopping_content_add(response['all_response']['shopping'], 'crawling')


            // hovering_like
            clicked_like_heart()
            set_animation_more()

            // search_bar
            initialize_search_bar()

            // toggle switch setting
            recommend_switch_setting()
        }
    })
}


// 탭 이동 함수
function move_category(target_id) {
    document.getElementById('recommend_youtube_container').style.display = 'none'
    document.getElementById('recommend_news_container').style.display = 'none'
    document.getElementById('recommend_book_container').style.display = 'none'
    document.getElementById('recommend_shopping_container').style.display = 'none'
    document.getElementById(target_id).style.display = 'block'
}

function give_event() {
    let navs = document.getElementsByClassName('recommend_nav')
    let navs_list_id = ['recommend_youtube_container', 'recommend_news_container', 'recommend_book_container', 'recommend_shopping_container']
    for (let i = 0; i < navs.length; i++) {
        let nav_row = navs[i].children
        for (let j = 0; j < nav_row.length; j++) {
            nav_row[j].addEventListener('click', function () {
                move_category(navs_list_id[j])
            })
        }
    }
}


// Crawling 붙여 넣기
// youtube
function youtube_content_add(youtube_crawling_data_list, type) {
    let content_type = ''
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        content_type = 's';
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < youtube_crawling_data_list.length; i++) {
        let youtube_row = youtube_crawling_data_list[i]
        let content_id = 'youtube_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(youtube_row[4]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="content_box" id="${content_id}">
                                    <iframe class="video_img" src="${youtube_row[0]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>ㅇ</iframe>
                                    <div class="video_title" style="font-size: 13px">${youtube_row[2]}</div>
                                    <div class="video_count">${youtube_row[3]}</div>
                                    <div class="recommend_youtube_heart_parent">
                                        <div class="recommend_like_heart recommend_youtube_like_heart" style="background-image: url(${heart_image})">
                                    </div>
                                </div>`
        if (content_type === 'c') {
            $('#youtube_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#youtube_search_content').append(temp_html)
        }
    }
}

// News
function news_content_add(news_crawling_data_list, type) {
    let content_type = ''
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        content_type = 's';
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < news_crawling_data_list.length; i++) {
        let news_row = news_crawling_data_list[i]
        let content_id = 'news_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(news_row[6]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="recommend_news_search_content" id="${content_id}">
                            <div class="recommend_news_search_content_image">
                                <a href="${news_row[3]}" target="_blank">
                                    <img src="${news_row[5]}">
                                </a>
                            </div>
                            <div class="recommend_news_search_content_desc">
                                <div class="recommend_news_search_content_desc_title">
                                    <p>${news_row[2]}</p>
                                </div>
                                <div class="recommend_news_search_content_desc_detail">
                                    <p>${news_row[4]}</p>
                                </div>
                                <div class="recommend_news_search_content_desc_footer">
                                    <div class="recommend_news_search_content_desc_footer_newspaper">
                                        <p>${news_row[0]}</p>
                                    </div>
                                    <div class="recommend_news_search_content_desc_footer_time">
                                        <p>${news_row[1]}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="recommend_news_search_content_more">
                                <div class="profile_like_news_toggle" onclick="content_do_share('${news_row[3]}')">
                                    <img src="/static/images/share.png">
                                </div>
                                <div class="recommend_like_heart" style="background-image: url('${heart_image}')">
                                    
                                </div>
                            </div>
                        </div>`
        //
        if (content_type === 'c') {
            $('#news_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#news_search_content').append(temp_html)
        }
    }
}

//book
function book_content_add(book_crawling_data_list, type) {
    let content_type = ''
    let display_value = 'none'
    let width = '102%'
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        width = '15vw'
        content_type = 's';
        display_value = 'flex'
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < book_crawling_data_list.length; i++) {
        let book_row = book_crawling_data_list[i]
        let content_id = 'book_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(book_row[7]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="content_box" id="${content_id}"> 
                            <div class="recommend_toggle recommend_book_toggle" style="width: ${width}">
                                <div class="profile_like_news_toggle" onclick="content_do_share('${book_row[5]}')">
                                    <img src="/static/images/share.png">
                                </div>
                                <div class="recommend_like_heart"
                                     style="background-image: url('${heart_image}')">
                                </div>
                            </div>
                            <a href="${book_row[5]}" target="_blank">
                                <div class="book_img" style="background-image: url('${book_row[6]}')"></div>
                            </a>
                            <div class="recommend_book_desc" style="display: ${display_value}">
                                <div class="recommend_book_desc_title">
                                    <p>제목</p>
                                    <p>${book_row[0]}</p>
                                </div>
                                <div class="recommend_book_desc_series">
                                    <p>시리즈</p>
                                    <p>${book_row[3]}</p>
                                </div>
                                <div class="recommend_book_desc_company">
                                    <p>출판사</p>
                                    <p>${book_row[2]}</p>
                                </div>
                                <div class="recommend_book_desc_author">
                                    <p>작가</p>
                                    <p>${book_row[1]}</p>
                                </div>
                                <div class="recommend_book_desc_price">
                                    <p>가격</p>
                                    <p>${book_row[4]}</p>
                                </div>
                            </div>
                        </div>`
        if (content_type === 'c') {
            $('#book_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#book_search_content').append(temp_html)
        }
    }
}


// shopping
function shopping_content_add(shopping_crawling_data_list, type) {
    let content_type = ''
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        content_type = 's';
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < shopping_crawling_data_list.length; i++) {
        let shopping_row = shopping_crawling_data_list[i]
        let content_id = 'shopping_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(shopping_row[4]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="recommend_shopping_search_content" id="${content_id}">
                                    <div class="recommend_toggle">
                                        <div class="profile_like_news_toggle" onclick="content_do_share('${shopping_row[3]}')">
                                            <img src="/static/images/share.png">
                                        </div>
                                        <div class="recommend_like_heart"
                                             style="background-image: url('${heart_image}')">
                                        </div>
                                    </div>
                                    <a href="${shopping_row[3]}" target="_blank">
                                        <div class="recommend_shopping_search_content_img">
                                            <img src="${shopping_row[0]}">
                                        </div>
                                    </a>
                                    <div class="recommend_shopping_search_content_desc">
                                        <div class="recommend_shopping_search_content_desc_bar"></div>
                                        <div class="recommend_shopping_search_content_desc_title">
                                            <p>${shopping_row[1]}</p>
                                        </div>
                                        <div class="recommend_shopping_search_content_desc_price">
                                            <p>${shopping_row[2]} 원</p>
                                        </div>
                                    </div>
                                </div>`
        if (content_type === 'c') {
            $('#shopping_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#shopping_search_content').append(temp_html)
        }

    }
}


// more function

function more_open_or_off(id) {
    let other_toggles = document.getElementsByClassName('toggle')

    for (let i = 0; i < other_toggles.length; i++) {
        other_toggles[i].style.display = 'none'
    }

    let toggle = document.getElementById(id).nextElementSibling
    if (toggle.style.display === 'none') {
        toggle.style.display = 'block'
    } else {
        toggle.style.display = 'none'
    }

}

// more_shopping_function

function set_animation_more() {
    let shopping_content = document.getElementsByClassName('recommend_toggle')
    for (let i = 0; i < shopping_content.length; i++) {
        shopping_content[i].addEventListener('mouseover', function () {
            shopping_content[i].style.animation = 'appear_toggle 1s ease-out forwards'

        })
        shopping_content[i].addEventListener('mouseout', function () {
            shopping_content[i].style.animation = ''
            shopping_content[i].style.opacity = '0'

        })
    }
}

// like clicked
function clicked_like_heart() {

    $('recommend_like_heart').off('click')
    let empty_heart_classes = document.getElementsByClassName('recommend_like_heart')
    let background_heart = 'url("/static/images/heart.png")'
    let background_empty_heart = 'url("/static/images/empty_heart.png")'
    for (let i = 0; i < empty_heart_classes.length; i++) {
        empty_heart_classes[i].addEventListener('click', (event) => {
                let curr_backgroundImage = event.target.style.backgroundImage;
                let id = event.target.parentElement.parentElement.id

                if (curr_backgroundImage === background_empty_heart) {
                    event.target.style.backgroundImage = background_heart
                    like_check_hub(id, 'like')

                } else {
                    event.target.style.backgroundImage = background_empty_heart
                    like_check_hub(id, 'like_cancel')

                }

            }
        )

    }
}

// like 분류 함수 (youtube? news? book? shopping?)
function like_check_hub(id, type) {
    let checker = id.split('_')[0]
    if (checker === 'youtube') {
        // url 가져 오기
        let youtube = document.getElementById(id)
        let url = youtube.firstElementChild.src
        let title = youtube.children[1].innerText
        let views = youtube.children[2].innerText
        let youtube_data = {}

        youtube_data['url'] = url
        youtube_data['title'] = title
        youtube_data['views'] = views

        // youtube like function
        like_youtube_ajax(youtube_data, type)
    }
    // news data 가져 오기
    else if (checker === 'news') {
        let news = document.getElementById(id)
        let link = news.children[0].children[0].href
        let title = news.children[1].children[0].innerText
        let content = news.children[1].children[1].innerText
        let company = news.children[1].children[2].children[0].innerText
        let date = news.children[1].children[2].children[1].innerText
        let thumbnail = news.children[0].children[0].children[0].src

        let news_data = {}
        news_data['title'] = title
        news_data['date'] = date
        news_data['company'] = company
        news_data['content'] = content
        news_data['thumbnail'] = thumbnail
        news_data['link'] = link

        like_news_ajax(news_data, type)
    }
    // book data 가져 오기
    else if (checker === 'book') {
        let book = document.getElementById(id)
        let title = book.children[2].children[0].children[1].innerText
        let author = book.children[2].children[3].children[1].innerText
        let company = book.children[2].children[2].children[1].innerText
        let price = book.children[2].children[4].children[1].innerText
        let link = book.children[1].href
        let thumbnail = book.children[1].children[0].style.backgroundImage.split('url("')[1].split('")')[0]
        let series = book.children[2].children[1].children[1].innerText

        let book_data = {}
        book_data['title'] = title
        book_data['author'] = author
        book_data['company'] = company
        book_data['price'] = price
        book_data['link'] = link
        book_data['thumbnail'] = thumbnail
        book_data['series'] = series

        like_book_ajax(book_data, type)
    }
    // shopping data 가져 오기
    else if (checker === 'shopping') {
        let shopping = document.getElementById(id)
        let link = shopping.children[1].href
        let price = shopping.children[2].children[2].children[0].innerText
        let title = shopping.children[2].children[1].children[0].innerText
        let thumbnail = shopping.children[1].children[0].children[0].src

        let shopping_data = {}
        shopping_data['price'] = price
        shopping_data['title'] = title
        shopping_data['thumbnail'] = thumbnail
        shopping_data['link'] = link
        console.log(shopping_data)
        like_shopping_ajax(shopping_data, type)
    }
}


function like_youtube_ajax(data, type) {

    // like 할 때
    if (type === 'like') {
        let result = 'Like result : '
        $.ajax({
            type: 'POST',
            url: '/api/like/youtube',
            data: data,
            success: function (response) {
                let ajax_result = response['result']
                result += ajax_result
                alert(result)
            }
        })
    } // like 취소
    else if(type === 'like_cancel'){
        let result = 'Like cancel result : '
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/youtube',
            data: data,
            success: function (response) {
                let ajax_result = response['result']
                result += ajax_result
                alert(result)
            }
        })
    }

}

function like_news_ajax(data, type){
    // 뉴스 like 할때
    if(type  === 'like'){
        $.ajax({
            type: 'POST',
            url: '/api/like/news',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
    // 뉴스 like 취소 할 때
    else if(type==='like_cancel'){
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/news',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
}

function like_book_ajax(data, type){
    // 책 like 할때
    if(type  === 'like'){
        $.ajax({
            type: 'POST',
            url: '/api/like/book',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
    // 책 like 취소 할 때
    else if(type==='like_cancel'){
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/book',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
}

function like_shopping_ajax(data, type){
    // 쇼핑 like 할때
    if(type  === 'like'){
        $.ajax({
            type: 'POST',
            url: '/api/like/shopping',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
    // 쇼핑 like 취소 할 때
    else if(type==='like_cancel'){
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/shopping',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
}


// 공유하기 버튼
function content_do_share(str) {
    var textarea = document.createElement('textarea');
    textarea.value = str;
    document.body.appendChild(textarea);
    textarea.select();
    textarea.setSelectionRange(0, 9999);
    document.execCommand('copy');
    document.body.removeChild(textarea);
    alert('복사되었습니다')
}

// search 관련
function initialize_search_bar() {
    let search_bars = document.getElementsByClassName('search_bar')
    for (let i = 0; i < search_bars.length; i++) {
        search_bars[i].children[1].addEventListener('keyup', (e) => {
            if (e.keyCode === 13) {
                let search_word = search_bars[i].children[1].value
                search_bars[i].children[1].value = ''


                // 이전 데이터 지우기
                clear_content()

                // // spinner running
                let search_spinner = document.getElementsByClassName('spinner_search')
                //
                // for(let i=0; i<search_spinner.length;i++){
                //     search_spinner[i].style.display ='flex'
                // }


                // search_창 보이기
                let search_contents = document.getElementsByClassName('search_content')
                for (let k = 0; k < search_contents.length; k++) {
                    search_contents[k].style.display = 'block'
                }
                document.getElementsByClassName('search_news_content')[0].style.display = 'block'
                document.getElementsByClassName('search_book_content')[0].style.display = 'block'


                $.ajax({
                    type: 'POST',
                    url: '/api/search/crawling',
                    data: {"target": search_word},
                    datatype: 'form',
                    success: function (response) {

                        // search_spinner 정지
                        for (let i = 0; i < search_spinner.length; i++) {
                            search_spinner[i].style.display = 'none'
                        }


                        // content 내용 붙이기
                        youtube_content_add(response['all_response']['youtube'], 'search')
                        news_content_add(response['all_response']['news'], 'search')
                        book_content_add(response['all_response']['book'], 'search')
                        shopping_content_add(response['all_response']['shopping'], 'search')

                        // hovering_like
                        clicked_like_heart()
                        set_animation_more()

                        // clicked_like
                        // like_news()
                    }
                })
            }
        })

    }
}

function clear_content() {
    let spinner_html = `<div class="recommend_spinner spinner_search" style="display: flex;">
                            <div class="recommend_spinner_lorder"></div>
                        </div>`

    $('#youtube_search_content').empty();
    $('#youtube_search_content').append(spinner_html);

    $('#news_search_content').empty();
    $('#news_search_content').append(spinner_html);

    $('#book_search_content').empty();
    $('#book_search_content').append(spinner_html);

    $('#shopping_search_content').empty();
    $('#shopping_search_content').append(spinner_html);
}

function recommend_switch_setting(){
    let switches = document.getElementsByClassName('recommend_container_total_toggle')
    for(let i=0; i<switches.length; i++){
        switches[i].addEventListener('click', (e)=>{
            console.log('switch clicked!!!!')
            console.log(e.target.innerText)
            let state = e.target.innerText

            if(state ==='ON'){

                e.target.innerText = 'OFF';
                e.target.nextElementSibling.style.display='none'
            }
            else if(state === 'OFF'){

                e.target.innerText = 'ON';
                e.target.nextElementSibling.style.display='flex'
            }
        })
    }
}