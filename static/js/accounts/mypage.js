//프로필 변경 버튼 클릭

function profile_change_check(){    
    
    document.getElementById('password-again-input').value = "";

    let change = document.getElementById('profile_change');
    let follow = document.getElementById('profile_follow');
    let like = document.getElementById('profile_like');
    change.style.backgroundColor = '#7657CE';
    change.style.color = 'white';
    change.style.fontWeight = 'bold';
    change.style.border = 'none';

    follow.style.backgroundColor = 'transparent';
    follow.style.color = '#A185F2';
    follow.style.fontWeight = 'normal';
    follow.style.border = '2px solid #A185F2';

    like.style.backgroundColor = 'transparent';
    like.style.color = '#A185F2';
    like.style.fontWeight = 'normal';
    like.style.border = '2px solid #A185F2';

    document.getElementById('profile_right_default').style.display='none'
    document.getElementById('profile_follow_container').style.display='none'
    document.getElementById('profile_like_container').style.display='none'
    document.getElementById('profile_change_container').style.display='none'

    document.getElementById('profile_auth_container').style.display='block'
    
}

// 프로필 변경 접근을 위한 비밀번호 재확인
function authCheck(){
    let passwordAgain = $("#password-again-input").val();  
    
    if (passwordAgain == ''){
        return;
    }

    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });

    $.ajax({
        type: 'POST',
        url: '/accounts/mypage/authcheck/',  
        dataType: "json",
        data: {"password":passwordAgain},        
        success: function (response) {
            if (response["msg"] === "ok"){                              
                profile_change();                
            }else{
                $("#password-again-helper").text("비밀번호를 확인해주세요.");
                $("#password-again-helper").css("color", "red");
            }
                    
        }
    })
}



//프로필 변경
function profile_change(){    

    document.getElementById('profile_right_default').style.display='none'
    document.getElementById('profile_follow_container').style.display='none'
    document.getElementById('profile_like_container').style.display='none'
    document.getElementById('profile_auth_container').style.display='none'
    document.getElementById('profile_change_container').style.display='block'
}

//프로필 팔로우 관리 클릭
function profile_follow(){
    let change = document.getElementById('profile_change');
    let follow = document.getElementById('profile_follow');
    let like = document.getElementById('profile_like');
    follow.style.backgroundColor = '#7657CE';
    follow.style.color = 'white';
    follow.style.fontWeight = 'bold';
    follow.style.border = 'none';

    change.style.backgroundColor = 'transparent';
    change.style.color = '#A185F2';
    change.style.fontWeight = 'normal';
    change.style.border = '2px solid #A185F2';

    like.style.backgroundColor = 'transparent';
    like.style.color = '#A185F2';
    like.style.fontWeight = 'normal';
    like.style.border = '2px solid #A185F2';

    document.getElementById('profile_right_default').style.display='none'
    document.getElementById('profile_follow_container').style.display='block'
    document.getElementById('profile_like_container').style.display='none'
    document.getElementById('profile_auth_container').style.display='none'
    document.getElementById('profile_change_container').style.display='none'
}

//프로필 찜
function profile_like(){
    let change = document.getElementById('profile_change');
    let follow = document.getElementById('profile_follow');
    let like = document.getElementById('profile_like');
    like.style.backgroundColor = '#7657CE';
    like.style.color = 'white';
    like.style.fontWeight = 'bold';
    like.style.border = 'none';

    follow.style.backgroundColor = 'transparent';
    follow.style.color = '#A185F2';
    follow.style.fontWeight = 'normal';
    follow.style.border = '2px solid #A185F2';

    change.style.backgroundColor = 'transparent';
    change.style.color = '#A185F2';
    change.style.fontWeight = 'normal';
    change.style.border = '2px solid #A185F2';

    document.getElementById('profile_right_default').style.display='none'
    document.getElementById('profile_follow_container').style.display='none'
    document.getElementById('profile_like_container').style.display='block'
    document.getElementById('profile_auth_container').style.display='none'
    document.getElementById('profile_change_container').style.display='none'
    youtube_like()
}


