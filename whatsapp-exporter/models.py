import time
from urllib.parse import quote

class Message:
    def __init__(self, received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type, latitude, longitude, media_path, sender):
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
        media_types = {
            0: {
                "type": "Text",
                "value": ""
            },
            1: {
                "type": "Image",
                "value": f"""<a href="{self.media_path}" target="_blank"><img src="{self.media_path}" loading="lazy"></a>"""
            },
            2: {
                "type": "Audio",
                "value": f"""<a href="{self.media_path}" target="_blank"><audio controls preload="none"><source src="{self.media_path}"></source></audio></a>"""
            },
            3: {
                "type": "Video",
                "value": f"""<a href="{self.media_path}" target="_blank"><video controls preload="none"><source src="{self.media_path}"</source></video></a>"""
            },
            4: {
                "type": "Contact",
                "value": f"""[Contact] {self.media_path} (<a download="{self.media_path}.vcf" href="data:application/octet-stream,{quote(str(self.data))}">Download)</a>"""
            },
            5: {
                "type": "Location",
                "value": f"""[Location] {self.latitude}, {self.longitude} (<a target="_blank" href="http://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}&zoom=16">{self.media_path if self.media_path else "Link"}</a>)"""
            },
            7: {
                "type": "System Message",
                "value": f"[System Message] {self.media_path}"
            },
            9: {
                "type": "Document",
                "value": f"""<a href="{self.media_path}" target="_blank">{self.media_path}</a>"""
            },
            13: {
                "type": "Animated GIF",
                "value": f"""<a href="{self.media_path}" target="_blank"><video controls preload="none"><source src="{self.media_path}"</source></video></a>"""
            },
            16: {
                "type": "Live Location",
                "value": f"[Live Location] {self.media_path}"
            },
            20: {
                "type": "Sticker",
                "value": f"""<a href="{self.media_path}" target="_blank"><img src="{self.media_path}" loading=\"lazy\"></a>"""
            }
        }

        if self.media_wa_type == 0:
            media = ""
        elif self.media_wa_type in media_types:
            if self.media_path:
                media = media_types[self.media_wa_type]["value"]
            elif self.latitude and self.longitude:
                media = media_types[self.media_wa_type]["value"]
            else:
                media = f"""[{media_types[self.media_wa_type]["type"]} not found]"""
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
            return f"> {self.received_timestamp_str} - {self.get_content()}"
        else:
            return f"< {self.received_timestamp_str} - {self.get_content()}"


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
