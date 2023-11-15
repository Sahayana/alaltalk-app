$(document).ready(function () {
    $('#left_wrap').load("/api/search/chat_list");
    // $('#left_wrap').load("/chat/room/7/");
    $('#right_wrap').load("/api/search/chat");

    // 친구 리스트 이동
    let friendListIcon = $(".user_icon");
    friendListIcon.on('click', function () {
        window.location.href = `/friend/v1/friends`;
    })

    // 마이페이지 이동
    let myPageIcon = $(".mypage_icon");
    myPageIcon.on('click', function () {
        window.location.href = `/account/v1/mypage`;
    })

    // 채팅 이동
    let ChatIcon = $(".chat_icon");
    ChatIcon.on('click', function () {
        window.location.href = `/api/search/`;
    })
})

function switch_chat() {
    $('#right_wrap').empty();
    $('#left_wrap').empty();
    $('#left_wrap').load("/api/search/chat");
    $('#right_wrap').load("/api/search/recommend");
    setTimeout(function () {
        reload();
        console.log('recommend_toggle!! -> ', document.getElementById('recommend_toggle'))
    }, 500)
    console.log('switch_chat()!')
}

function toggle_recommend() {
    let toggle_menu = document.getElementById('toggle_content')
    if (toggle_menu.style.display !== 'none') {
        toggle_menu.style.display = 'none'
    }
    else {
        toggle_menu.style.display = 'block'
    }
}