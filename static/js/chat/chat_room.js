// 채팅방 리스트에 마지막메세지 띄워주기
function lastMessageList() {
    //let all_partner = document.getElementsByClassName('chat_partner')
    //console.log(all_partner)

    //let partner_list = []
    //for (let i = 0; i < all_partner.length; i++) {
        //let partner = all_partner[i]['href'].split('/')[4]
        //console.log(partner)
        //partner_list.append(partner)
    //}
    //console.log(partner_list)
    //let form_data = new FormData();
    //form_data.append('partner_id', partner_list)

    $.ajax({
        url: "/chat/lastmessagelist/",
        type: "post",
        data: JSON.stringify({}),
        enctype: 'multipart/form-data',
        async: false,
        success: function (data) {
            let rows = data['last_message_list']
            for (let i = 0; i < rows.length; i++) {
                let author_id = rows[i]['author_id']
                let message = rows[i]['message']
                let chatroom_id = rows[i]['chatroom_id']
                console.log(author_id, message, chatroom_id)

                let temp_html = `<div class="partner_last_msg partner_last_msg_${author_id}">${message}</div>`
                $('.chat_partner_' + chatroom_id).children('.info_group').append(temp_html)
            }
        },
        error: function (request, status, error) {
            alert('error')

            console.log(request, status, error)
        }
    })

}