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
    let row = document.getElementById('landing_row_4')
    let scroll_position = row.offsetTop + row.offsetHeight
    window.scrollTo({top: scroll_position, behavior: 'smooth'});
}





