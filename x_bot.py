# -*- coding: utf-8 -*-
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.handlers import (
	MessageHandler, DeletedMessagesHandler,
	EditedMessageHandler, InlineQueryHandler, CallbackQueryHandler
)
from handler_1 import owner_user_permision_control, owner_user_inline_query, owner_user_callback_query

from Models import (
	RequestedLink
)

import datetime
from datetime import timedelta
import os, glob


api_key = "18472436"
api_hash = "52860d3c4cf613852662077aaf2c66d1"
bot_token = "6251525565:AAFWYyyEhfVEXCyNV8Uq5_OGtFWBgD-Q2-c"
app = Client("X_Video_Bot", api_key, api_hash, bot_token=bot_token)


##############################################################################################
################################# Save And Send All Messages #################################
##############################################################################################
# ------------------ Save All Message
# app.add_handler(MessageHandler(save_all_message), group=0)
# ------------------ Save All Deleted Message
# app.add_handler(DeletedMessagesHandler(save_all_message_deleted), group=1)
# ------------------ Save All Edited Message
# app.add_handler(EditedMessageHandler(save_all_message_edited), group=2)

# ------------------ Add Owner Bot Permision In SendMessage
# app.add_handler(MessageHandler(owner_permision_control), group=3)
# ------------------ Add Owner Bot Permision In EditMessage
# app.add_handler(EditedMessageHandler(owner_permision_control), group=4)
# ------------------ Add Edit Delete Permision In SendMessage
# app.add_handler(MessageHandler(permision_control), group=5)
# ------------------ Add Edit Delete Permision In EditMessage
# app.add_handler(EditedMessageHandler(permision_control), group=6)

# ------------------ Chat And Group Lock
# app.add_handler(MessageHandler(chat_and_group_lock), group=7)
# app.add_handler(EditedMessageHandler(chat_and_group_lock), group=7)

# ------------------ Send User Deleted Message In SendMessage
# app.add_handler(MessageHandler(show_last_deleted_message, filters=filters.text), group=13)
# ------------------ Send User Deleted Message In EditMessage
# app.add_handler(EditedMessageHandler(show_last_deleted_message, filters=filters.text), group=14)
# ------------------ Send User Edited Message In SendMessage
# app.add_handler(MessageHandler(show_last_edited_message, filters=filters.text), group=15)
# ------------------ Send User Edited Message In EditMessage
# app.add_handler(EditedMessageHandler(show_last_edited_message, filters=filters.text), group=16)
##############################################################################################
#################################### Control All Messages ####################################
##############################################################################################
# ------------------ Control common_user In SendMessage
# app.add_handler(MessageHandler(common_user_permision_control, filters=filters.text), group=17)
# ------------------ Control common_user In EditMessage
# app.add_handler(EditedMessageHandler(common_user_permision_control, filters=filters.text), group=18)

# ------------------ Control special_user In SendMessage
# app.add_handler(MessageHandler(special_user_permision_control, filters=filters.text), group=19)
# ------------------ Control special_user In EditMessage
# app.add_handler(EditedMessageHandler(special_user_permision_control, filters=filters.text), group=20)

# ------------------ Control admin_user In SendMessage
# app.add_handler(MessageHandler(admin_user_permision_control, filters=filters.text), group=21)
# ------------------ Control admin_user In EditMessage
# app.add_handler(EditedMessageHandler(admin_user_permision_control, filters=filters.text), group=22)

# ------------------ Control owner_user In SendMessage
app.add_handler(MessageHandler(owner_user_permision_control, filters=filters.text), group=0)
# ------------------ Control owner_user In EditMessage
# app.add_handler(EditedMessageHandler(owner_user_permision_control, filters=filters.text), group=24)

# ------------------ Control owner_user In InlineQueryHandler
app.add_handler(InlineQueryHandler(owner_user_inline_query), group=1)

# ------------------ Control owner_user In CallbackQueryHandler
app.add_handler(CallbackQueryHandler(owner_user_callback_query), group=2)



async def loop_del():
    messages_ = [i for i in RequestedLink.select()]
    for item in messages_:
        if datetime.datetime.now() > item.send_time + timedelta(seconds = 20):
            await app.delete_messages(int(item.chat_id), int(item.message_id))
            item.delete_instance()

async def loop_del_1():
    list_of_file = glob.glob('*.mp4')
    for filePath in list_of_file:
        try:
            os.remove(filePath)
        except:
            pass

scheduler = AsyncIOScheduler()
scheduler.add_job(loop_del, "interval", seconds=7)

scheduler.start()

scheduler_1 = AsyncIOScheduler()
scheduler_1.add_job(loop_del_1, "interval", seconds=60)

scheduler_1.start()

print("Run")

app.run()