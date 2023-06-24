function displayActiveChat(chat, linkToChat) {
    chat.classList.add("active-chat");
    chat.scrollTop = chat.scrollHeight;
    linkToChat.classList.add("active-chatpartner");
}

window.onload = function(event) {
    let firstChat = document.querySelectorAll(".chat")[0];
    let firstChatPartnerLink = document.querySelectorAll("a")[0];
    displayActiveChat(firstChat, firstChatPartnerLink);

    links = document.querySelectorAll("a").forEach(function(link){
        link.addEventListener("click", function(event) {
            event.preventDefault();
            document.querySelector(".active-chat").classList.remove("active-chat");
            document.querySelector(".active-chatpartner").classList.remove("active-chatpartner");

            let target = link.hash.replace("#","");
            chat = document.querySelector(`[data-chatid="${target}"]`);
            displayActiveChat(chat, link);
        }, false);
    });
}
