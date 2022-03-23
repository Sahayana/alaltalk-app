function click_recommend_function() {
    console.log('page is onload!')

    $.ajax({
        type: 'POST',
        url: '/api/search/crawling',
        data: {"target": "코딩"},
        datatype: 'form',
        success: function (response) {
            console.log(response['all_response']['book'])

            // 스피너 멈추기
            let spinners = document.getElementsByClassName('recommend_spinner')

            for (let k = 0; k < spinners.length; k++) {
                spinners[k].style.display = 'none';
            }
            // content 내용 붙이기
            youtube_content_add(response['all_response']['youtube'])
            news_content_add(response['all_response']['news'])
            shopping_content_add(response['all_response']['shopping'])

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
function youtube_content_add(youtube_crawling_data_list){
    for (let i = 0; i < youtube_crawling_data_list.length; i++) {
                let youtube_row = youtube_crawling_data_list[i]
                let temp_html = `<div class="content_box" >
                                    <iframe class="video_img" src="${youtube_row[0]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>ㅇ</iframe>
                                    <div class="video_title" style="font-size: 13px">${youtube_row[2]}</div>
                                    <div class="video_count">${youtube_row[3]}</div>
                                    <div class="play_icon"></div>
                                    <div class="more_icon"></div>
                                    <div class="toggle" style="display: none">
                                        <p>공유하기</p>
                                        <div class="line"></div>
                                        <p>찜하기</p>
                                    </div>
                                </div>`
                $('#youtube_recommend_content').append(temp_html)
            }
}

// News
function news_content_add(news_crawling_data_list){
    for (let i = 0; i <news_crawling_data_list.length; i++) {
                let news_row = news_crawling_data_list[i]
                let temp_html = `<div class="profile_like_news">
                                        <li>
                                            <div class="profile_like_news_image"></div>
                                            <div class="profile_like_news_info">
                                                <div class="profile_like_news_title">${news_row[2]}</div>
                                                <div class="profile_like_news_content">${news_row[4]}
                                                </div>
                                                <div class="profile_like_news_company">${news_row[1]}</div>
                                            </div>
                                            <div class="profile_like_news_toggle" style="display: none;">
                                                <p>공유하기</p>
                                            </div>
                                            <div class="profile_like_news_button">
                                                <div class="profile_like_news_setting"></div>
                                                <div class="profile_like_news_heart"></div>
                                            </div>

                                        </li>
                                    </div>`
                //
                $('#news_recommend_content').append(temp_html)
            }
}

// shopping
function shopping_content_add(shopping_crawling_data_list){
    for (let i = 0; i <shopping_crawling_data_list.length; i++) {
                let shopping_row = shopping_crawling_data_list[i]
                let temp_html = `<div class="recommend_shopping_search_content">
                                    <div class="more_icon" id="shopping_recommend_${i}" onclick="more_open_or_off(this.id)"></div>
                                    <div class="toggle" style="display: none">
                                        <p>공유하기</p>
                                        <div class="line"></div>
                                        <p>찜하기</p>
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

function more_open_or_off(id){

}
