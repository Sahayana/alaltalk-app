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

function see_our_page() {
    var start_scroll = $('html');
    let row = document.getElementById('landing_row_1');
    let scroll_position = row.offsetTop + row.offsetHeight
    var page = 3;

    start_scroll.animate({scrollTop :scroll_position},500);

}
// function see_our_page(){
//     var start_scroll = $('html');
//     let row = document.getElementById('landing_row_1');
//     let scroll_position = row.offsetTop + row.offsetHeight
//     // window.scrollTo({top: scroll_position, behavior: 'smooth'});
//     var page = 2;
//
//     // $('#landing_row_1').animate({scrollTop:$(this.hash).offset().top}, 500);
//     start_scroll.animate({scrollTop :scroll_position},500);
//     $(window).on("wheel", function(e) {
//     if(start_scroll.is(":animated")) return;
//     if(e.originalEvent.deltaY > 50) {
//         if(page == 7) return;
//         page++;
//     } else if(e.originalEvent.deltaY < 50) {
//         if(page == 1) return;
//         page--;
//     }
//     if(page > 4) {
//         var posTop =(page-1) * (scroll_position);
//     } else {
//         var posTop =(page-1) * scroll_position;
//     }
//
//     start_scroll.animate({scrollTop : posTop});
// })
//
// }






