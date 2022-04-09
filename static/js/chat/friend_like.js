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
        }
    })
}