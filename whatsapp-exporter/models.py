import time
from urllib.parse import quote

class Message:
    def __init__(self, received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type, latitude,
                 longitude, media_path, sender):
        self.received_timestamp = received_timestamp
        self.remote_resource = remote_resource
        self.key_from_me = key_from_me
        self.data = data
        self.media_caption = media_caption
        self.media_wa_type = media_wa_type
        self.latitude = latitude
        self.longitude = longitude
        self.media_path = media_path
        self.received_timestamp_str = Message.__timestamp_to_str(received_timestamp)
        self.sender = sender

    @staticmethod
    def __timestamp_to_str(timestamp: str) -> str:
        ts = int(timestamp) / 1000.0
        return time.strftime('%d.%m.%Y %H:%M', time.localtime(ts))

    def get_content(self) -> str:
        media_caption = self.media_caption if self.media_caption is not None else ""

        if self.media_wa_type == 0:
            return self.data
        else:
            return media_caption


    def get_media(self) -> str:
        """
        Retrieve a message's media attachments which can have the following types:
        0: "Text", 1: "Image", 2: "Audio", 3: "Video", 4: "Contact", 5: "Location", 7: "System Message", 9: "Document",
        10: "Missed Call", 13: "Animated GIF", 14: "Multiple contacts", 15: "Deleted",16: "Live Location", 20: "Sticker"
        """
        if self.media_wa_type == 0:
            media = ""
        elif self.media_wa_type == 1:
            media = f"""<a href="{self.media_path}" target="_blank"><img src="{self.media_path}" loading="lazy"></a>"""
        elif self.media_wa_type == 2:
            media = f"""<a href="{self.media_path}" target="_blank"><audio controls preload="none"><source src="{self.media_path}"></source></audio></a>"""
        elif self.media_wa_type == 3:
            media = f"""<a href="{self.media_path}" target="_blank"><video controls preload="none"><source src="{self.media_path}"</source></video></a>"""
        elif self.media_wa_type == 4:
            media = f"""[Contact] {self.media_path} (<a download="{self.media_path}.vcf" href="data:application/octet-stream,{quote(str(self.data))}">Download)</a>"""
        elif self.media_wa_type == 5:
            media = f"""[Location] {self.latitude}, {self.longitude} (<a target="_blank" href="http://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}&zoom=16">{self.media_path if self.media_path else "Link"}</a>)"""
        elif self.media_wa_type == 7:
            media = f"[System Message] {self.media_path}"
        elif self.media_wa_type == 9:
            media = f"""<a href="{self.media_path}" target="_blank">{self.media_path}</a>"""
        elif self.media_wa_type == 10:
            media = f"""[Missed Call] </a>"""
        elif self.media_wa_type == 13:
            media = f"""<a href="{self.media_path}" target="_blank"><video controls preload="none"><source src="{self.media_path}"</source></video></a>"""
        elif self.media_wa_type == 14:
            media = f"""[Multiple Contacts] {self.media_path}"""
        elif self.media_wa_type == 15:
            media = f"""[Deleted]"""
        elif self.media_wa_type == 16:
            media = f"""[Live Location] {self.latitude}, {self.longitude} (<a target="_blank" href="http://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}&zoom=16">{self.media_path if self.media_path else "Link"}</a>)"""
        elif self.media_wa_type == 20:
            media = f"""<a href="{self.media_path}" target="_blank"><img src="{self.media_path}" loading="lazy"></a>"""
        else:
            media = f"[Unknown medium] {self.media_path}"

        return media
    def get_sender_name(self) -> str:
        if self.sender:
            return self.sender
        elif self.remote_resource:
            return self.remote_resource.split("@")[0]
        else:
            return self.remote_resource

    def __str__(self):
        if self.key_from_me:
            return f"> {self.received_timestamp_str} - {self.get_content()} {self.get_media()}"
        else:
            return f"< {self.received_timestamp_str} - {self.get_content()} {self.get_media()}"


class Chat:
    def __init__(self, key_remote_jid, subject: str, sort_timestamp, name: str, messages: list):
        self.key_remote_jid = key_remote_jid
        self.subject = subject
        self.sort_timestamp = sort_timestamp
        self.name = name
        self.phone_number = key_remote_jid.split("@")[0]
        self.title = self.__get_chat_title()
        self.messages = messages

    def __str__(self):
        return str(self.key_remote_jid) + " " + str(self.title)

    def __get_chat_title(self):
        if self.subject is not None:
            return self.subject
        elif self.name is not None:
            return self.name
        else:
            return self.phone_number
