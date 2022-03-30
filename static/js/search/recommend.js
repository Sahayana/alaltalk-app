
// 채팅로그 받아오기
var chat_log = [];
function get_chat_log(){
   var link = document.location.href;
    console.log(link);
    let room_id = link.split('/');
    room_id = parseInt(room_id[5]);
    
    $.ajax({
        url: "/chat/chatlog/",
        type: 'POST',
        data: JSON.stringify({"room_id": room_id}),
        enctype: 'multipart/form-data',
        async: false,
        success: function (response) {
            console.log(response.chat_log);
            chat_log = response.chat_log;

        },
        error: function (request, status, error) {
            alert('error')

            console.log(request, status, error)
        }

    });
}



function click_recommend_function() {
    console.log('page is onload!')

    let form_data = new FormData()

    let chat_log = sentence = ["안녕하세요 이감국어교육연구소입니다.",
                   "너무 길어서 힘드네요...어쩔 수 없죠그런데 제목도 깁니다 ㅠ",
                   "오늘은 문학에서 등장하는 정확히 잡기 힘든 개념어를 이야기해보고자 합니다."
                   ,"댓글로 질문해주셨던 대화체 독백체로 일단 시작을 해보겠습니다.",
                   "일단 제목은 더럽게 길지만 요약하자면 일단 다음과 같이 분류할 수 있습니다.",
                   "1.대화의 형식2.대화체3.독백 = 독백체 = 독백적 발화(내적 독백과 다름) = 독백적 어조2번의 개념이 1번 개념을 포함하고 있으며2번 개념과 3번 개념은 다소 겹칩니다.",
                   "정리한다면서 더더욱 복잡해지고 있습니다.",
                   "네 이렇게나 어렵기 때문에 수능에서도 그렇게 엄격하게 출제한 적은 별로 없습니다.",
                   "일단 상황을 전제해 봅시다.A와 B 두 사람이 있습니다.",
                   "A가 B에게 말을 하고 B는 그에 대한 반응을 보입니다(대답을 합니다)A는 이 때 화자가 되고 B는 청자가 됩니다.",
                   "화자가 드러나고 청자가 화자의 말에 대한 반응을 합니다.이건 명백한 ‘대화’의 상황입니다.",
                   "대화의 상황은 대화의 형식을 빌려~ 라고 선지에서 주로 표현되며이것이 1번의 개념이 됩니다.그러면 1번의 대화와 2번의 대화체는 어떻게 다를까요?겉모습부터 봅시다.",
                   "대화체라는 녀석한테는 대화와 다르게 ‘체’가 추가되었습니다. ‘체’는 말투처럼 이해하시길 바랍니다.",
                   "즉, 대화체는 대화를 하는 듯한 말투입니다.그리고 실제 수능에서는 이와 비슷한‘말을 건네는 어투’로 가장 많이 등장합니다.다시 말해서 실제로 대화가 이루어질 필요는 없습니다.",
                   "다시 말해서 화자가 말을 건네고 있다면 청자의 반응이 존재하지 않더라도,청자의 존재만 뚜렷하게 인정된다면 대화체가 인정됩니다.왜? 실제 청자의 대답이 없더라도 충분히 대화를 하는 듯한 말투가 되기 때문입니다.",
                   "그러면 대화체면 대화다라는 말은 성립할까요?아닙니다. 아닐수도 있죠. 왜냐하면 청자의 반응이 없더라도 청자의 존재만 인정되면 대화체가 되지만 대화는 반드시 청자의 대답을, 반응을 필요로 하기 때문입니다.",
                   "그렇다면 대화는 대화체다 라는 말은 어떨까요?성립합니다. 왜냐하면 대화라면 화자도 말을 하고 청자도 그에 대한 반응을 하고 있으니 청자가 당연히 존재하므로 대화체로 인정되기 때문입니다.",
                   "다시 정리하겠습니다.1.대화체는 대화의 형식을포함합니다. 다만 대화체는 대화의 형식과다릅니다.2. 대화의 형식은 청자의 반응을 반드시 필요로 하지만 대화체는 청자의 반응을 필요로 하지는 않습니다. 화자의 존재만 전제되면 됩니다.3. 말을 건네는 어투도 대화체랑거의 같은 표현입니다..",
                   "다만 표현 조금 더 단단하게 잡고 간다면 대화체는 말을 건네는 어투일때도 인정이 되고대화적 형식일때도 인정이 되는 겁니다.",
                   "이제 마지막 개념을 잡아봅시다.독백이나 독백체나 독백적 발화나 독백적 어조나 다 같은 표현으로 생각해도 괜찮아요.독백은 말 그대로 화자가 혼자 말하는 상황 상상하시면 됩니다.그러면 청자는 반드시 필요할까요? 아뇨 없어도 됩니다.따라서 말을 하는 듯하는데 청자가 존재하지 않다면 독백, 독백체로 인정됩니다.",
                   "아 그러면 청자가 존재하면, 즉 드러나면 독백이 아닌가요?그렇지는 않습니다.다시 말해서 청자가 존재함이 인정되도, 실제로 청자의 반응이 없다면 이는 대화체로도 인정되지만 독백체로도 인정이 됩니다.",
                   "이제 슬슬 짜증이 나죠. 제가 그래서 2번 3번이 다소 겹친다고 합니다.이 지점때문에 수능 문학 개념에서 그렇게 큰 비중을 차지하지는 못하게 됩니다..그냥 이해하기 쉽게 이렇게 생각합시다.",
                   "화자가 말을 하고 청자가 존재하되 청자의 반응이 없다면 청자가 존재하기때문에 대화는 아니더라도 대화체가 인정이 된다. 거기에 일단 청자의 반응이 없기 때문에 화자가 혼자 말하고 있고 따라서 독백, 독백체, 독백적 발화, 독백체도 맞는 말이다…하고 잡아주시면 됩니다.",
                   "아 독백체 진짜 짜증나요! 싶으시면 이렇게 생각하셔도 됩니다.대부분의 시는 독백체입니다.독백체가 아닌 시들은 ‘말’처럼 안 느껴집니다.이런 시들은 어떤 느낌이 드냐면..정말 담담한 느낌이 드는 경우가 많습니다.그래서 주로 평서형 종결 어미와 명사형 종결 어미들이 쓰입니다.이런 경우가 아니라면 보통 정말 ‘말’을 하는 듯한 인상을 주고, 그러면 독백체라고 인정합니다.",
                   "다시 정리합니다.1.대화체와 독백체가 동시에 쓰일 수 있습니다.2.실제로 많은 시들이 독백체입니다.도움이 되셨길 바랍니다"];

    form_data.append('chat_log', chat_log);
    let machin_result = ''


    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/api/v1/textrank/",
        data: form_data,
        cache: false,
        processData: false,
        contentType: false,
        async: false,
        enctype: 'multipart/form-data',
        success: function (response) {
            // console.log(response.keyword)
            // console.log('추천시스템 성공!')
            machin_result  = response.keyword[0]

        },
        error: function (request, status, error) {
            alert('error')

            console.log(request, status, error)
        }

    });

    recommend_crawling_on(machin_result)

}