//찜목록 카테고리

//youtube카테고리 클릭
function youtube_like(){
    document.getElementById('youtube').style.color = '#7657CE';
    document.getElementById('news').style.color = '#d2d2d2';
    document.getElementById('book').style.color = '#d2d2d2';
    document.getElementById('shopping').style.color = '#d2d2d2';

    document.getElementById('profile_like_youtube').style.display = 'block';
    document.getElementById('profile_like_news').style.display = 'none';
    document.getElementById('profile_like_book').style.display = 'none';
    document.getElementById('profile_like_shopping').style.display = 'none';
}

function news_like(){
    document.getElementById('news').style.color = '#7657CE';
    document.getElementById('youtube').style.color = '#d2d2d2';
    document.getElementById('book').style.color = '#d2d2d2';
    document.getElementById('shopping').style.color = '#d2d2d2';

    document.getElementById('profile_like_news').style.display = 'block';
    document.getElementById('profile_like_youtube').style.display = 'none';
    document.getElementById('profile_like_book').style.display = 'none';
    document.getElementById('profile_like_shopping').style.display = 'none';
}

function book_like(){
    document.getElementById('book').style.color = '#7657CE';
    document.getElementById('youtube').style.color = '#d2d2d2';
    document.getElementById('news').style.color = '#d2d2d2';
    document.getElementById('shopping').style.color = '#d2d2d2';

    document.getElementById('profile_like_book').style.display = 'block';
    document.getElementById('profile_like_youtube').style.display = 'none';
    document.getElementById('profile_like_news').style.display = 'none';
    document.getElementById('profile_like_shopping').style.display = 'none';
}

function shopping_like(){
    document.getElementById('shopping').style.color = '#7657CE';
    document.getElementById('youtube').style.color = '#d2d2d2';
    document.getElementById('news').style.color = '#d2d2d2';
    document.getElementById('book').style.color = '#d2d2d2';

    document.getElementById('profile_like_shopping').style.display = 'block';
    document.getElementById('profile_like_youtube').style.display = 'none';
    document.getElementById('profile_like_news').style.display = 'none';
    document.getElementById('profile_like_book').style.display = 'none';
}

//공유하기 토글 열기
function toggle_open(){

}

function isPw(pw) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(pw);
}



function isImg(file) {
    let regExp = /(.*?)\.(jpg|jpeg|png|JPG|JPEG|PNG)$/;
    return regExp.test(file);
}


function previewImg(img) {

    let profileImg = document.getElementById("profile-img-modified");

    if(!isImg(img.value)){
        alert('이미지 파일만 업로드 가능합니다.')
        return;
    }

    if (img.files && img.files[0]) {  

        let reader = new FileReader();
        reader.onload = function (e) {            
            profileImg.src = e.target.result;
        }        
        reader.readAsDataURL(img.files[0]);
    }    
}


// 프로필변경

function  profileChange(){
    let nickName = $("#profile-nickname").val();
    let bio = $("#profile-bio").val();
    let profileImg = $("#profile-img")[0].files[0];
    let password = $("#profile-password-change").val();


    let formData = new FormData();
    formData.append("nickname", nickName);       
    formData.append("img", profileImg);
    formData.append("bio", bio);
    if (password.length > 0 && !isPw(password)){
        alert("비밀번호를 확인해주세요.");
        return;
    }else{
        formData.append("password", password);
    }
    // for (var pair of formData.entries()) {
    //     console.log(pair[0]+ ', ' + pair[1]);
    // }

    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });

    $.ajax({
        type: 'POST',
        url: '/accounts/mypage/modify/',  
        cache: false,
        contentType: false,
        processData: false,
        mimeType: "multipart/form-data",
        data: formData, 
        success: function (response) {
            console.log(response)
            alert("회원정보를 변경하였습니다.");
            window.location.reload();            
        }
    })

}


