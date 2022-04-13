// 해당 채팅방에 접속해있지 않아도 최근 메세지를 받을 수 있도록 함
function latestMessageNotConnected() {
    let all_partner = document.getElementsByClassName('chat_partner')

    var partner_list = []
    for (let i = 0; i < all_partner.length; i++) {
        let partner = all_partner[i]['href'].split('/')
        partner = parseInt(partner[4]);
        partner_list.push(partner)
    }

    $.ajax({
        url: "/chat/latestmessagenotconnected/",
        type: "post",
        traditional: true,
        data: JSON.stringify({"partner_list": partner_list}),
        async: false,
        success: function (data) {
            let rows = data['latest_chat_list']
            for (let i = 0; i < rows.length; i++) {
                let chatter_id = rows[i]['partner']
                let message = rows[i]['latest_message_each_chatroom']
                let author_id = rows[i]['author_message']

                let temp_html = `<div class="partner_last_msg partner_last_msg_${author_id}">${message}</div>`
                $('.chat_partner_' + chatter_id).children('.info_group').append(temp_html)
            }
        },
        error: function (request, status, error) {
            alert('error')

            console.log(request, status, error)
        }
    })
}


//채팅방에 이전메세지 불러오기
function messageLoader(user_id) {
    var link = document.location.href;
    let room_id = link.split('/');
    room_id = parseInt(room_id[5]);

    let form_data = new FormData();
    form_data.append('room_id', room_id)

    $.ajax({
        url: "/chat/messageloader/",
        type: "post",
        data: JSON.stringify({"room_id": room_id}),
        enctype: 'multipart/form-data',
        async: false,
        success: function (data) {
            let rows = data['last_messages_list']
            for (let i = 0; i < rows.length; i++) {
                let author_id = rows[i]['author_id']
                let message = rows[i]['message']
                let timestamp = rows[i]['created_at'].split('')

                if ((timestamp[11] === 1 && timestamp[12] >= 2) || timestamp[11] === 2) {
                    var am_or_pm = timestamp[2] + timestamp[3] + '년' + timestamp[5] + timestamp[6] + '월' + timestamp[8] + timestamp[9] + '일,' + ' 오후 ' + timestamp[11] + timestamp[12] + ':' + timestamp[14] + timestamp[15]
                } else {
                    var am_or_pm = timestamp[2] + timestamp[3] + '년' + timestamp[5] + timestamp[6] + '월' + timestamp[8] + timestamp[9] + '일,' + ' 오전 ' + timestamp[11] + timestamp[12] + ':' + timestamp[14] + timestamp[15]
                }

                if (author_id === user_id) {
                    if (message.includes('http') === true) {
                        let temp_html1 = `<div class="user_chat">
                                                  <div onmouseover="show_user_timestamp(${i})" onmouseout="hide_user_timestamp(${i})" onclick="window.open('${message}')" style="cursor: pointer; text-decoration-line: underline" class='user_to_partner'>${message}</div>
                                                  <div class="timestamp_user timestamp_user_${i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').append(temp_html1)
                    } else {
                        let temp_html1 = `<div class="user_chat">
                                                  <div onmouseover="show_user_timestamp(${i})" onmouseout="hide_user_timestamp(${i})" class='user_to_partner'>${message}</div>
                                                  <div class="timestamp_user timestamp_user_${i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').append(temp_html1)
                    }
                } else {
                    if (message.includes('http') === true) {
                        let temp_html2 = `<div class="partner_chat">
                                                  <div onmouseover="show_partner_timestamp(${i})" onmouseout="hide_partner_timestamp(${i})" onclick="window.open('${message}')" style="cursor: pointer; text-decoration-line: underline" class='partner_to_user'>${message}</div>
                                                  <div class="timestamp_partner timestamp_partner_${i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').append(temp_html2)
                    } else {
                        let temp_html2 = `<div class="partner_chat">
                                                  <div onmouseover="show_partner_timestamp(${i})" onmouseout="hide_partner_timestamp(${i})" class='partner_to_user'>${message}</div>
                                                  <div class="timestamp_partner timestamp_partner_${i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').append(temp_html2)
                    }
                }
            }
        },
        error: function (request, status, error) {
            alert('error')

            console.log(request, status, error)
        }
    })
}


