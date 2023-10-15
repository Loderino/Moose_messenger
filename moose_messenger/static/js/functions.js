let current_user;

function sendMessage(username, session) {
    var message = document.getElementById("message_text").value;
    $.ajax({
        url: "/Send_message",
        type: "POST",
        contentType: "json",
        data: JSON.stringify({"message": message, "username": username, "session": session}),
        success: function(data) {
            console.log(data);  
        }
    });
}

function get_side(username){
    if (current_user == username){
        return "right"
    }
    else{
        return "left"
    }
}

function create_message_div(message, time_code, username){
    message_div = "<div class='message' style='float:" +get_side(username)+ "'>"+"<div class = 'username'>"+username+"</div>"+"<div class = 'message_content'>"+split_to_rows(message)+"</div>"+"<div class = 'time_code'>"+time_code+"</div>"+ "</div>";
    return message_div
}

function split_to_rows(str){
    var words = str.split(' ');
    var lines = [];
    var currentLine = '';

    for (var i = 0; i < words.length; i++) {
        var word = words[i];

        // Если слово длиннее 70 символов, разбиваем его на части
        if (word.length > 70) {
            var parts = word.match(/.{1,70}/g);
            lines.push(...parts);
            currentLine = '';
            continue;
        }

        // Проверяем, не превысит ли текущая строка 70 символов, если добавить к ней это слово
        if ((currentLine + word).length > 70) {
            lines.push(currentLine.trim());
            currentLine = word + ' ';
        } else {
            currentLine += word + ' ';
        }
    }

    // Добавляем оставшуюся строку, если она не пустая
    if (currentLine.trim() !== '') {
        lines.push(currentLine.trim());
}

return lines.join('<br>');
}

function getMessages() {
    $.ajax({
        url: "/Get_messages",
        type: "POST",
        success: function(data) {
            itog = ""
            data.forEach(element => {
                itog+=create_message_div(element["content"], element["time"], element["username"])
            });
            document.getElementById("chat_div").innerHTML = itog 
        }
    });
}
setInterval(getMessages, 1000);