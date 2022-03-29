
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
            console.log(response.chat_log);
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

    $.ajax({
        type: 'POST',
        url: '/api/search/crawling',
        data: {"target": "커피"},
        datatype: 'form',
        async: false,
        success: function (response) {
            console.log(response['all_response']['shopping'])

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
            hovering_like_heart()
            set_animation_more()

            // clicked_like
            like_news()

            // search_bar
            initialize_search_bar()
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

// // 각 nav_bar에 click event 주기
// let navs = document.getElementsByClassName('recommend_nav')
// let navs_list_id = ['recommend_youtube_container', 'recommend_news_container', 'recommend_book_container', 'recommend_shopping_container']
// for (let i = 0; i < navs.length; i++) {
//     let nav_row = navs[i].children
//     for (let j = 0; j < nav_row.length; j++) {
//         nav_row[j].addEventListener('click', function () {
//             move_category(navs_list_id[j])
//         })
//     }
// }

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
                                <div class="recommend_like_heart" style="background-image: url('/static/images/empty_heart.png')">
                                    
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
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        content_type = 's';
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < book_crawling_data_list.length; i++) {
        let book_row = book_crawling_data_list[i]
        let content_id = 'book_' + content_type + '_' + i
        let temp_html = `<div class="content_box" id="${content_id}"> 
                            <div class="recommend_toggle recommend_book_toggle">
                                <div class="profile_like_news_toggle" onclick="content_do_share('${book_row[5]}')">
                                    <img src="/static/images/share.png">
                                </div>
                                <div class="recommend_like_heart"
                                     style="background-image: url('/static/images/empty_heart.png')">
                                </div>
                            </div>
                            <a href="${book_row[5]}" target="_blank">
                                <div class="book_img" style="background-image: url('${book_row[6]}')"></div>
                            </a>
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
        let temp_html = `<div class="recommend_shopping_search_content" id="${content_id}">
                                    <div class="recommend_toggle">
                                        <div class="profile_like_news_toggle" onclick="content_do_share('${shopping_row[3]}')">
                                            <img src="/static/images/share.png">
                                        </div>
                                        <div class="recommend_like_heart"
                                             style="background-image: url('/static/images/empty_heart.png')">
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
function hovering_like_heart() {

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
        let url = document.getElementById(id).firstElementChild.src
        // youtube like function
        like_youtube_ajax(url, type)
    } else if (checker === 'news') {
        console.log('news!')
    } else if (checker === 'book') {
        console.log('book!')
    } else if (checker === 'shopping') {
        console.log('shopping')
    }
}


function like_youtube_ajax(data, type) {

    // like 할 때
    if (type === 'like') {
        let result = 'Like result : '
        $.ajax({
            type: 'POST',
            url: '/api/like/youtube',
            data: {'url': data},
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
            data: {'url': data},
            success: function (response) {
                let ajax_result = response['result']
                result += ajax_result
                alert(result)
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
                        console.log(response['all_response'])
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
                        hovering_like_heart()
                        set_animation_more()

                        // clicked_like
                        like_news()
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
