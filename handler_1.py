
import itertools
from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultArticle,
    InlineQuery,
    Message as M,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InputMediaVideo
)
import wget
import asyncio, uuid, urllib.request
from bs4 import BeautifulSoup
import requests
import re
from pyrogram.errors import FileReferenceExpired

from Models import (
	ShortenLink, RequestedLink
)

import datetime

from uuid import uuid4

import os, time
import cv2


btn_reply_markup=InlineKeyboardMarkup(
  [
    [  # First row
      InlineKeyboardButton(  # Opens a web URL
        "📽 چنل یوتیوب 📽",
        url="https://youtube.com/@Genshin.island?si=KVHx_Kju9IfG0XNc"
      ),
    ],
    [  # Second row
      InlineKeyboardButton(  # Opens a web URL
        "🔰 چنل تلگرام 🔰",
        url="https://t.me/Genshin_Island"
      ),
    ],
        [  # Second row
      InlineKeyboardButton(  # Opens a web URL
        "👥 گروه تلگرام 👥",
        url="https://t.me/genshin_island_GP"
      ),
    ],
        [  # Second row
      InlineKeyboardButton(  # Opens a web URL
        "📸 صفحه اینستاگرام 📸",
        url="https://instagram.com/genshin.ir?igshid=MzRlODBiNWFlZA=="
      ),
    ],
        [  # Second row
      InlineKeyboardButton(  # Opens a web URL
        "🎧 چنل دیسکورد 🎧",
        url="https://discord.gg/genshin-island-963423034641903616"
      ),
    ],
        [  # Second row
      InlineKeyboardButton(  # Opens a web URL
        "💰 چنل خرید و فروش اکانت 💰",
        url="https://t.me/Genshin_Impact_Trade_IR"
      ),
    ]
  ]
)

async def get_date_time(date:str):
	"""
		convert date like 2022-12-16 10:08:29
	"""
	if date != "None":
		ymd = date.split(" ")[0] # 2022-12-16
		time = date.split(" ")[1] # 10:08:29

		year = int(ymd.split("-")[0]) # 2022
		month = int(ymd.split("-")[1]) # 12
		day = int(ymd.split("-")[2]) # 16

		hour = int(time.split(":")[0]) # 10
		minute = int(time.split(":")[1]) # 08
		second = int(time.split(":")[2]) # 29
		return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second,)
	else:
		return datetime.datetime(2079, 1, 1)


async def downloadLink(link):
    url = str(link)
    link_list = []
    responce = requests.get(url).content
    soup = BeautifulSoup(responce, "html.parser")
    result = soup.findAll("script")
    result = str(result)
    tag = re.findall(r"html5player+\.+setVideoUrl\w{3,4}\('.+'+", result)
    for item in tag:
        str_tag = str(item)
        replaced_str_tag1 = re.sub(r"html5player\.setVideoUrlLow\('", "",
                                    str_tag)
        replaced_str_tag2 = re.sub(r"html5player\.setVideoUrlHigh\('", "",
                                    replaced_str_tag1)
        replaced_str_tag3 = re.sub(r"'", "", replaced_str_tag2)
        link_list.append(replaced_str_tag3)
    try:
        return link_list[1]
    except:
        return link_list[0]

async def xvideosLink(query, page=0):
    query = query.replace(" ", "+")
    if page == 0:
        url = f"https://www.xvideos.com/?k={query}"
    else:
        url = f"https://www.xvideos.com/?k={query}&p={page}"
    link_list_name = []
    link_list = []
    uuid4_list = []
    link_list_image = []
    cookies = {}
    responce = requests.get(url, cookies=cookies).content
    soup = BeautifulSoup(responce, "html.parser")
    result = soup.select("p.title > a")

    for item in result:
        link_list_name.append(item.text)

    result = soup.select(".thumb img")

    for item in result:
        link_list_image.append(item["data-src"])

    result = soup.select("p.title > a")

    for item in result:
        if item["href"][:6] == "/video":
            link_list.append(f"https://www.xvideos.com{item['href']}")
            _uuid = str(uuid4())
            uuid4_list.append(_uuid)
            file_s = ShortenLink.get_or_none(
                link=f"https://www.xvideos.com{item['href']}",
            )
            if file_s == None:
                ShortenLink.create(
                    u_id=_uuid,
                    link=f"https://www.xvideos.com{item['href']}",
                )
    
    return link_list, link_list_image, link_list_name, uuid4_list



