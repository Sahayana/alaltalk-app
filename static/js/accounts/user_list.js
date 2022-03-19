
// 친구 찾기
function searchUser(){
    $("#search-modal-btn").click();
    let query = "";
    query = $("#search_input").val();
    
    let userListUri = $(".search_bar").data('uri');   

    $.ajax({
        type: 'GET',
        url: `${userListUri}?q=${query}`,         
        success: function (response) {
            // console.log(response["result"]);
            let friends = response["result"];
            friends.forEach(friend => {
                appendResult(friend);
            });
                             
        }
    });    

    return false;
}

// 검색한 친구 리스트 모달에 출력
function appendResult(friend){
    let tempHtml = `
            <div class="user_box">
                <div class="user_img"></div>
                <div class="info_group">
                    <div class="user_name">${friend['nickname']}</div>
                    <div class="user_id">${friend['email']}</div>
                </div>
                <div class="btn apply_follow">친구신청</div>
            </div>
    `

    $(".modal-body").append(tempHtml);
}