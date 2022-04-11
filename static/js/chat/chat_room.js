// // 채팅방 리스트에 마지막메세지 띄워주기
// function lastMessageList() {
//
//     $.ajax({
//         url: "/chat/lastmessagelist/",
//         type: "post",
//         data: JSON.stringify({}),
//         enctype: 'multipart/form-data',
//         async: false,
//         success: function (data) {
//             let rows = data['last_message_list']
//             for (let i = 0; i < rows.length; i++) {
//                 let author_id = rows[i]['author_id']
//                 let message = rows[i]['message']
//                 let chatroom_id = rows[i]['chatroom_id']
//                 console.log(author_id, message, chatroom_id)
//
//                 let temp_html = `<div class="partner_last_msg partner_last_msg_${author_id}">${message}</div>`
//                 $('.chat_partner_' + chatroom_id).children('.info_group').append(temp_html)
//             }
//         },
//         error: function (request, status, error) {
//             alert('error')
//
//             console.log(request, status, error)
//         }
//     })
//
// }
//
// //최근메세지 채팅 리스트에 업데이트하기
//
// function latestMessage() {
//     var link = document.location.href;
//     console.log(link);
//     let room_id = link.split('/');
//     room_id = parseInt(room_id[5]);
//
//     let form_data = new FormData();
//     form_data.append('room_id', room_id)
//
//     $.ajax({
//         url: "/chat/latestmessage/",
//         type: "post",
//         data: JSON.stringify({"room_id": room_id}),
//         enctype: 'multipart/form-data',
//         async: false,
//         success: function (data) {
//             let message = data['message']
//             let partner_id = data['partner_id']
//             let author_id = data['author_id']
//             // console.log(message, partner_id, author_id)
//             let temp_html = `<div class="partner_last_msg partner_last_msg_${author_id}">${message}</div>`
//             $('.chat_partner_' + room_id).children('.info_group').append(temp_html)
//         },
//         error: function (request, status, error) {
//             alert('error')
//
//             console.log(request, status, error)
//         }
//     })
// }

// 해당 채팅방에 접속해있지 않아도 최근 메세지를 받을 수 있도록 함
function latestMessageNotConnected() {
    let all_partner = document.getElementsByClassName('chat_partner')
    console.log(all_partner)

    var partner_list = []
    for (let i = 0; i < all_partner.length; i++) {
        let partner = all_partner[i]['href'].split('/')
        partner = parseInt(partner[4]);
        console.log(i, partner, typeof (partner))
        partner_list.push(partner)
    }
    console.log(partner_list)

    $.ajax({
        url: "/chat/latestmessagenotconnected/",
        type: "post",
        traditional: true,
        data: JSON.stringify({"partner_list": partner_list}),
        async: false,
        success: function (data) {
            console.log(data['latest_chat_list'])
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