//채팅로그 더보기 버튼
function moreList(user_id) {
    var startNum = $('.user_to_partner').length + $('.partner_to_user').length;
    //마지막 리스트 번호를 알아내기 위해서 length를 구함.

    var link = document.location.href;
    var room_id = link.split('/');
    room_id = parseInt(room_id[5]);

    let form_data = new FormData();
    form_data.append('startNum', startNum)
    form_data.append('room_id', room_id)
    form_data.append('user_id', user_id)


    $.ajax({
        url: "/chat/morelist/",
        type: "post",
        data: JSON.stringify({"room_id": room_id, 'startNum': startNum, 'user_id': user_id}),
        enctype: 'multipart/form-data',
        async: false,
        success: function (data) {
            let rows = data['chat_list']
            for (let i = rows.length - 1; i >= 0; i--) {
                let author_id = rows[i]['author_id']
                let message = rows[i]['message']
                let timestamp = rows[i]['created_at'].split('')

                if ((timestamp[11] === 1 && timestamp[12] >= 2) || timestamp[11] === 2) {
                    var am_or_pm = timestamp[2] + timestamp[3] + '년' + timestamp[5] + timestamp[6] + '월' + timestamp[8] + timestamp[9] + '일,' + ' 오후 ' + timestamp[11] + timestamp[12] + ':' + timestamp[14] + timestamp[15]
                } else {
                    var am_or_pm = timestamp[2] + timestamp[3] + '년' + timestamp[5] + timestamp[6] + '월' + timestamp[8] + timestamp[9] + '일,' + ' 오전 ' + timestamp[11] + timestamp[12] + ':' + timestamp[14] + timestamp[15]
                }

                if (author_id === user_id) {
                    if (message.includes('http') === true) {
                        let temp_html1 = `<div class="user_chat">
                                                  <div onmouseover="show_user_timestamp(${startNum + i})" onmouseout="hide_user_timestamp(${startNum + i})" onclick="window.open('${message}')" style="cursor: pointer; text-decoration-line: underline" class='user_to_partner'>${message}</div>
                                                  <div class="timestamp_user timestamp_user_${startNum + i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').prepend(temp_html1)
                    } else {
                        let temp_html1 = `<div class="user_chat">
                                                  <div onmouseover="show_user_timestamp(${startNum + i})" onmouseout="hide_user_timestamp(${startNum + i})" class='user_to_partner'>${message}</div>
                                                  <div class="timestamp_user timestamp_user_${startNum + i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').prepend(temp_html1)
                    }
                } else {
                    if (message.includes('http') === true) {
                        let temp_html2 = `<div class="partner_chat">
                                                  <div onmouseover="show_partner_timestamp(${startNum + i})" onmouseout="hide_partner_timestamp(${startNum + i})" onclick="window.open('${message}')" style="cursor: pointer; text-decoration-line: underline" class='partner_to_user'>${message}</div>
                                                  <div class="timestamp_partner timestamp_partner_${startNum + i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').prepend(temp_html2)
                    } else {
                        let temp_html2 = `<div class="partner_chat">
                                                  <div onmouseover="show_partner_timestamp(${startNum + i})" onmouseout="hide_partner_timestamp(${startNum + i})" class='partner_to_user'>${message}</div>
                                                  <div class="timestamp_partner timestamp_partner_${startNum + i}">${am_or_pm}</div>
                                              </div>`
                        $('#chat_box').prepend(temp_html2)
                    }
                }
            }
            if (rows.length === 0) {
                $('.more').hide()
                let last_alert = `<div class="last_list">마지막 대화입니다.</div>`
                $('#chat_box').prepend(last_alert)
            } else {
                $('.more').hide()
                let morebtn = `<div class="more" style="cursor: pointer;" onclick=moreList(user_id)>이전대화 불러오기</div>`
                $('#chat_box').prepend(morebtn)

            }

        },
        error: function (request, status, error) {
            alert('error')

            console.log(request, status, error)
        }
    })
}


// 각 채팅 onmouse 타임스템프

function show_user_timestamp(num) {
    $('.timestamp_user_' + num).show();
}

function hide_user_timestamp(num) {
    $('.timestamp_user_' + num).hide();
}

function show_partner_timestamp(num) {
    $('.timestamp_partner_' + num).show();
}

function hide_partner_timestamp(num) {
    $('.timestamp_partner_' + num).hide();
}