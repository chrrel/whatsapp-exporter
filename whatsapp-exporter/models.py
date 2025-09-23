import time
from dataclasses import dataclass, field
from urllib.parse import quote


@dataclass
class Message:
    received_timestamp: str
    remote_resource: str
    key_from_me: str
    data: str
    media_caption: str
    media_wa_type: int
    latitude: str
    longitude: str
    media_path: str
    sender: str

    def __post_init__(self):
        self.received_timestamp = Message.__timestamp_to_str(self.received_timestamp)

    def __str__(self):
        prefix = ">" if self.key_from_me else "<"
        return f"{prefix} {self.received_timestamp} - {self.content} {self.get_media()}"

    @staticmethod
    def __timestamp_to_str(timestamp: str) -> str:
        ts = int(timestamp) / 1000.0
        return time.strftime("%d.%m.%Y %H:%M", time.localtime(ts))

    @property
    def content(self) -> str:
        return self.data if self.media_wa_type == 0 else (self.media_caption or "")

    @property
    def sender_name(self) -> str:
        if self.sender:
            return self.sender
        elif self.remote_resource:
            return self.remote_resource.split("@")[0]
        else:
            return ""

    def get_media(self) -> str:
        """
        Retrieve a message's media attachments which can have the following types:
        0: "Text", 1: "Image", 2: "Audio", 3: "Video", 4: "Contact", 5: "Location", 7: "System Message", 9: "Document",
        10: "Missed Call", 13: "Animated GIF", 14: "Multiple contacts", 15: "Deleted", 16: "Live Location",
        20: "Sticker", 42: "View Once"
        """
        media_map = {
            0: "",
            1: f"""<a href="{self.media_path}" target="_blank"><img src="{self.media_path}" loading="lazy"></a>""",
            2: f"""<a href="{self.media_path}" target="_blank"><audio controls preload="none"><source src="{self.media_path}"></source></audio></a>""",
            3: f"""<a href="{self.media_path}" target="_blank"><video controls preload="none"><source src="{self.media_path}"></source></video></a>""",
            4: f"""[Contact] {self.media_path} (<a download="{self.media_path}.vcf" href="data:application/octet-stream,{quote(str(self.data))}">Download)</a>""",
            5: f"""[Location] {self.latitude}, {self.longitude} (<a target="_blank" href="http://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}&zoom=16">{self.media_path if self.media_path else "Link"}</a>)""",
            7: f"[System Message] {self.media_path}",
            9: f"""<a href="{self.media_path}" target="_blank">{self.media_path}</a>""",
            10: "[Missed Call]",
            13: f"""<a href="{self.media_path}" target="_blank"><video controls preload="none"><source src="{self.media_path}"></source></video></a>""",
            14: f"""[Multiple Contacts] {self.media_path}""",
            15: "[Deleted]",
            16: f"""[Live Location] {self.latitude}, {self.longitude} (<a target="_blank" href="http://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}&zoom=16">{self.media_path if self.media_path else "Link"}</a>)""",
            20: f"""<a href="{self.media_path}" target="_blank"><img src="{self.media_path}" loading="lazy"></a>""",
            42: f"""[View Once] {self.media_path}"""
        }
        return media_map.get(self.media_wa_type, f"[Unknown medium] {self.media_path}")


@dataclass
class Chat:
    key_remote_jid: str
    subject: str
    sort_timestamp: str
    name: str
    phone_number: str = field(init=False)
    title: str = field(init=False)
    messages: field(default_factory=list)

    def __post_init__(self):
        self.phone_number = self.key_remote_jid.split("@")[0]
        self.title = self.subject or self.name or self.phone_number

    def __str__(self):
        return str(self.key_remote_jid) + " " + str(self.title)
