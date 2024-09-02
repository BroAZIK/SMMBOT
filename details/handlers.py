from telegram import Update, InputFile, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.parsemode import ParseMode
from pprint import pprint
from .message import *
from .buttons import *
from settings import *
from database.db import *

def start(update: Update, context):
    user_id = update.effective_chat.id

    if user_id != ADMIN_ID:
        status = context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id).status
        if status in ["member", "administrator", "creator"]:
            try:
                insert(table="index", user_id=user_id, data={"Stage": "start", "edit_id": 0})
            except:
                upd(table="index", user_id=user_id, data={"Stage": "start", "edit_id": 0})

            update.message.reply_text(
                text=start_mes.format(update.effective_chat.full_name),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(start_but, resize_keyboard=True)
            )
            update.message.reply_text(
                text=start_mes2,
                parse_mode=ParseMode.HTML
            )
        else:
            update.message.reply_text(
                text=non_sub_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=InlineKeyboardMarkup(non_sub_but)
            )

        
    else:
        try:
            insert(table="index", user_id=user_id, data={"Stage": "start", "edit_id": 0})
        except:
            upd(table="index", user_id=user_id, data={"Stage": "start", "edit_id": 0})
        update.message.reply_text(
            text=admin_start_mes,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
        )

def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.answer()

    if query.data == 'check':
        check(update, context)

    if query.data == "info":
        context.bot.send_message(chat_id = update.effective_chat.id,text=info_message, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(start_but))
        context.bot.send_message(chat_id = update.effective_chat.id,text=start_mes2, parse_mode=ParseMode.HTML)
    
    if query.data == "stats":
        len_users = len(get(table="all_users"))
        len_bases = len(get(table="medias"))
        data = db2.all()
        len_service = sum(item.get("loads", 0) for item in data if isinstance(item, dict))
        context.bot.sendMessage(
            chat_id=query.from_user.id,
            text=stats_mes.format(len_users, len_bases, len_service),
            parse_mode=ParseMode.HTML
        )
        context.bot.sendMessage(
            chat_id=query.from_user.id,
            text=start_mes2,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(start_but)
        )
        
def check(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = update.effective_chat.id
    message_id = query.message.message_id
    status = context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id).status

    if status in ["member", "administrator", "creator"]:
        try:
            insert(table="index", user_id=user_id, data={"Stage": "start", "edit_id": 0})
        except:
            upd(table="index", user_id=user_id, data={"Stage": "start", "edit_id": 0})
    
        
        context.bot.delete_message(chat_id=user_id, message_id=message_id)
        context.bot.send_message(chat_id=user_id, text=start_mes.format(update.effective_chat.first_name), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(start_but))
        context.bot.send_message(chat_id=user_id, text=start_mes2, parse_mode=ParseMode.HTML)
    else:
        context.bot.delete_message(chat_id=user_id, message_id=message_id)
        context.bot.send_message(chat_id=user_id, text="Iltimos, avval kanalga qo'shiling.",
                reply_markup=InlineKeyboardMarkup(non_sub_but))