function make_reccommend(sentence){

}

function recommend_crawling_on(data){
    $.ajax({
        type: 'POST',
        url: '/api/search/crawling',
        data: {"target": '코딩'},
        datatype: 'form',
        async: false,
        success: function (response) {
            console.log(response['all_response']['book'])

            // 스피너 멈추기
            let spinners = document.getElementsByClassName('recommend_spinner')

            for (let k = 0; k < spinners.length; k++) {
                spinners[k].style.display = 'none';
            }

            // content 내용 붙이기
            youtube_content_add(response['all_response']['youtube'], 'crawling')
            news_content_add(response['all_response']['news'], 'crawling')
            book_content_add(response['all_response']['book'], 'crawling')
            shopping_content_add(response['all_response']['shopping'], 'crawling')


            // hovering_like
            clicked_like_heart()
            set_animation_more()

            // clicked_like
            // like_news()

            // search_bar
            initialize_search_bar()
        }
    })
}


// 탭 이동 함수
function move_category(target_id) {
    document.getElementById('recommend_youtube_container').style.display = 'none'
    document.getElementById('recommend_news_container').style.display = 'none'
    document.getElementById('recommend_book_container').style.display = 'none'
    document.getElementById('recommend_shopping_container').style.display = 'none'
    document.getElementById(target_id).style.display = 'block'
}

function give_event() {
    let navs = document.getElementsByClassName('recommend_nav')
    let navs_list_id = ['recommend_youtube_container', 'recommend_news_container', 'recommend_book_container', 'recommend_shopping_container']
    for (let i = 0; i < navs.length; i++) {
        let nav_row = navs[i].children
        for (let j = 0; j < nav_row.length; j++) {
            nav_row[j].addEventListener('click', function () {
                move_category(navs_list_id[j])
            })
        }
    }
}


