import configparser
import sqlite3
from sqlite3 import Connection
from typing import List, Optional, Dict

import exporter
from models import Message, Chat


def query_messages(con: Connection, key_remote_jid: str, contacts: Dict[str, Optional[str]]) -> List[Message]:
    cur = con.cursor()
    query = """
            SELECT received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type 
            FROM messages 
            WHERE key_remote_jid =:key_remote_jid
            ORDER BY max(receipt_server_timestamp, received_timestamp)"""

    messages = []
    for received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type in cur.execute(query, {"key_remote_jid": key_remote_jid}):
        messages.append(
            Message(received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type, contacts.get(remote_resource, None))
        )
    return messages


def query_all_chats(db_path: str, contacts: Dict[str, Optional[str]]) -> List[Chat]:
    chats = []
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = "SELECT raw_string_jid as key_remote_jid, subject, sort_timestamp FROM chat_view ORDER BY sort_timestamp DESC"
    for key_remote_jid, subject, sort_timestamp in cur.execute(query):
        chats.append(
            Chat(key_remote_jid, subject, sort_timestamp, contacts.get(key_remote_jid, None), query_messages(con, key_remote_jid, contacts))
        )
    con.close()
    return chats


def query_contacts(db_path: str) -> Dict[str, Optional[str]]:
    contacts = {}
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for jid, wa_name in cur.execute("SELECT jid, wa_name from wa_contacts"):
        contacts[jid] = wa_name
    con.close()
    return contacts


def main():
    print("### WhatsApp Database Exporter ###")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    print("[+] Reading Database")
    if config["input"].getboolean("use_wa_db"):
        contacts = query_contacts(config["input"].get("wa_path"))
    else:
        contacts = {}
    chats = query_all_chats(config["input"].get("msgstore_path"), contacts)

    if config["output"].getboolean("export_html"):
        print("[+] Exporting to HTML")
        exporter.chats_to_html(chats, config["output"].get("html_output_path"))
    if config["output"].getboolean("export_txt"):
        print("[+] Exporting to txt files")
        exporter.chats_to_txt(chats, config["output"].get("txt_output_directory_path"))
    print("[+] Finished")


if __name__ == "__main__":
    main()
