
//프로필 변경버튼 클릭
function profile_change(){
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