// Crawling 붙여 넣기
// youtube
function youtube_content_add(youtube_crawling_data_list, type) {
    let content_type = ''
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        content_type = 's';
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < youtube_crawling_data_list.length; i++) {
        let youtube_row = youtube_crawling_data_list[i]
        let content_id = 'youtube_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(youtube_row[4]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="content_box" id="${content_id}">
                                    <iframe class="video_img" src="${youtube_row[0]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>ㅇ</iframe>
                                    <div class="video_title" style="font-size: 13px">${youtube_row[2]}</div>
                                    <div class="video_count">${youtube_row[3]}</div>
                                    <div class="recommend_youtube_heart_parent">
                                        <div class="recommend_like_heart recommend_youtube_like_heart" style="background-image: url(${heart_image})">
                                    </div>
                                </div>`
        if (content_type === 'c') {
            $('#youtube_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#youtube_search_content').append(temp_html)
        }
    }
}

// News
function news_content_add(news_crawling_data_list, type) {
    let content_type = ''
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        content_type = 's';
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < news_crawling_data_list.length; i++) {
        let news_row = news_crawling_data_list[i]
        let content_id = 'news_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(news_row[6]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="recommend_news_search_content" id="${content_id}">
                            <div class="recommend_news_search_content_image">
                                <a href="${news_row[3]}" target="_blank">
                                    <img src="${news_row[5]}">
                                </a>
                            </div>
                            <div class="recommend_news_search_content_desc">
                                <div class="recommend_news_search_content_desc_title">
                                    <p>${news_row[2]}</p>
                                </div>
                                <div class="recommend_news_search_content_desc_detail">
                                    <p>${news_row[4]}</p>
                                </div>
                                <div class="recommend_news_search_content_desc_footer">
                                    <div class="recommend_news_search_content_desc_footer_newspaper">
                                        <p>${news_row[0]}</p>
                                    </div>
                                    <div class="recommend_news_search_content_desc_footer_time">
                                        <p>${news_row[1]}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="recommend_news_search_content_more">
                                <div class="profile_like_news_toggle" onclick="content_do_share('${news_row[3]}')">
                                    <img src="/static/images/share.png">
                                </div>
                                <div class="recommend_like_heart" style="background-image: url('${heart_image}')">
                                    
                                </div>
                            </div>
                        </div>`
        //
        if (content_type === 'c') {
            $('#news_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#news_search_content').append(temp_html)
        }
    }
}

