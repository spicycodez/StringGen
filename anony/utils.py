from pyrogram import types, __version__ as pv
from telethon import __version__ as tv

from config import SUPPORT_CHAT

class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def gen_key(self) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=f"ᴩʏʀᴏɢʀᴀᴍ v{pv}", callback_data="pyrogram"),
                    self.ikb(text=f"ᴛᴇʟᴇᴛʜᴏɴ v{tv}", callback_data="telethon"),
                ]
            ]
        )

    def pm_key(self, user_id: int) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs",
                        url=f"tg://openmessage?user_id={user_id}",
                    )
                ]
            ]
        )

    def retry_key(self) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [[self.ikb(text="ᴛʀʏ ᴀɢᴀɪɴ", callback_data="generate")]]
        )

    def start_key(self) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [self.ikb(text="• ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ •", callback_data="generate")],
                [
                    self.ikb(text=" ᴄʜᴀɴɴᴇʟ ", url=SUPPORT_CHAT),
                    self.ikb(text=" sᴏᴜʀᴄᴇ ", url="https://t.me/SpicyxBots"),
                ],
            ]
        )
