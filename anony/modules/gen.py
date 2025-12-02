import asyncio

from pyrogram import Client, errors, filters, types, StopPropagation
from telethon import errors as telerror, TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from config import SUPPORT_CHAT
from anony import app, buttons


async def listen(cq: types.CallbackQuery, text: str, timeout: int = 120) -> str:
    try:
        await cq.message.reply_text(text)
        message = await app.listen.Message(filters.text, id=filters.user(cq.from_user.id), timeout=timeout)
        return message.text
    except asyncio.TimeoutError:
        await cq.message.reply_text("» ᴛɪᴍᴇᴅ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 5 ᴍɪɴᴜᴛᴇs.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())
        raise StopPropagation


@app.on_callback_query(filters.regex("generate"))
async def _generate(_, cq: types.CallbackQuery):
    await cq.answer()
    await cq.message.reply_text("<b>» ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ғᴏʀ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ :</b>", reply_markup=buttons.gen_key())

@app.on_callback_query(filters.regex(r"(pyrogram|telethon)"))
async def _gen_session(_, cq: types.CallbackQuery):
    sgen = cq.data
    pyrogram = sgen == "pyrogram"
    await cq.answer()
    await cq.message.reply_text(f"» ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ {sgen} sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ...")

    api_id = await listen(cq, "» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴀᴘɪ ɪᴅ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :")
    try:
        api_id = int(api_id)
    except ValueError:
        return await cq.message.reply_text("» ᴛʜᴇ ᴀᴘɪ ɪᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())

    api_hash = await listen(cq, "» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴀᴘɪ ʜᴀsʜ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :")
    if len(api_hash) < 30:
        return await cq.message.reply_text("» ᴛʜᴇ ᴀᴘɪ ʜᴀsʜ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())

    phone_number = await listen(cq, "» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :")
    await cq.message.reply_text("» ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴏᴛᴩ ᴀᴛ ᴛʜᴇ ɢɪᴠᴇɴ ɴᴜᴍʙᴇʀ...")
    client = (
        Client(name="Anony", api_id=api_id, api_hash=api_hash, in_memory=True)
        if pyrogram
        else TelegramClient(StringSession(), api_id, api_hash)
    )
    await client.connect()

    try:
        code = (
            await client.send_code(phone_number)
            if pyrogram
            else await client.send_code_request(phone_number)
        )
        await asyncio.sleep(1)

    except errors.FloodWait as f:
        return await cq.message.reply_text(f"» ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴄᴏᴅᴇ ғᴏʀ ʟᴏɢɪɴ.\n\nᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ {f.value} sᴇᴄᴏɴᴅs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())
    except (errors.ApiIdInvalid, telerror.ApiIdInvalidError):
        return await cq.message.reply_text("» ᴀᴘɪ ɪᴅ ᴏʀ ᴀᴘɪ ʜᴀsʜ ɪs ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())
    except (errors.PhoneNumberInvalid, telerror.PhoneNumberInvalidError):
        return await cq.message.reply_text("» ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴᴠᴀʟɪᴅ.\n\nᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())
    except Exception as ex:
        return await cq.message.reply_text(f"Error : <code>{str(ex)}</code>")

    otp = await listen(cq, f"ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴘ sᴇɴᴛ ᴛᴏ {phone_number}.\n\nɪғ ᴏᴛᴩ ɪs <code>12345</code>, ᴩʟᴇᴀsᴇ sᴇɴᴅ ɪᴛ ᴀs <code>1 2 3 4 5</code>", timeout=600)
    otp = otp.replace(" ", "")
    try:
        (
            await client.sign_in(phone_number, code.phone_code_hash, otp)
            if pyrogram
            else await client.sign_in(phone_number, otp)
        )
    except (errors.PhoneCodeInvalid, telerror.PhoneCodeInvalidError):
        return await cq.message.reply_text("» ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs <b>ᴡʀᴏɴɢ.</b>\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())
    except (errors.PhoneCodeExpired, telerror.PhoneCodeExpiredError):
        return await cq.message.reply_text("» ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs <b>ᴇxᴩɪʀᴇᴅ.</b>\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())
    except (errors.SessionPasswordNeeded, telerror.SessionPasswordNeededError):
        pwd = await listen(cq, "» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴛᴡᴏ sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘᴀssᴡᴏʀᴅ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ :")

        try:
            (
                await client.check_password(password=pwd)
                if pyrogram
                else await client.sign_in(password=pwd)
            )
        except (errors.PasswordHashInvalid, telerror.PasswordHashInvalidError):
            return await cq.message.reply_text("» ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ᴡʀᴏɴɢ.\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=buttons.retry_key())

    except Exception as ex:
         return await cq.message.reply_text(f"ᴇʀʀᴏʀ : <code>{str(ex)}</code>")

    try:
        txt = "ʜᴇʀᴇ ɪs ʏᴏᴜʀ {0} sᴛʀɪɴɢ sᴇssɪᴏɴ\n\n<code>{1}</code>\n\nᴀ sᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ ʙʏ <a href={2}>Spicy Bots</a>\n☠ <b>ɴᴏᴛᴇ :</b> ᴅᴏɴ'ᴛ sʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ʏᴏᴜʀ ɢɪʀʟғʀɪᴇɴᴅ."
        if pyrogram:
            string_session = await client.export_session_string()
            await client.send_message(
                "me",
                txt.format(sgen, string_session, SUPPORT_CHAT),
                link_preview_options=types.LinkPreviewOptions(is_disabled=True),
            )
            try:
                await client.join_chat("SpicyxNetwork")
            except:
                pass
        else:
            string_session = client.session.save()
            await client.send_message(
                "me",
                txt.format(sgen, string_session, SUPPORT_CHAT),
                link_preview=False,
                parse_mode="html",
            )
            try:
                await client(JoinChannelRequest("@SpicyxNetwork"))
            except:
                pass
    except KeyError:
        pass
    try:
        await client.disconnect()
        await cq.message.reply_text(f"Successfully generated your {sgen} string session.\n\nPlease check your saved messages for getting it.\n\nA string generator bot by <a href={SUPPORT_CHAT}>Spicy Bots</a>.", reply_markup=buttons.pm_key(cq.from_user.id))
    except:
        pass
