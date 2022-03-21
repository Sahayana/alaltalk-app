

function click_recommend_function() {
    console.log('page is onload!')
    // document.getElementById('recommend_spinner').style.display='none'
    $.ajax({
        type: 'POST',
        url: '/api/search/crawling',
        data: {"target": "노래"},
        datatype: 'form',
        success: function (response) {
            for (let i = 0; i < response['all_response']['youtube'].length; i++) {
                let youtube_row = response['all_response']['youtube'][i]
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
    })
}


// 탭 이동 함수
function move_category(target_id) {
    console.log('function is working')
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

function give_event(){
    console.log('give event!')
    let navs = document.getElementsByClassName('recommend_nav')
    let navs_list_id = ['recommend_youtube_container', 'recommend_news_container', 'recommend_book_container', 'recommend_shopping_container']
    for (let i = 0; i < navs.length; i++) {
        console.log('hi')
        let nav_row = navs[i].children
        for (let j = 0; j < nav_row.length; j++) {
            console.log(j)
            nav_row[j].addEventListener('click', function () {
                move_category(navs_list_id[j])
            })
        }
}
}