def text(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    mess = update.message.text
    status = context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id).status
    stage = get(table="index", user_id=user_id)["Stage"]
    edit_id = get(table="index", user_id=user_id)["edit_id"]

    if mess == "Statistika📊":
        len_users = len(get(table="all_users"))
        len_bases = len(get(table="medias"))
        data = db2.all()
        len_service = sum(item.get("loads", 0) for item in data if isinstance(item, dict))
        update.message.reply_text(
            text=stats_mes.format(len_users, len_bases, len_service),
            parse_mode=ParseMode.HTML)

        update.message.reply_text(
            text=f"<b>Ruxsatlangan itemlar:</b>👇🏻\n{ALLOWED_ITEMS}",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
        )


    if mess == "Ortga⬅️":
        upd(table="index", user_id=user_id, data={"Stage": "start"})
        update.message.reply_text(
                text=admin_start_mes,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
        stage = get(table="index", user_id=user_id)["Stage"]
        if stage == "add" or stage == "get_caption":
            delete_info = delete(media_id=edit_id)
            if delete_info == True:
                update.message.reply_text(
                    text=delete2_mes,
                    parse_mode=ParseMode.HTML,
                    reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
                )
                upd(table="index", user_id=user_id, data={"Stage": "start", "edit_id": 0})
            if delete_info == False:
                update.message.reply_text(
                    text=not_delete_mes,
                    parse_mode=ParseMode.HTML,
                    reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
                )

    if stage == 'add':
        doccer_id = insert(table="media", data={"text": mess, "loads": 0, "type": "text"})
        update.message.reply_text(
            text=text_mes.format(mess, doccer_id,0, CHANNEL_ID),
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
        )
        context.bot.send_message(
            chat_id=LOG_ID,
            text=text_mes.format(mess, doccer_id,0, CHANNEL_ID),
            parse_mode=ParseMode.HTML,
            )
        update.message.reply_text(
                text=succesfully_adding_mes.format(doccer_id),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
        upd(table="index", user_id=user_id, data={"Stage": "start"})




    if stage == "get_caption":
        upd(table="media", media=edit_id, data={"caption": mess, "doccer_id": edit_id})
        item = get(table="media", media_id=edit_id)
        item_type = item['type']

        if item_type == "video":
            update.message.reply_video(
                video=item["file_id"],
                caption=video_caption_mes.format(item["caption"],
                            item["duration"], 
                            round(item["size"] / 1028, 2),
                            edit_id,
                            item['loads'],
                            CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML
            )
            context.bot.send_video(
                            chat_id=LOG_ID,
                video=item["file_id"],
                caption=video_caption_mes.format(item["caption"],
                            item["duration"], 
                            round(item["size"] / 1028, 2),
                            edit_id,
                            item['loads'],
                            CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML
                            )
            update.message.reply_text(
                text=succesfully_adding_mes.format(item_type),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
            upd(table="index", user_id=user_id, data={"Stage": "start"})

        if item_type == "photo":
            update.message.reply_photo(
                photo=item["file_id"],
                caption=photo_caption_mes.format(item["caption"],
                            edit_id,
                            item['loads'],
                            CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML
            )
            context.bot.send_photo(
                            chat_id=LOG_ID,
                            photo=item["file_id"],
                            caption=photo_caption_mes.format(item["caption"],
                            edit_id,
                            item['loads'],
                            CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML)
            
            update.message.reply_text(
                text=succesfully_adding_mes.format(item_type),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
            upd(table="index", user_id=user_id, data={"Stage": "start"})

        if item_type == "document":
            update.message.reply_document(
                document=item['file_id'],
                caption=document_mes.format(
                    item['caption'],
                    edit_id,
                    item['loads'],
                    CHANNEL_ID
                ),
                parse_mode=ParseMode.HTML
            )
            context.bot.send_document(
                            chat_id=LOG_ID,
                document=item['file_id'],
                caption=document_mes.format(
                    item['caption'],
                    edit_id,
                    item['loads'],
                    CHANNEL_ID
                ),
                parse_mode=ParseMode.HTML)
            
            update.message.reply_text(
                text=succesfully_adding_mes.format(item_type),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
            upd(table="index", user_id=user_id, data={"Stage": "start"})
    
        if item_type == "music":
            update.message.reply_audio(
                audio=item['file_id'],
                performer=item['performer'],
                title=item['title'],
                thumb=item['logo'],
                caption=music_mes.format(
                    item['caption'],
                    edit_id,
                    item['loads'],
                    CHANNEL_ID
                    ),
                    parse_mode=ParseMode.HTML
            )
            context.bot.send_audio(
                            chat_id=LOG_ID,
                            audio=item['file_id'],
                            performer=item['performer'],
                            title=item['title'],
                            thumb=item['logo'],
                            caption=music_mes.format(
                            item['caption'],
                            edit_id,
                            item['loads'],
                            CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML
                            )

            update.message.reply_text(
                text=succesfully_adding_mes.format(item_type),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
            upd(table="index", user_id=user_id, data={"Stage": "start"})

    if stage == "delete":
        upd(table="index", user_id=user_id, data={"Stage": "start"})
        delete_info = delete(media_id=int(mess))

        if delete_info == True:
            update.message.reply_text(
                text=delete2_mes,
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
        else:
            update.message.reply_text(
                text=not_delete_mes,
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(admin_start_but, resize_keyboard=True)
            )
    
    if mess == "Olib tashlash🗑":
        upd(table="index", user_id=user_id, data={"Stage": "delete"})

        update.message.reply_text(
            text=delete_mes,
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True)
        )

    if user_id != ADMIN_ID:
        if status in ["member", "administrator", "creator"]:
        
            if mess.isdigit():
                media = get(table="media", media_id=mess)
                if media == []:
                    update.message.reply_text(
                        text=not_found_mes.format(mess),
                        parse_mode=ParseMode.HTML
                    )
                else:
                    if media['type'] == "video":
                        update.message.reply_video(
                            video=media['file_id'],
                            caption=video_caption_mes.format(
                                media['caption'],
                                media['duration'],
                                round(media['size'] / 1028),
                                mess,
                                media['loads'],
                                CHANNEL_ID),
                            parse_mode=ParseMode.HTML,
                            # reply_markup=ReplyKeyboardMarkup(start_but, resize_keyboard=True)
                        )
                        

                    if media["type"] == "photo":
                        update.message.reply_photo(
                        photo=media["file_id"],
                        caption=photo_caption_mes.format(media["caption"],
                            mess,
                            media['loads'],
                            CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML
            )
                    
                    if media['type'] == "text":
                        update.message.reply_text(
                            text=text_mes.format(
                                media['text'],
                                mess,
                                media['loads'],
                                CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML
                        )

                    if media['type'] == "document":
                        update.message.reply_document(
                            document=media["file_id"],
                            caption=document_mes.format(
                                media['caption'],
                                mess,
                                media['loads'],
                                CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML
                        )

                    if media['type'] == "music":
                        update.message.reply_audio(
                            audio=media['file_id'],
                            performer=media['performer'],
                            title=media['title'],
                            thumb=media['logo'],
                            caption=music_mes.format(
                            media['caption'],
                            mess,
                            media['loads'],
                            CHANNEL_ID
                            ),
                            parse_mode=ParseMode.HTML)


                    update.message.reply_text(
                            text=start_mes2,
                            parse_mode=ParseMode.HTML,
                            reply_markup=InlineKeyboardMarkup(start_but)
                        )
            else:
                update.message.reply_text(
                        text=not_found_mes.format(mess),
                        parse_mode=ParseMode.HTML
                    )


        else:
            context.bot.delete_message(chat_id=user_id, message_id=update.message.message_id)
            context.bot.send_message(chat_id=user_id, text="Iltimos, avval kanalga qo'shiling.",
                reply_markup=InlineKeyboardMarkup(non_sub_but))
            
    else:
        if update.message.text == "Item qo'shish➕":
            upd(table="index", user_id=user_id, data={"Stage": "add"})
            
            update.message.reply_text(
                text=add_item_mes,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True)
            )

def video(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    video_id = update.message.video.file_id
    video_size = update.message.video.file_size
    video_duration = update.message.video.duration
    stage = get(table="index", user_id=user_id)["Stage"]

    if user_id == ADMIN_ID:
        if stage == "add":

            in_id = insert(table="media", data={
                "file_id": video_id,
                "size": video_size,
                "duration": video_duration,
                "type": "video",
                "loads": 0
            })
            upd(table="index", user_id=user_id, data={"edit_id": in_id})

            update.message.reply_text(
                text=send_caption_mes.format(in_id),
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True))
            upd(table="index", user_id=user_id, data={"Stage": "get_caption"})

def photo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    photo_i = update.message.photo
    stage = get(table="index", user_id=user_id)["Stage"]
    if user_id == ADMIN_ID:
        if stage == "add":

            in_id = insert(table="media", data={
                "file_id": photo_i[0]["file_id"],
                "type": "photo",
                "loads": 0
            })
            upd(table="index", user_id=user_id, data={"edit_id": in_id})

            update.message.reply_text(
                text=send_caption_mes.format(in_id),
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True))
            upd(table="index", user_id=user_id, data={"Stage": "get_caption"})

def document(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    file_id = update.message.document.file_id
    file_size = update.message.document.file_size
    stage = get(table="index", user_id=user_id)["Stage"]
    if user_id == ADMIN_ID:
        if stage == "add":

            in_id = insert(table="media", data={
                "file_id": file_id,
                "type": "document",
                "file_size": file_size,
                "loads": 0
            })
            upd(table="index", user_id=user_id, data={"edit_id": in_id})
            update.message.reply_text(
                text=send_caption_mes.format(in_id),
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True))
            upd(table="index", user_id=user_id, data={"Stage": "get_caption"})

def music(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    file_id = update.message.audio.file_id
    title = update.message.audio.title
    duration = update.message.audio.duration

    stage = get(table="index", user_id=user_id)["Stage"]
    if user_id == ADMIN_ID:
        if stage == "add":
            in_id = insert(table="media", data={
                "file_id": file_id,
                "performer": CHANNEL_ID,
                "title": title,
                "logo": LOGO_ID,
                "duration": duration,
                "loads": 0,
                "type": "music"
            })
            upd(table="index", user_id=user_id, data={"edit_id": in_id})
            update.message.reply_text(
                text=send_caption_mes.format(in_id),
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(back_but, resize_keyboard=True))
            upd(table="index", user_id=user_id, data={"Stage": "get_caption"})
