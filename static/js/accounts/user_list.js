
// 친구 찾기
function searchUser(){
    $(".search_result").empty();

    let query = "";
    query = $("#search_input").val();

    if (query==='' || query==='.'){
        return;
    }

    if (query.length < 3){
        alert("2글자 이상 입력해주세요.");
        return;
    }
    
    let userListUri = $(".search_bar").data('uri');   

    $.ajax({
        type: 'GET',
        url: `${userListUri}?q=${query}`,         
        success: function (response) {
            // console.log(response["result"]);
            let friends = response["result"];
            friends.forEach(friend => {
                console.log(friend);
                appendResult(friend);
            });

            $(".user_list").css('display', 'none');
            $(".search_result").css('display', 'block');                             
        }
    });    

    return false;
}

// 검색한 친구 리스트 모달에 출력
function appendResult(friend){
    let tempHtml =''
    if (friend[1] === 0){
        tempHtml = `
        <div class="user_box">
            <div class="user_img">
                <img src="https://alaltalk.s3.ap-northeast-2.amazonaws.com/${friend[0]['img']}" alt="friend_p_img" srcset="">
            </div>
            <div class="info_group">
                <div class="user_name">${friend[0]['nickname']}</div>
                <div class="user_id">${friend[0]['email']}</div>
            </div>
            <div class="btn already_friend"> 친구 </div>
        </div>
    `;

    }else if (friend[1] === 2){
        tempHtml = `
        <div class="user_box">
            <div class="user_img">
                <img src="https://alaltalk.s3.ap-northeast-2.amazonaws.com/${friend[0]['img']}" alt="friend_p_img" srcset="">
            </div>
            <div class="info_group">
                <div class="user_name">${friend[0]['nickname']}</div>
                <div class="user_id">${friend[0]['email']}</div>
            </div>
            <div class="btn apply_follow" onclick=sendRequest(${friend[0]['id']})>친구신청</div>
        </div>
    `;

    }else{
        tempHtml = `
        <div class="user_box">
            <div class="user_img">
                <img src="https://alaltalk.s3.ap-northeast-2.amazonaws.com/${friend[0]['img']}" alt="friend_p_img" srcset="">
            </div>
            <div class="info_group">
                <div class="user_name">${friend[0]['nickname']}</div>
                <div class="user_id">${friend[0]['email']}</div>
            </div>
            <div class="btn already_friend"> 나 </div>
        </div>
    `;

    }    
    
    $(".search_result").append(tempHtml);
}


// 친구신청
function sendRequest(receiver_id){

    $.ajax({
        type: 'GET',
        url: `/accounts/friends/request/${receiver_id}`,         
        success: function (response) {
            console.log(response);
            if (response["msg"] === "already"){
                alert("이미 친구 요청한 회원입니다.");
                return;
            }else{
                alert("친구요청을 보냈습니다.");
                window.location.reload();
            }
                             
        }
    });    
    

}


$(document).ready(function(){       

    // 친구 리스트 이동
    let friendListIcon = $(".user_icon");
    friendListIcon.on('click', function(){
        window.location.href = `/accounts/friends/`;
    });

    // 마이페이지 이동
    let myPageIcon = $(".mypage_icon");
    myPageIcon.on('click', function(){
        window.location.href = `/accounts/mypage/`;
    });

    // 채팅 이동
    let ChatIcon = $(".chat_icon");
    ChatIcon.on('click', function(){
        window.location.href = `/chat/`;
    })
});


function friend_chat(id){
    window.location.href= `/chat/`+ id;
}