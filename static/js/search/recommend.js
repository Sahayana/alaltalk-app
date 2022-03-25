function click_recommend_function() {
    console.log('page is onload!')

    $.ajax({
        type: 'POST',
        url: '/api/search/crawling',
        data: {"target": "커피"},
        datatype: 'form',
        success: function (response) {
            console.log(response['all_response']['news'])

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


            // clicked_like
            like_news()
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
        let temp_html = `<div class="content_box" id="${content_id}">
                                    <iframe class="video_img" src="${youtube_row[0]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>ㅇ</iframe>
                                    <div class="video_title" style="font-size: 13px">${youtube_row[2]}</div>
                                    <div class="video_count">${youtube_row[3]}</div>
                                    <div class="play_icon"></div>
                                    <div class="more_icon"></div>
                                    <div class="toggle" style="display: none" >
                                        <p>공유하기</p>
                                        <div class="line"></div>
                                        <p>찜하기</p>
                                    </div>
                                </div>`
        $('#youtube_recommend_content').append(temp_html)
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
                                <div class="profile_like_news_toggle" onclick="content_do_share(${content_id})">
                                    <img src="/static/images/share.png">
                                </div>
                                <div class="profile_like_news_heart" style="background-image: url('/static/images/empty_heart.png')">
                                    
                                </div>
                            </div>
                        </div>`
        //
        $('#news_recommend_content').append(temp_html)
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
                    <div class="book_img" style="background-image: url('${book_row[6]}')"></div>
                    <div class="more_icon" onclick="more_open_or_off(${content_id})"></div>
                    <div class="toggle" style="display: none;">
                        <p>공유하기</p>
                        <div class="line"></div>
                        <p>찜하기</p>
                    </div>
                </div>`
        $('#book_recommend_content').append(temp_html)
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
                                    <div class="more_icon" id="shopping_recommend_${i}" onclick="more_open_or_off(this.id)"></div>
                                    <div class="toggle" style="display: none">
                                        <div class="toggle_row">
                                            <p>공유하기</p>
                                        </div>
                                        <div class="toggle_row">
                                            <p>찜하기</p>
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
        $('#shopping_recommend_content').append(temp_html)
    }
}


// more function

function more_open_or_off(id) {
    let toggle = document.getElementById(id).nextElementSibling
    if (toggle.style.display === 'none') {
        toggle.style.display = 'block'
    } else {
        toggle.style.display = 'none'
    }

}

// like clicked
function hovering_like_heart() {
    let empty_heart_classes = document.getElementsByClassName('profile_like_news_heart')
    let background_heart = 'url("/static/images/heart.png")'
    let background_empty_heart = 'url("/static/images/empty_heart.png")'
    for (let i = 0; i < empty_heart_classes.length; i++) {

        empty_heart_classes[i].addEventListener('click', (event) => {
                let curr_backgroundImage = event.target.style.backgroundImage;
                if (curr_backgroundImage === background_empty_heart) {
                    event.target.style.backgroundImage = background_heart
                    alert('like!')
                } else {
                    event.target.style.backgroundImage = background_empty_heart
                    alert('like! 취소!')
                }

            }
        )

    }
}

// 공유하기!
function content_do_share(id){

}

