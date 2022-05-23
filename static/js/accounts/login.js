
function login(){
    let email = document.getElementById("current-email").value
    let password = document.getElementById("current-password").value
    // console.log(email);
    // console.log(password);

    let formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);  

    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });

    $.ajax({
        type: 'POST',
        url: '/accounts/login/',  
        cache: false,
        contentType: false,
        processData: false,          
        data: formData, 
        success: function (response) {          
            
            if (response["token"] == "NOT_ACTIVATED"){
                alert("이메일 인증을 완료해주세요.");
                return;
            }else if (response["token"] == "UNVALID_PASSWORD"){
                alert("잘못된 비밀번호입니다.");
                return;
            }else if (response["token"] == "NOT_REGISTERD"){
                alert("등록되지 않은 회원입니다.");
                return;                            
            }else{
                $.cookie("Authorization", response["token"]);
                console.log($.cookie('Authorization'));
                window.location.replace('/');
            }         
        }
    });    

};


// 임시 비밀번호 전송

function tempPw(){
    let userEmail = ""; 
    userEmail = $("#email-find").val();
    // console.log(userEmail);
    
    $.ajax({
        type: 'GET',
        url: `/accounts/login/temp?q=${userEmail}`,         
        success: function (response) {
            if (response["msg"] == "none-user"){
                alert("존재하지 않는 이메일 주소입니다.");
                return;
            }else{
                alert("임시 비밀번호가 전송되었습니다.");
                window.location.reload();
            }
                             
        }
    });    
    
}

// 회원가입 페이지로 이동

function moveToSignUp(){
    window.location.href = '/accounts/signup/';
}