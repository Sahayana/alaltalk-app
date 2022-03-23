$(document).ready(function () {
    $('#left_wrap').load("/api/search/chat_list");
    $('#right_wrap').load("/api/search/chat");
})

function switch_chat() {
    $('#right_wrap').empty();
    $('#left_wrap').empty();
    $('#left_wrap').load("/api/search/chat");
    $('#right_wrap').load("/api/search/recommend");
    setTimeout(function(){
        click_recommend_function();
        give_event()
    }, 100)
}

function toggle_recommend(){
    let toggle_menu = document.getElementById('toggle_content')
    if(toggle_menu.style.display!=='none'){
        toggle_menu.style.display='none'
    }
    else{
        toggle_menu.style.display='block'
    }
}
