
function login(){
    let email = document.getElementById("current-email").value
    let password = document.getElementById("current-password").value
    console.log(email);
    console.log(password);

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
            console.log(response)
            if (response["msg"] == "error" ){
                alert("이메일 혹은 비밀번호를 확인해주세요");
                return;
            }else{
                window.location.replace('/');
            };         
        }
    });    

};