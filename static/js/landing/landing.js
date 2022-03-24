var swiper_content = new Swiper(".landing_interest_slide", {
    navigation: {
        nextEl: ".landing_slide_next_button",
    },
    loop: true
});

var swiper_mac = new Swiper(".landing_content_row_4_left_mac_body", {
    navigation: {
        nextEl: ".landing_content_row_4_next_button",
    },
    loop: true
});

document.addEventListener('scroll', function (){
    let header = window.document.getElementById('landing_header')
    let value = window.scrollY
    let row1 = window.document.getElementById('landing_row_1')
    let row2 = window.document.getElementById('landing_row_2')
    let row3 = window.document.getElementById('landing_row_3')
    let row4 = window.document.getElementById('landing_row_4')
    let row5 = window.document.getElementById('landing_row_5')

    if(value < 40){
        header.style.animation = 'appear_header 2s ease-out forwards';
    } else{
        header.style.animation = 'disappear_header 1s ease-out forwards';
    }

})

function see_our_page(){
    // $('#landing_row_1').animate({scrollTop:$(this.hash).offset().top}, 500);
    let row = document.getElementById('landing_row_1')
    let scroll_position = row.offsetTop + row.offsetHeight
    window.scrollTo({top: scroll_position, behavior: 'smooth'});

    // $(".landing_content_row").each(function () {
    //             // 개별적으로 Wheel 이벤트 적용 mousewheel(IE/chrome/opera) DOMMouseScroll(FF)
    //             $(this).on("mousewheel DOMMouseScroll", function (e) {
    //                 e.preventDefault();
    //                 var delta = scroll_position;
    //                 /* IE */
    //                 if (!event) event = window.event;
    //                 //휠에 대한 정보 얻기 파이어폭스 외 IE/Chrome/Opera = wheelDelta
    //                 if (event.wheelDelta) {
    //                     delta = event.wheelDelta / 50;
    //                     //평균 50~120 사이로 요소의 인식높이에 따라 다름(한 화면(height100%)기준일떄는 120
    //                     if (window.opera) delta = -delta;
    //                 //휠에 대한 정보 얻기 Mozilla FF = detail
    //                 } else if (event.detail) delta = -event.detail / 3;
    //                 var moveTop = null;
    //                 // 마우스휠을 위에서 아래로
    //                 if (delta < 0) {
    //                     if ($(this).next() != undefined) {
    //                         moveTop = $(this).next().offset().top;
    //                     }
    //                 // 마우스휠을 아래에서 위로
    //                 } else {
    //                     if ($(this).prev() != undefined) {
    //                         moveTop = $(this).prev().offset().top;
    //                     }
    //                 }
    //                 // 화면 이동 0.8초(800)
    //                 $("html,body").stop().animate({
    //                     scrollTop: moveTop + 'px'
    //                 }, {
    //                     duration: 300, complete: function () {
    //                     }
    //                 });
    //             });
    //         });

}






