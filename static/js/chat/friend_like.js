function take_like_content_to_me(id){
        let category = id.split('_')[0]
        let id_number = id.split('_')[1]
        if(category==='youtube'){
            console.log('youtube content to me!')
            youtube_take_me(id_number)
        } else if(category ==='news'){
            console.log('news content to me!')
            news_take_me(id_number)
        } else if(category ==='book'){
            console.log('book content to me!')
            book_take_me(id_number)
        } else if(category ==='shopping'){
            console.log('shopping content to me!')
            shopping_take_me(id_number)
        } else{
            console.log('Wrong Category!')
        }
    }

function youtube_take_me(id){
    $.ajax({
        type:'POST',
        url: '/api/chat_room/youtube',
        data: {
            'id': id
        },
        success: function(response){
            console.log('youtube_take_funcstion result:', response['result'])
            alert('저장!')
        }
    })
}


function news_take_me(id){
    $.ajax({
        type:'POST',
        url: '/api/chat_room/news',
        data: {
            'id': id
        },
        success: function(response){
            console.log('youtube_take_funcstion result:', response['result'])
            alert('저장!')
        }
    })
}


function book_take_me(id){
    $.ajax({
        type:'POST',
        url: '/api/chat_room/book',
        data: {
            'id': id
        },
        success: function(response){
            console.log('youtube_take_funcstion result:', response['result'])
            alert('저장!')
        }
    })
}



function shopping_take_me(id){
    $.ajax({
        type:'POST',
        url: '/api/chat_room/shopping',
        data: {
            'id': id
        },
        success: function(response){
            console.log('youtube_take_funcstion result:', response['result'])
            alert('저장!')
        }
    })
}

/////////////////////////////////친구 관심 키워드///////////////////////////////////////////

function get_friend_recommend() {
    let friend_id = document.getElementById('friend_id').innerText;
    console.log(friend_id);
    $.ajax({
            url: "/accounts/friend/recommend/keyword/",
            type: 'GET',
            data: {"friend_id": friend_id},
            enctype: 'multipart/form-data',
            async: false,
            success: function (response) {
                console.log(response.friend_keywords);
                let friend_keyword = response.friend_keywords;
                for (let i=0; i < friend_keyword.length; i++) {
                    let temp_html = `<div class="friend_keyword">${friend_keyword[i]}</div>`

                    $('.friend_like_recommend_container').append(temp_html)
                }

            },
            error: function (request, status, error) {
                console.log('친구 추천키워드 에러')

                console.log(request, status, error)
            }

        });
}

$(document).ready(function(){
    get_friend_recommend()
});