// 친구 요청 수락
function acceptRequest(requestId){    
    // let requestId = $(this).data("id");
    // console.log(this);
    console.log(requestId);

    $.ajax({
        type: 'GET',
        url: `/accounts/friends/accept/${requestId}`,         
        success: function (response) {
            console.log(response);
            if (response["msg"] === "accepted"){
                alert("친구 요청을 수락하였습니다.");
                window.location.reload();
                profile_follow();
            }else{
                alert("문제가 발생하였습니다.");
                return;
            }
                             
        }
    });    
}

// 친구 요청 거절
function declineRequest(requestId){

    $.ajax({
        type: 'GET',
        url: `/accounts/friends/decline/${requestId}`,         
        success: function (response) {
            console.log(response);
            if (response["msg"] === "declined"){
                alert("친구 요청을 거절하였습니다.");
                window.location.reload();
                profile_follow();
            }else{
                alert("문제가 발생하였습니다.");
                return;
            }
                             
        }
    });    
    
}



function set_animation_more() {
    let shopping_content = document.getElementsByClassName('recommend_toggle')
    for (let i = 0; i < shopping_content.length; i++) {
        shopping_content[i].addEventListener('mouseover', function () {
            shopping_content[i].style.animation = 'appear_toggle 1s ease-out forwards'

        })
        shopping_content[i].addEventListener('mouseout', function () {
            shopping_content[i].style.animation = ''
            shopping_content[i].style.opacity = '0'

        })
    }
}





$(document).ready(function(){

    set_animation_more()
    
    // 프로필 이미지 업로드
    let profileImgDiv = document.querySelector('.profile_image_change');

    profileImgDiv.addEventListener('click', function(){
        document.getElementById('profile-img').click();
    })

    // 프로필 이미지 프리뷰
    let profileImgInput = document.querySelector('#profile-img');
    profileImgInput.addEventListener('change', function(){
        previewImg(this);        
    })

    // 친구 리스트 이동
    let friendListIcon = $(".user_icon");
    friendListIcon.on('click', function(){
        window.location.href = `/accounts/friends/`;
    })

    // 마이페이지 이동
    let myPageIcon = $(".mypage_icon");
    myPageIcon.on('click', function(){
        window.location.href = `/accounts/mypage/`;
    })


    // 채팅 이동
    let ChatIcon = $(".chat_icon");
    ChatIcon.on('click', function(){
        window.location.href = `/chat/`;
    })

    let profileChangeBtn = document.querySelector('#profile_change_button');

    // 닉네임 유효성 검사

    let nickName = document.querySelector("#profile-nickname");
    let nameError = document.querySelector("#name_error");

    nickName.addEventListener('keyup', function (){ //키를 놓을 때 발생하는 이벤트       
        
        if (nickName.value.length < 3){                   
            nameError.innerText = "닉네임은 3자리 이상이여야 합니다.";
            nameError.style.visibility ='visible';
            profileChangeBtn.disabled = true;           
            return false;
        }else {            
            profileChangeBtn.disabled = false;
            nameError.style.visibility ='hidden'; 
        }
    })

    // 비밀번호 유효성 검사

    let password = document.querySelector("#profile-password-change");
    let passwordCheck = document.querySelector("#profile-password-check");
    
    let pwdError = document.querySelector("#pwd_error");
    let pwdCheckError = document.querySelector("#pwd_check_error");

    password.addEventListener('keyup', function(){        
        if (!isPw(password.value)){             
            pwdError.innerText = "영문과 숫자 조합의 8-20자의 비밀번호를 설정해주세요.";
            pwdError.style.visibility ='visible';
            profileChangeBtn.disabled = true;               
            return false;
        }else{                 
            pwdError.style.visibility ='hidden';
            profileChangeBtn.disabled = false;
        }

    })

    passwordCheck.addEventListener('keyup', function (){     
        
        if (password.value !== passwordCheck.value){                   
            pwdCheckError.innerText = "패스워드를 확인해주세요.";
            pwdCheckError.style.visibility ='visible';  
            profileChangeBtn.disabled = true;             
            return false
        }else {                  
            pwdCheckError.style.visibility ='hidden';
            profileChangeBtn.disabled = false;
        }

    })
    

});