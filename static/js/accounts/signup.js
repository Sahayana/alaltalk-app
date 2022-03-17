// Input 정규표현식

function isEmail(email) {
    var exp = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
    return exp.test(email)
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
    if(!isImg(img.value)){
        alert('이미지 파일만 업로드 가능합니다.')
        return;
    }

    if (img.files && img.files[0]) {  

        let reader = new FileReader();
        reader.onload = function (e) {
            profileImgDiv.style.backgroundImage = `url(${e.target.result})`;
            profileImgDiv.style.backgroundSize = 'cover';
            profileImgDiv.style.backgroundRepeat = 'no-repeat';
        }        
        reader.readAsDataURL(img.files[0]);
    }
      
    
}


$(document).ready(function(){
    
    // Profile Image upload
    let profileImgDiv = document.querySelector('.signup-profile-img');

    profileImgDiv.addEventListener('click', function(){
        document.querySelector('#profile-img').click();
    })

    // Profile Image Preview
    let profileImgInput = document.querySelector('#profile-img');
    profileImgInput.addEventListener('change', function(){
        previewImg(this);
        document.querySelector('.profile-img-default').style.display ='none';
        document.querySelector('.profile-img-p').style.display ='none';
    })


    // Email vailidation
    let email = document.querySelector("#email");
    let emailDiv = document.querySelector(".email");
    email.addEventListener('keyup', function (){     
        // 조건에 맞지 않을 때는 빨간색, 조건을 충족했다면 초록색
        
        let e_error = document.querySelector("#e_error");
        if (!isEmail(email.value)){
            emailDiv.style.border = '2px solid red';        
            e_error.innerText = "올바른 이메일 형식이 아닙니다."
            e_error.style.visibility ='visible';
            return false
        }else {
            emailDiv.style.border = '2px solid green';        
            e_error.style.visibility ='hidden';
        }
    })

    // Password Validation
    let password = document.querySelector("#current-password");
    let passwordCheck = document.querySelector("#check-password");

    let passwordDiv = document.querySelector(".password");
    let passwordCheckDiv = document.querySelector(".password2");

    password.addEventListener('keyup', function(){
        let pwd_error = document.querySelector('#pwd_error');
        if (!isPw(password.value)){
            passwordDiv.style.border = '2px solid red';        
            pwd_error.innerText = "영문과 숫자 조합의 8-20자의 비밀번호를 설정해주세요.";
            pwd_error.style.visibility ='visible';
            return false
        }else {
            passwordDiv.style.border = '2px solid green';        
            pwd_error.style.visibility ='hidden';

        }

    })

    passwordCheck.addEventListener('keyup', function (){     
        let pwd_check_error = document.querySelector('#pwd_check_error');
        if (password.value !== passwordCheck.value){
            passwordCheckDiv.style.border = '2px solid red';        
            pwd_check_error.innerText = "패스워드를 확인해주세요.";
            pwd_check_error.style.visibility ='visible';
            return false
        }else {
            passwordCheckDiv.style.border = '2px solid green';        
            pwd_check_error.style.visibility ='hidden';
        }

    })


    // Nickname Validation

    let nickName = document.querySelector("#nickname");
    let nickNameDiv = document.querySelector(".nickname");

    nickName.addEventListener('keyup', function (){ //키를 놓을 때 발생하는 이벤트
        
        let name_error = document.querySelector('#name_error');

        if (nickName.value.length < 3){
            nickNameDiv.style.border = '2px solid red';        
            name_error.innerText = "닉네임은 3자리 이상이여야 합니다.";
            name_error.style.visibility ='visible';
            return false
        }else {
            nickNameDiv.style.border = '2px solid green';        
            name_error.style.visibility ='hidden';
        }
    })

    // signBtn activation
    let agreeChecked = document.querySelector(".agree-checkbox");
    let signBtn = document.getElementById("signBtn");


    $("#agree-cb").addEventListener('click', function(){
        $("#agree-cb").prop('checked',true);
    })

    let checked = $("#agree-cb").is(":checked");

    if (checked){
            signBtn.disabled = false;
        }else{
            signBtn.disabled = true;
        }


    // Returning to login

    let loginBtn = document.querySelector(".loginBtn");
    loginBtn.addEventListener('click', function(){
        window.location.href = '/'
    })


});

