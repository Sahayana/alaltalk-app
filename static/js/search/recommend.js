window.onload = function(){
    console.log('page is onload!')
    $.ajax({
        type: 'POST',
        url: '/api/search/crawling',
        data: {"target": "운동"},
        datatype: 'form',
        success: function(response){
            console.log(response)
            console.log(response['all_response']['youtube'])
        }
    })
}


// 탭 이동 함수
function move_category(target_id){
    console.log('function is working')
    document.getElementById('recommend_youtube_container').style.display='none'
    document.getElementById('recommend_news_container').style.display='none'
    document.getElementById('recommend_book_container').style.display='none'
    document.getElementById('recommend_shopping_container').style.display='none'
    document.getElementById(target_id).style.display='block'
}

// 각 nav_bar에 click event 주기
let navs = document.getElementsByClassName('recommend_nav')
let navs_list_id = ['recommend_youtube_container','recommend_news_container','recommend_book_container','recommend_shopping_container']
for(let i=0; i<navs.length; i++){
    let nav_row = navs[i].children
    for(let j=0;j<nav_row.length;j++){
        nav_row[j].addEventListener('click',function(){
            move_category(navs_list_id[j])
        })
    }
}