async def xvideosLinkTag(query, page=1):
    query = query.replace(" ", "-")
    if page == 1:
        url = f"https://www.xvideos.com/tags/{query}"
    else:
        url = f"https://www.xvideos.com/tags/{query}/{page}"
    link_list_name = []
    link_list = []
    uuid4_list = []
    link_list_image = []
    cookies = {}
    responce = requests.get(url, cookies=cookies).content
    soup = BeautifulSoup(responce, "html.parser")
    result = soup.select("p.title > a")

    for item in result:
        link_list_name.append(item.text)

    result = soup.select(".thumb img")

    for item in result:
        link_list_image.append(item["data-src"])

    result = soup.select("p.title > a")

    for item in result:
        if item["href"][:6] == "/video":
            link_list.append(f"https://www.xvideos.com{item['href']}")
            _uuid = str(uuid4())
            uuid4_list.append(_uuid)
            file_s = ShortenLink.get_or_none(
                link=f"https://www.xvideos.com{item['href']}",
            )
            if file_s == None:
                ShortenLink.create(
                    u_id=_uuid,
                    link=f"https://www.xvideos.com{item['href']}",
                )
    
    return link_list, link_list_image, link_list_name, uuid4_list


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return [[e for e in t if e != None] for t in itertools.zip_longest(*args)]


def myFunc_sort(e):
    return e.word_id

async def get_file_on_server(url):
    return wget.download(url)
    


async def owner_user_permision_control(c: Client, m: M):

    text = m.text.lower()
    
    if text == "btn":
        await m.reply_photo("xiao.jpg", caption="""🏝 جزیره ی گنشین 🏝

🌐با بهترین کیفیت برای شما عزیزان در زمینه ی بازی گنشین و... رو می تونید در چنل های زیر ببینید و دنبال کنید.""", 
        reply_markup=btn_reply_markup,
    )
    
    if text=="/help":
        file_name = "File/Filw_2.mp4"
        cap = """@XVIDEOS_sexy_bot   @XVIDEOS_sexy_bot

تبلیغات نمی کنم چون کارم درسته پولم که نمی خواد بدی پس بیا خجالت نکش

ربات برای دسترسی مستقیم به فیلم های سایت 
Xvideos.com
هستش 

😊 جهت کار با ربات کافی است :
۱ - علامت + رو بنویس
۲ -  شماره صفحه مورد نظر ( معمولا صفحه 1 ) را بنویس و علامت ; رو پیدا کن و بنویس
۳ - عبارت مورد نظر ( نوع دسته بندی سکس، نوع پوزیشن، قسمت مربوطه، سبک مورد نظر ... ) را وارد بنویس

 حالا عبارت نوشته شده رو ارسال کن برای بات

مثل : 
+1;cute teen
یا
+3;sexy

@XVIDEOS_sexy_bot   @XVIDEOS_sexy_bot

برای کار با کوئری اینلاین کافی است یوزر نیم ربات را در چت های خود ( مثلا چت گروه ها، چت سیو مسیج، چت دوستاتون ) بنویسید سپس عبارت مورد نظر را وارد نموده و اندکی صبر نمایید برای وارد کردن شماره صفحه از علامت ; استفاده کنید

مثل : 
@XVIDEOS_sexy_bot cute
یا
@XVIDEOS_sexy_bot sexy;3

روز و روزگار خوش 😁"""
        mess = await m.reply_video(file_name, duration=20, caption=cap)
    
    if text.startswith("?"):
        val = str(text[1:]).strip()
        try:
            warr_1 = await m.reply("در حال انجام")
            download_links = await downloadLink(val)
            warr_2 = await m.reply("در حال دریافت فایل")
            file_name = await get_file_on_server(download_links)
            warr_3 = await m.reply("در حال آپلود روی سرور")
            data = cv2.VideoCapture(f'{file_name}')
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = data.get(cv2.CAP_PROP_FPS)
            duration = round(frames / fps)
            mess = await m.reply_video(file_name, caption="بعد از 20 ثانیه پاک می شود", duration=int(duration))
            RequestedLink.get_or_create(
                link = val,
                message_id = mess.id,
                chat_id = m.chat.id,
                send_time = await get_date_time(str(mess.date))
            )
            os.remove(file_name)
            await warr_1.delete()
            await warr_2.delete()
            await warr_3.delete()
        except Exception as error_bot:
            await m.reply(error_bot, quote=True)
        # await m.reply(f"[دانلود]({download_links})", quote=True)

    if text.startswith("/"):
        val = str(text[1:]).strip()
        try:
            warr_1 = await m.reply("در حال انجام")
            download_links = await downloadLink(val)
            warr_2 = await m.reply("در حال دریافت فایل")
            file_name = await get_file_on_server(download_links)
            warr_3 = await m.reply("در حال آپلود روی سرور")
            data = cv2.VideoCapture(f'{file_name}')
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = data.get(cv2.CAP_PROP_FPS)
            duration = round(frames / fps)
            mess = await m.reply_video(file_name, caption="بعد از 20 ثانیه پاک می شود", duration=int(duration))
            RequestedLink.get_or_create(
                link = val,
                message_id = mess.id,
                chat_id = m.chat.id,
                send_time = await get_date_time(str(mess.date))
            )
            os.remove(file_name)
            await warr_1.delete()
            await warr_2.delete()
            await warr_3.delete()
        except Exception as error_bot:
            await m.reply("مشکلی رخ داده است", quote=True)
            await m.reply(error_bot, quote=True)
            
    elif text.startswith("+"):
        text = text[1:]
        query = text.split(";")[1]
        try: 
            count = int(text.split(";")[0].strip())
        except:
            count = 0
        result = await xvideosLink(query, count if count > -1 else 0)
        links = result[0]
        pics = result[1]
        for i in range(len(links)):
            try:
                await m.reply_photo(f"{pics[i]}", caption="`?" + f"{links[i]}`")
            except:
                pass
            
    elif text.startswith("-"):
        text = text[1:]
        query = text.split(";")[1]
        try: 
            count = int(text.split(";")[0].strip())
        except:
            count = 0
        result = await xvideosLinkTag(query, count if count > 0 else 1)
        links = result[0]
        pics = result[1]
        for i in range(len(links)):
            try:
                await m.reply_photo(f"{pics[i]}", caption="`?" + f"{links[i]}`")
            except:
                pass


