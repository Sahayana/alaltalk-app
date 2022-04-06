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

window.addEventListener("scroll", function() {
    let current_scroll = window.scrollY;
    let row4 = window.document.getElementById('landing_row_4')
    let scroll_position4 = row4.offsetTop + row4.offsetHeight

    let see_btn = window.document.getElementById('landing_see_our_page');

    if (current_scroll >= scroll_position4-1) {
        see_btn.style.display ="none"
    } else {
        see_btn.style.display ="flex"
    }
});



function see_our_page() {
    let start_scroll = $('html');
    let current_scroll = window.scrollY;

    let row1 = window.document.getElementById('landing_row_1')
    let row2 = window.document.getElementById('landing_row_2')
    let row3 = window.document.getElementById('landing_row_3')
    let row4 = window.document.getElementById('landing_row_4')

    console.log(current_scroll);

    let scroll_position1 = row1.offsetTop + row1.offsetHeight
    let scroll_position2 = row2.offsetTop + row2.offsetHeight
    let scroll_position3 = row3.offsetTop + row3.offsetHeight
    let scroll_position4 = row4.offsetTop + row4.offsetHeight

    let scroll_position = 0;
    if (current_scroll < scroll_position1-1) {
        scroll_position = scroll_position1;
    } else if (current_scroll>= scroll_position1-1 && current_scroll < scroll_position2-1) {
        scroll_position = scroll_position2;
    } else if (current_scroll>= scroll_position2-1 && current_scroll < scroll_position3-1) {
        scroll_position = scroll_position3;
    } else {
        scroll_position = scroll_position4;

    }


    start_scroll.animate({scrollTop :scroll_position},500);

}