
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
            // console.log(response)
            if (response["msg"] == "error" ){
                alert("이메일 혹은 비밀번호를 확인해주세요");
                return;
            }else{
                window.location.replace('/');
            };         
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