async def owner_user_inline_query(c: Client, i:InlineQuery):
    if i.query != "":
        results = []
        if i.query.startswith("-"):
            query = i.query.split(";")[0]
            try:
                count = int(i.query.split(";")[1].strip()) if len(i.query.split(";")) > 1 else 1
            except:
                count = 1
                
            result_1 = await xvideosLinkTag(query.replace("-", "").strip(), count if count > 0 else 1)
            links_1 = result_1[0]
            pics_1 = result_1[1]
            names_1 = result_1[2]
            uuid4s_1 = result_1[3]
            
            for item in range(len(links_1)):
                results.append(
                    InlineQueryResultArticle(
                        title=f"{names_1[item]}",
                        input_message_content=InputTextMessageContent(
                            f"`?{links_1[item]}`"
                        ),
                        description=f"{links_1[item]}",
                        thumb_url =f"{pics_1[item]}",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    f"{names_1[item][:25]} ...",
                                    callback_data=f"l:{uuid4s_1[item]}"
                                )]
                            ]
                        )
                    ),
                )
            
        else:
            results = []
            query = i.query.split(";")[0]
            try:
                count = int(i.query.split(";")[1].strip()) if len(i.query.split(";")) > 1 else 0
            except:
                count = 0
            result = await xvideosLink(query, count if count > -1 else 0)
            links = result[0]
            pics = result[1]
            names = result[2]
            uuid4s = result[3]
            
            for item in range(len(links)):
                results.append(
                    InlineQueryResultArticle(
                        title=f"{names[item]}",
                        input_message_content=InputTextMessageContent(
                            f"`?{links[item]}`"
                        ),
                        description=f"{links[item]}",
                        thumb_url =f"{pics[item]}",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    f"{names[item][:25]} ...",
                                    callback_data=f"l:{uuid4s[item]}"
                                )]
                            ]
                        )
                    ),
                )
        
        await i.answer(results, cache_time=1)
            


async def owner_user_callback_query(_:Client, e:CallbackQuery):
    if e.data.startswith("l:"):
        value = e.data.replace("l:", "")
        _link = ShortenLink.get_or_none(
            u_id=value
        )
        try:
            download_links = await downloadLink(_link.link)
            file_name = await get_file_on_server(download_links)
            data = cv2.VideoCapture(f'{file_name}')
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = data.get(cv2.CAP_PROP_FPS)
            duration = round(frames / fps)
            mess = await _.send_video(
                chat_id=e.from_user.id,
                video=file_name,
                caption="بعد از 20 ثانیه پاک می شود",
                duration=duration
            )
            RequestedLink.get_or_create(
                link = _link,
                message_id = mess.id,
                chat_id = e.from_user.id,
                send_time = await get_date_time(str(mess.date))
            )
            os.remove(file_name)
        except Exception as eeeeeee:
            await _.send_message(
                chat_id=e.from_user.id,
                text=f"{eeeeeee}"
            )
            
        
        
