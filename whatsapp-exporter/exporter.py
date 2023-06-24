import html

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
        if len(chat.messages) == 0:
            continue
        messages = "".join([_message_to_html(m) for m in chat.messages])
        chat_contents += f"<div class='chat' data-chatid='{_esc(chat.key_remote_jid)}'>{messages}</div>"
        preview = ""
        if chat.messages[-1].get_content() is not None:
            preview = chat.messages[-1].get_content()[0:55]
        chats_list += f"<div class='chat-partner'><a href='#{_esc(chat.key_remote_jid)}' title='{_esc(chat.phone_number)}'>" \
                      f"{_esc(chat.title)}<div class='chat-partner-subtitle'>{_esc(preview)}</div></a></div>"
    _save_to_html_file(chat_contents, chats_list, filepath)


def _message_to_html(m: Message) -> str:
    if m.key_from_me:
        direction_class = " sent"
    else:
        direction_class = ""

    if m.remote_resource:
        return f"<div class='message{direction_class}'><div class='sender'>{_esc(m.get_sender_name())}</div>" \
               f"{_esc(m.get_content())}<div class='time'>{_esc(m.received_timestamp_str)}</div></div>"
    else:
        return f"<div class='message{direction_class}'>{_esc(m.get_content())}" \
               f"<div class='time'>{_esc(m.received_timestamp_str)}</div></div>"


def _esc(content) -> str:
    return html.escape(str(content))


def _load_file_content(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def _save_to_html_file(chat_contents: str, chats_list: str, filepath: str):
    # Use template as f-string and populate it with data
    js_code = _load_file_content("res/main.js")
    css_code = _load_file_content("res/styles.css")
    # Avoid SyntaxError: f-string must not include a backslash
    template = _load_file_content('res/template.html').replace("\n", "")
    html_output = f"{template}".format(**locals())

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html_output)
