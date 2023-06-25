import html
from string import Template

from models import Message


def chats_to_txt(chats: list, directory_path: str):
    for chat in chats:
        messages = "\n".join([str(message) for message in chat.messages])
        with open(f"{directory_path}/{chat.key_remote_jid}.txt", "w", encoding="utf-8") as file:
            file.write(chat.title + "\n" + messages)


def chats_to_html(chats: list, filepath: str):
    chat_contents = ""
    chats_list = ""
    for chat in chats:
        # Hide empty chats
        if len(chat.messages) == 0:
            continue

        # Add the chat contents to the HTML
        t = Template("""<div class="chat" data-chatid="$chat_id">$messages</div>""")
        chat_contents += t.substitute(
            chat_id=_esc(chat.key_remote_jid),
            messages="".join([_message_to_html(m) for m in chat.messages])
        )

        # Add a row to the list of chats
        t = Template("""<div class="chat-partner"><a href="#$id" title="$phone_number">$title<div>$preview</div></a></div>""")
        last_message = chat.messages[-1].get_content()
        preview = last_message[0:55] if last_message is not None else ""
        chats_list += t.substitute(
            id=_esc(chat.key_remote_jid),
            phone_number=_esc(chat.phone_number),
            title=_esc(chat.title),
            preview=_esc(preview)
        )

    _save_to_html_file(chat_contents, chats_list, filepath)


def _message_to_html(m: Message) -> str:
    direction_class = " sent" if m.key_from_me else ""
    sender = _esc(m.get_sender_name())
    content = _esc(m.get_content())
    time = _esc(m.received_timestamp_str)

    if m.remote_resource:
        t = Template("""<div class="message$direction_class"><div class="sender">$sender</div>$content<div class="time">$time</div></div>""")
        return t.substitute(direction_class=direction_class, sender=sender, content=content, time=time)
    else:
        t = Template("""<div class="message$direction_class">$content<div class="time">$time</div></div>""")
        return t.substitute(direction_class=direction_class, content=content, time=time)


def _esc(content) -> str:
    return html.escape(str(content))


def _load_file_content(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def _save_to_html_file(chat_contents: str, chats_list: str, filepath: str):
    # Load the HTML template from file and populate it with data
    t = Template(_load_file_content("resources/template.html"))
    html_output = t.substitute(
        js_code=_load_file_content("resources/main.js"),
        css_code=_load_file_content("resources/styles.css"),
        chats_list=chats_list,
        chat_contents=chat_contents
    )

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html_output)