//book
function book_content_add(book_crawling_data_list, type) {
    let content_type = ''
    let display_value = 'none'
    let width = '102%'
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        width = '15vw'
        content_type = 's';
        display_value = 'flex'
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < book_crawling_data_list.length; i++) {
        let book_row = book_crawling_data_list[i]
        let content_id = 'book_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(book_row[7]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="content_box" id="${content_id}"> 
                            <div class="recommend_toggle recommend_book_toggle" style="width: ${width}">
                                <div class="profile_like_news_toggle" onclick="content_do_share('${book_row[5]}')">
                                    <img src="/static/images/share.png">
                                </div>
                                <div class="recommend_like_heart"
                                     style="background-image: url('${heart_image}')">
                                </div>
                            </div>
                            <a href="${book_row[5]}" target="_blank">
                                <div class="book_img" style="background-image: url('${book_row[6]}')"></div>
                            </a>
                            <div class="recommend_book_desc" style="display: ${display_value}">
                                <div class="recommend_book_desc_title">
                                    <p>제목</p>
                                    <p>${book_row[0]}</p>
                                </div>
                                <div class="recommend_book_desc_series">
                                    <p>시리즈</p>
                                    <p>${book_row[3]}</p>
                                </div>
                                <div class="recommend_book_desc_company">
                                    <p>출판사</p>
                                    <p>${book_row[2]}</p>
                                </div>
                                <div class="recommend_book_desc_author">
                                    <p>작가</p>
                                    <p>${book_row[1]}</p>
                                </div>
                                <div class="recommend_book_desc_price">
                                    <p>가격</p>
                                    <p>${book_row[4]}</p>
                                </div>
                            </div>
                        </div>`
        if (content_type === 'c') {
            $('#book_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#book_search_content').append(temp_html)
        }
    }
}


// shopping
function shopping_content_add(shopping_crawling_data_list, type) {
    let content_type = ''
    if (type === 'crawling') {
        content_type = 'c';
    } else if (type === 'search') {
        content_type = 's';
    } else {
        return console.log('type is not define!!')
    }

    for (let i = 0; i < shopping_crawling_data_list.length; i++) {
        let shopping_row = shopping_crawling_data_list[i]
        let content_id = 'shopping_' + content_type + '_' + i
        let heart_image = '/static/images/empty_heart.png'
        if(shopping_row[4]){
            heart_image = '/static/images/heart.png'
        }
        let temp_html = `<div class="recommend_shopping_search_content" id="${content_id}">
                                    <div class="recommend_toggle">
                                        <div class="profile_like_news_toggle" onclick="content_do_share('${shopping_row[3]}')">
                                            <img src="/static/images/share.png">
                                        </div>
                                        <div class="recommend_like_heart"
                                             style="background-image: url('${heart_image}')">
                                        </div>
                                    </div>
                                    <a href="${shopping_row[3]}" target="_blank">
                                        <div class="recommend_shopping_search_content_img">
                                            <img src="${shopping_row[0]}">
                                        </div>
                                    </a>
                                    <div class="recommend_shopping_search_content_desc">
                                        <div class="recommend_shopping_search_content_desc_bar"></div>
                                        <div class="recommend_shopping_search_content_desc_title">
                                            <p>${shopping_row[1]}</p>
                                        </div>
                                        <div class="recommend_shopping_search_content_desc_price">
                                            <p>${shopping_row[2]} 원</p>
                                        </div>
                                    </div>
                                </div>`
        if (content_type === 'c') {
            $('#shopping_recommend_content').append(temp_html)
        } else if (content_type === 's') {
            $('#shopping_search_content').append(temp_html)
        }

    }
}


// more function

function more_open_or_off(id) {
    let other_toggles = document.getElementsByClassName('toggle')

    for (let i = 0; i < other_toggles.length; i++) {
        other_toggles[i].style.display = 'none'
    }

    let toggle = document.getElementById(id).nextElementSibling
    if (toggle.style.display === 'none') {
        toggle.style.display = 'block'
    } else {
        toggle.style.display = 'none'
    }

}

// more_shopping_function

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

// like clicked
function clicked_like_heart() {

    $('recommend_like_heart').off('click')
    let empty_heart_classes = document.getElementsByClassName('recommend_like_heart')
    let background_heart = 'url("/static/images/heart.png")'
    let background_empty_heart = 'url("/static/images/empty_heart.png")'
    for (let i = 0; i < empty_heart_classes.length; i++) {
        empty_heart_classes[i].addEventListener('click', (event) => {
                let curr_backgroundImage = event.target.style.backgroundImage;
                let id = event.target.parentElement.parentElement.id

                if (curr_backgroundImage === background_empty_heart) {
                    event.target.style.backgroundImage = background_heart
                    like_check_hub(id, 'like')

                } else {
                    event.target.style.backgroundImage = background_empty_heart
                    like_check_hub(id, 'like_cancel')

                }

            }
        )

    }
}

// like 분류 함수 (youtube? news? book? shopping?)
function like_check_hub(id, type) {
    let checker = id.split('_')[0]
    if (checker === 'youtube') {
        // url 가져 오기
        let url = document.getElementById(id).firstElementChild.src
        // youtube like function
        like_youtube_ajax(url, type)
    }
    // news data 가져 오기
    else if (checker === 'news') {
        let news = document.getElementById(id)
        let link = news.children[0].children[0].href
        let title = news.children[1].children[0].innerText
        let content = news.children[1].children[1].innerText
        let company = news.children[1].children[2].children[0].innerText
        let date = news.children[1].children[2].children[1].innerText
        let thumbnail = news.children[0].children[0].children[0].src

        let news_data = {}
        news_data['title'] = title
        news_data['date'] = date
        news_data['company'] = company
        news_data['content'] = content
        news_data['thumbnail'] = thumbnail
        news_data['link'] = link

        like_news_ajax(news_data, type)
    }
    // book data 가져 오기
    else if (checker === 'book') {
        let book = document.getElementById(id)
        let title = book.children[2].children[0].children[1].innerText
        let author = book.children[2].children[3].children[1].innerText
        let company = book.children[2].children[2].children[1].innerText
        let price = book.children[2].children[4].children[1].innerText
        let link = book.children[1].href
        let thumbnail = book.children[1].children[0].style.backgroundImage.split('url("')[1].split('")')[0]

        let book_data = {}
        book_data['title'] = title
        book_data['author'] = author
        book_data['company'] = company
        book_data['price'] = price
        book_data['link'] = link
        book_data['thumbnail'] = thumbnail

        like_book_ajax(book_data, type)
    }
    // shopping data 가져 오기
    else if (checker === 'shopping') {
        let shopping = document.getElementById(id)
        let link = shopping.children[1].href
        let price = shopping.children[2].children[2].children[0].innerText
        let title = shopping.children[2].children[1].children[0].innerText
        let thumbnail = shopping.children[1].children[0].children[0].src

        let shopping_data = {}
        shopping_data['price'] = price
        shopping_data['title'] = title
        shopping_data['thumbnail'] = thumbnail
        shopping_data['link'] = link
        console.log(shopping_data)
        like_shopping_ajax(shopping_data, type)
    }
}


function like_youtube_ajax(data, type) {

    // like 할 때
    if (type === 'like') {
        let result = 'Like result : '
        $.ajax({
            type: 'POST',
            url: '/api/like/youtube',
            data: {'url': data},
            success: function (response) {
                let ajax_result = response['result']
                result += ajax_result
                alert(result)
            }
        })
    } // like 취소
    else if(type === 'like_cancel'){
        let result = 'Like cancel result : '
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/youtube',
            data: {'url': data},
            success: function (response) {
                let ajax_result = response['result']
                result += ajax_result
                alert(result)
            }
        })
    }

}

function like_news_ajax(data, type){
    // 뉴스 like 할때
    if(type  === 'like'){
        $.ajax({
            type: 'POST',
            url: '/api/like/news',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
    // 뉴스 like 취소 할 때
    else if(type==='like_cancel'){
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/news',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
}

function like_book_ajax(data, type){
    // 책 like 할때
    if(type  === 'like'){
        $.ajax({
            type: 'POST',
            url: '/api/like/book',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
    // 책 like 취소 할 때
    else if(type==='like_cancel'){
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/book',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
}

function like_shopping_ajax(data, type){
    // 쇼핑 like 할때
    if(type  === 'like'){
        $.ajax({
            type: 'POST',
            url: '/api/like/shopping',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
    // 쇼핑 like 취소 할 때
    else if(type==='like_cancel'){
        $.ajax({
            type: 'POST',
            url: '/api/like_cancel/shopping',
            data: data,
            success: function(response){
                alert(response['result'])
            }
        })
    }
}


// 공유하기 버튼
function content_do_share(str) {
    var textarea = document.createElement('textarea');
    textarea.value = str;
    document.body.appendChild(textarea);
    textarea.select();
    textarea.setSelectionRange(0, 9999);
    document.execCommand('copy');
    document.body.removeChild(textarea);
    alert('복사되었습니다')
}

// search 관련
function initialize_search_bar() {
    let search_bars = document.getElementsByClassName('search_bar')
    for (let i = 0; i < search_bars.length; i++) {
        search_bars[i].children[1].addEventListener('keyup', (e) => {
            if (e.keyCode === 13) {
                let search_word = search_bars[i].children[1].value
                search_bars[i].children[1].value = ''


                // 이전 데이터 지우기
                clear_content()

                // // spinner running
                let search_spinner = document.getElementsByClassName('spinner_search')
                //
                // for(let i=0; i<search_spinner.length;i++){
                //     search_spinner[i].style.display ='flex'
                // }


                // search_창 보이기
                let search_contents = document.getElementsByClassName('search_content')
                for (let k = 0; k < search_contents.length; k++) {
                    search_contents[k].style.display = 'block'
                }
                document.getElementsByClassName('search_news_content')[0].style.display = 'block'
                document.getElementsByClassName('search_book_content')[0].style.display = 'block'


                $.ajax({
                    type: 'POST',
                    url: '/api/search/crawling',
                    data: {"target": search_word},
                    datatype: 'form',
                    success: function (response) {

                        // search_spinner 정지
                        for (let i = 0; i < search_spinner.length; i++) {
                            search_spinner[i].style.display = 'none'
                        }


                        // content 내용 붙이기
                        youtube_content_add(response['all_response']['youtube'], 'search')
                        news_content_add(response['all_response']['news'], 'search')
                        book_content_add(response['all_response']['book'], 'search')
                        shopping_content_add(response['all_response']['shopping'], 'search')

                        // hovering_like
                        clicked_like_heart()
                        set_animation_more()

                        // clicked_like
                        // like_news()
                    }
                })
            }
        })

    }
}

function clear_content() {
    let spinner_html = `<div class="recommend_spinner spinner_search" style="display: flex;">
                            <div class="recommend_spinner_lorder"></div>
                        </div>`

    $('#youtube_search_content').empty();
    $('#youtube_search_content').append(spinner_html);

    $('#news_search_content').empty();
    $('#news_search_content').append(spinner_html);

    $('#book_search_content').empty();
    $('#book_search_content').append(spinner_html);

    $('#shopping_search_content').empty();
    $('#shopping_search_content').append(spinner_html);
}
