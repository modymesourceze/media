from config import Config
from telebot.async_telebot import AsyncTeleBot
# @ELHYBA & @Source_Ze
from telebot.types import Message, CallbackQuery,InlineKeyboardMarkup as Keyboard, InlineKeyboardButton as Button, InputFile as File
from funcs import read, write
from telemod import Listener
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from pytube import YouTube
import os, requests, asyncio, re, urllib.request, pytube


bot_token = Config.TG_BOT_TOKEN


app = AsyncTeleBot(
    token = bot_token, parse_mode="Markdown"
)

loop = asyncio.get_event_loop()

listener = Listener(bot=app, loop=loop)

users_db = "database/users.json"
channels_db = "database/channels.json"
banned_db = "database/banned.json"
others_db = "database/others.json"
admins_db = "database/admins.json"
users = read(users_db)
admins = read(admins_db)
others = read(others_db)
channels = read(channels_db)
banned = read(banned_db)
# @ELHYBA & @Source_Ze

async def subscription(user_id):
    if len(list(channels)) == 0:
            return False
    status = ["creator", "administrator", "member"]
    for channel in channels:
        member = await app.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status not in status:
            return {
                "channel" : channel,
            }
        return False

@app.message_handler(commands=["start"], chat_types=["private"])
async def start(message: Message):
    user_id = message.from_user.id
    if user_id in banned:
        await app.reply_to(
            message,
            "تم حظرك من استخدام البوت تواصل مع المطور ليرفع عنك الحظر."
        )
        return # @ELHYBA & @Source_Ze
    if user_id not in users:
        users.append(user_id)
        write(users_db, users)
        if others.get("options")["new_members_notice"]:
            for adminn in admins:
                caption: str = f"-> عضو جديد استخدم البوت 🔥\n\n-> ايدي : {user_id}\n-> يوزر : @{message.from_user. username}\n\n-> عدد الأعضاء الحاليين : {len(users)}"
                try:
                    await app.send_message(
                        int(adminn),
                        caption
                    )
                except:
                    continue
    subscribe =  await subscription(user_id)
    if subscribe:
        await app.reply_to(
            message,
            text=f"عذرا عزيزي\nعليك الإشتراك بقناة البوت أولا لتتمكن من استخدامه\n{subscribe['channel']}\nاشترك ثم ارسل : /start"
        )
        return # @ELHYBA & @Source_Ze
    await app.reply_to(
        message,
        text="مرحبا بك في بوت التحميل الميديا.\nيمكنك اختيار الموقع الذي تريد من الأزرار في الأسفل :",
        reply_markup=Keyboard([
            [
               Button("- Instagram -", callback_data="instagram"),
               Button("- TikTok -", callback_data="tiktok")
            ],
            [
                Button("- Pintrest -", callback_data="pintrest"),
                Button("- Snapchat -", callback_data="snapchat")
            ],
            [
                Button("- YouTube - ", callback_data="youtube"),
                Button("- SoundCloud -", callback_data="soundcloud") # @ELHYBA & @Source_Ze
            ],
            [
                Button("- المطور -", url="ELHYBA.t.me")
            ]
        ])
    )


@app.message_handler(regexp=r"^(المطور)$")
async def dev(message: Message):
    chat_id = 6581896306
    user = await app.get_chat(chat_id)
    user_bio = user.bio 
    nickname = user.first_name
    username = user.username
    photo_path = "developer.jpg"
    file_id= user.photo.big_file_id
    file_info = await app.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_info.file_path}"
    response = requests.get(file_url)
      
    with open(photo_path, "wb") as f:
        f.write(response.content)
    caption = user_bio
    markup = Keyboard([
        [
            Button(nickname, url=f"{username}.t.me")
        ]
    ]) # @ELHYBA & @Source_Ze
    await app.send_photo(
        chat_id=message.chat.id, 
        photo=File(file=photo_path),
        caption=caption, 
        reply_markup=markup
    )


@app.message_handler(commands=["admin"], chat_types="private")
async def admin(message: Message):
    user_id = message.from_user.id
    if user_id not in admins:
        await app.reply_to(
            message,
            text="هذا الأمر يخص المشرفين"
        )
        return # @ELHYBA & @Source_Ze
    markup = Keyboard(keyboard())
    info = await app.get_chat(user_id)
    admin_name = info.first_name
    caption = f"-> مرحبا عزيزي الأدمن ( `{admin_name}` )\n\n-> احصائيات: \n-> الأعضاء : {len(users)}\n-> المحظورين : {len(banned)}\n\n-> أوامر أخرى : \n- حظر + الأيدي\n- رفع حظر + الأيدي\n- رفع ادمن + الأيدي\n- تنزيل ادمن + الأيدي"
    await app.reply_to(
        message,
        text=caption,
        reply_markup=markup
    )
    # @ELHYBA & @Source_Ze

@app.message_handler(regexp=r"^(حظر)", chat_types=["private"])
async def ban(message: Message):
    user_id = message.from_user.id
    if user_id not in admins:
        await app.reply_to(
            message,
            text="هذا الأمر يخص المشرفين"
        )
        return
    member = message.text.split()[-1]
    if int(member) in admins:
        await app.reply_to(
            message,
            text="لا يمكنك حظر هذا المستخدم."
        )
        return
    if int(member) in banned:
        await app.reply_to(
            message,
            text="تم حظر هذا المستخدم من قبل."
        )
        return
    banned.append(int(member))
    write(banned_db, banned)
    await app.reply_to(
            message,
            text="تم حظر هذا المستخدم"
    )
    # @ELHYBA & @Source_Ze

@app.message_handler(regexp=r"^(رفع حظر)" , chat_types=["private"])
async def unban(message: Message):
    user_id = message.from_user.id
    if user_id not in admins:
        await app.reply_to(
            message,
            text="هذا الأمر يخص المشرفين"
        )
        return
    member = message.text.split()[-1]
    if int(member) in banned:
        banned.remove(int(member))
        write(banned_db, banned)
        await app.reply_to(
            message,
            text="تم رفع الحظر عن هذا المستخدم."
        )
        return # @ELHYBA & @Source_Ze
    await app.reply_to(
            message,
            text="لم يتم حظر هذا المستخدم من قبل."
    )
    
@app.message_handler(regexp=r"^(رفع ادمن)", chat_types=["private"])
async def promote(message: Message):
    user_id = message.from_user.id
    if user_id not in admins:
        await app.reply_to(
            message,
            text="هذا الأمر يخص المشرفين"
        )
        return
    member = message.text.split()[-1]
    if int(member) in admins:
        await app.reply_to(
            message,
            text="هذا المستخدم مشرف بالفعل."
        )
        return
    if int(member) in banned:
        await app.reply_to(
            message,
            text="هذا المستخدم تم حظره من قبل يرجى رفع الحظر ثم إعادة المحاوله."
        )
        return
    admins.append(int(member))
    write(admins_db, admins)
    await app.reply_to(
            message,
            text="تم ترقية المستخدم لرتبة مشرف"
    )
    
    
@app.message_handler(regexp=r"^(تنزيل ادمن)", chat_types=["private"])
async def demote(message: Message):
    user_id = message.from_user.id
    if user_id not in admins:
        await app.reply_to(
            message,
            text="هذا الأمر يخص المشرفين"
        )
        return
    member = message.text.split()[-1]
    if int(member) in admins:
        admins.remove(int(member))
        write(admins_db, admins)
        await app.reply_to(
            message,
            text="تم تنزيل هذا المستخدم من قائمة المشرفين."
        )
        return
    await app.reply_to(
            message,
            text="هذا المستخدم ليس من المشرفين."
    )


@app.callback_query_handler(
    func= lambda callback: callback.data in ["forward_from_users","new_members_notice"])
async def redefine(callback: CallbackQuery):
    data = callback.data
    others["options"][data] = True if not others["options"][data] else False
    write(others_db, others)
    await app.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,# @ELHYBA & @Source_Ze
        reply_markup=Keyboard(keyboard())
    )
    

@app.callback_query_handler(
    func= lambda callback: callback.data == "add_channel")
async def add_channel(callback: CallbackQuery):
    message = await listener.listen_to(m=callback, text="أرسل معرف القناه مع مبدوء ب @")
    channel = message.text
    try:
        await app.get_chat(channel)
    except :
        await app.reply_to(
            message,
            "لم يتم إيجاد هذه الدردشه."
        )
        return
    if channel in channels:
        await app.reply_to(
            message,
            "القناه موجوده بالفعل."
        )
        return
    channels.append(channel)
    write(channels_db, channels)
    await app.reply_to(
        message,
        "تمت إضافة القناه."
    )


@app.callback_query_handler(
    func= lambda callback: callback.data == "remove_channel")
async def remove_channel(callback: CallbackQuery):
    message = await listener.listen_to(m=callback, text="أرسل معرف القناه مع مبدوء ب @")
    channel = message.text
    if channel not in channels:
        await app.reply_to(
            message,
            "لم يتم إيجاد هذه الدردشه."
        )
        return
    channels.remove(channel)
    write(channels_db, channels)
    await app.reply_to(
            message,
        "تم حذف القناه."
    )


@app.callback_query_handler(
    func= lambda callback: callback.data == "current_channels")
async def current_channels(callback: CallbackQuery):
    caption = "- القنوات الحاليه :\n"
    text = "\n".join(channels)
    caption+=text
    await app.answer_callback_query(callback_query_id=callback.id , text = caption, show_alert=True)


@app.callback_query_handler(
    func= lambda callback: callback.data == "send_storage")
async def send_storage(callback: CallbackQuery):
    files_path = "database"
    files = os.listdir(files_path)
    for file in files:
        file_path = os.path.join(files_path, file)
        await app.send_document(
            callback.message.chat.id,
            document=File(file_path)
        )# @ELHYBA & @Source_Ze


# @ELHYBA & @Source_Ze
def instagram(url):
    headers = {
        'authority': 'reelsaver.net',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://reelsaver.net',
        'referer': 'https://reelsaver.net/download-reel-instagram',
        'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': generate_user_agent(),
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
    'via': 'form',
    'ref': 'download-reel-instagram',
    'url': url,}
    response = requests.post('https://reelsaver.net/api/instagram', headers=headers, data=data).json()
    if not response["success"]:
        return { "success" : False }
    user = response['data']['user']['username']
    video = response["data"]['medias'][0]['src']
    urls = { "video" : video, "username" : user , "success" : True}
    return urls


@app.callback_query_handler(
    func= lambda callback: callback.data == "instagram")
async def insta_vid(callback: CallbackQuery):
    user_id = callback.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await listener.listen_to(m=callback , text=caption)
    await app.delete_message(user_id, answer.id)
    await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="Processing...")
    url = answer.text
    response = instagram(url)
    if not response["success"]:
        await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="الرابط غير صالح")
        return # @ELHYBA & @Source_Ze
    bot = await app.get_me ()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● author : [{response['username']}](https://www.instagram.com/{response['username']})\n\n● Uploaded By : [{bot_name}]({bot_url})"
    await app.send_video(
        chat_id=user_id,
        video=response["video"],
        caption=caption,
    )
    await app.delete_message(user_id, answer.output.id)


def pintrest(url):
   
   data = {
     "url" : url,
   }
   
   headers = {
      "authority": "pinterestvideodownloader.com",
      "content-type": "application/x-www-form-urlencoded",
    }
  
   response = requests.post("https://pinterestvideodownloader.com/download.php", headers=headers, data=data).text
   result = re.findall(r'<video src="(.*?)"', response)
   match = re.search(r"(.*?)pin(.*?)", url)
   
   if match:
      return {"url": result[0], "success" : True}
   # @ELHYBA & @Source_Ze
   return {"success" : False}


@app.callback_query_handler(
    func= lambda callback: callback.data == "pintrest")
async def pin_vid(callback: CallbackQuery):
    user_id = callback.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await listener.listen_to(m=callback , text=caption)
    await app.delete_message(user_id, answer.id)
    await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="Processing...")
    url = answer.text
    response = pintrest(url)
    if not response["success"]:
        await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="الرابط غير صالح")
        return # @ELHYBA & @Source_Ze
    bot = await app.get_me ()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● Uploaded By : [{bot_name}]({bot_url})"
    await app.send_video(
        chat_id=user_id,
        video=response["url"],
        caption=caption,
    )
    await app.delete_message(user_id, answer.output.id)


def snapchat(url):
	
	web = "https://www.expertstool.com/converter.php"
	payload = { 
	  "url" : url
	   }
	source = requests.post(web,data=payload).content
	soup = BeautifulSoup(source,"html.parser")
	
	link = soup.find_all("a", {"class" : "btn-primary"})[1]["href"]
	
	if len(link) > 300 or len(link) < 100:
		return {"success": False}
	
	return { "url" : link , "success": True}
# @ELHYBA & @Source_Ze

@app.callback_query_handler(
    func= lambda callback: callback.data == "snapchat")
async def snap_vid(callback: CallbackQuery):
    user_id = callback.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await listener.listen_to(m=callback , text=caption)
    await app.delete_message(user_id, answer.id)
    await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="Processing...")
    url = answer.text
    response = snapchat(url)
    if not response["success"]:
        await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="الرابط غير صالح")
        return # @ELHYBA & @Source_Ze
    bot = await app.get_me ()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● Uploaded By : [{bot_name}]({bot_url})"
    await app.send_video(
        chat_id=user_id,
        video=response["url"],
        caption=caption,
    )
    await app.delete_message(user_id, answer.output.id)# @ELHYBA & @Source_Ze
    

# @ELHYBA & @Source_Ze
def tiktok(url):
    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',# @ELHYBA & @Source_Ze
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
    }
    
    data = {
    	'id': url,
    	'locale': 'en',
    	'tt': 'VG5CYm1h',
	}
  
    response = requests.post('https://ssstik.io/abc', headers=headers, data=data).text
    try:
        title = response.split('"maintext">', 1)[1].split("<", 1)[0]
    except IndexError:
        return { "success" : False }
    urls = response.split('<div class="flex-1 result_overlay_buttons pure-u-1 pure-u-sm-1-2">')[1]
    a_voice = urls.split('<a href="')[2]
    voice = a_voice.split('"')[0]
    a_video = urls.split('<a href="')[1]
    video = a_video.split('"')[0]
    result = {"mp4" : video, "mp3" : voice, "title" : title, "id" : url.rsplit("/", 1)[0], "success": True}
    
    return result
     
  
@app.callback_query_handler(
    func= lambda callback: callback.data == "tiktok")
async def tik_vid(callback: CallbackQuery):
    user_id = callback.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await listener.listen_to(m=callback , text=caption)
    await app.delete_message(user_id, answer.id)
    await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="Processing...")
    url = answer.text
    response = tiktok(url)
    if not response["success"]:
        await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="الرابط غير صالح")
        return # @ELHYBA & @Source_Ze
    urllib.request.urlretrieve(response["mp4"], f"{response['title']}.mp4")
    bot = await app.get_me ()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    markup = Keyboard([
        [
            Button("- تحميل الصوت-", callback_data=f"tiktokaudio_{response['id']}")
        ]
    ])
    caption = f"title : {response['title']}\n\n● Uploaded By : [{bot_name}]({bot_url})"
    await app.send_video(
        chat_id=user_id,
        video=File(f"{response['title']}.mp4"),
        caption=caption,
        reply_markup=markup
    )
    await app.delete_message(user_id, answer.output.id)
    os.remove(f"{response['title']}.mp4")
    

@app.callback_query_handler(
    func= lambda callback: callback.data.startswith("tiktokaudio_"))
async def tik_aud(callback: CallbackQuery):
    user_id = callback.from_user.id
    vid_id = callback.data.split("_")[1]
    response = tiktok(f"https://vm.tiktok.com/{vid_id}/")
    urllib.request.urlretrieve(response["mp3"], f"{response['title']}.mp3")
    bot = await app.get_me ()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● Uploaded By : [{bot_name}]({bot_url})"
    await app.send_audio(
        chat_id=user_id,
        audio=File(f"{response['title']}.mp3"),
        caption=caption,
    )# @ELHYBA & @Source_Ze
    os.remove(f"{response['title']}.mp3")
    

def youtube(url):
    yt = YouTube(url)
    streams = yt.streams
    info = yt.vid_info
    return streams, info["videoDetails"] # @ELHYBA & @Source_Ze
    

def streams_keys(streams, v_id):
    markup = []
    
    for stream in streams:
        if stream.type.startswith(('video', 'audio')):
            res = "🎵" if stream.type.startswith("audio") else stream.resolution
            extension = stream.mime_type.split('/')[-1]
            size = "{:.2f}".format(float(stream.filesize_mb))
            text = f'{res}, {extension}, {size}MB'
            data = f'download {v_id} {stream.itag}'
            markup.append([Button(text, callback_data=data)])
    return markup


@app.callback_query_handler(
    func= lambda callback: callback.data == "youtube")
async def quality(callback: CallbackQuery):
    user_id = callback.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await listener.listen_to(m=callback , text=caption)
    await app.delete_message(user_id, answer.id)
    await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="Processing...")
    url = answer.text
    try:
        response = youtube(url)
    except pytube.exceptions.RegexMatchError:
        await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="الرابط غير صالح")
        return # @ELHYBA & @Source_Ze
    streams = response[0]
    info = response[1]
    markup = Keyboard(streams_keys(streams, info["videoId"]))
    await app.edit_message_text(
        chat_id=user_id,
        message_id=answer.output.id,
        text="● اختر الجوده المناسبه: ",
        reply_markup=markup
    )
    

@app.callback_query_handler(
    func= lambda callback: callback.data.startswith("download"))
async def download(callback: CallbackQuery):
    data = callback.data.split()
    response = youtube(f"https://www.youtube.com/watch?v={data[1]}")
    yt = response[0]
    stream = yt.get_by_itag(data[2])
    if not stream:
        await app.answer_callback_query("INVALID OR TIMEOUT",  show_alert=True)
        return
    bot = await app.get_me()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    info = response[1]
    title = info["title"]
    length = info["lengthSeconds"]
    views = info["viewCount"]
    thumbnail = info["thumbnail"]["thumbnails"][-1]["url"] # @ELHYBA & @Source_Ze
    caption = f"● Title: {title} \n\n● Duration: {length}sec\n\n● Views: {views}\n\n● Uploaded By : [{bot_name}]({bot_url})"
    if stream.type.startswith(('video', "audio")) and stream.filesize_mb > 100:
        text = "- Content Size Is More Than 50MB. I Can't Upload it to Telegram\n\n" + caption
        markup = Keyboard([
            [
                Button("- Download -", url=stream.url),
                Button("- thumbnail -", url=thumbnail)
            ]
        ])
        await app.edit_message_text(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.id, 
            text=text, 
            reply_markup=markup
        )
        return
    await app.edit_message_text(chat_id = callback.message.chat.id, message_id=callback.message.id, text="Downloading...")
    stream.download()
    await app.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Uploading...")
    await app.send_video(
         chat_id = callback.message.chat.id, 
         video=File(stream.default_filename),
         caption=caption,# @ELHYBA & @Source_Ze
    )
    await app.delete_message(callback.message.chat.id , callback.message.id)
    os.remove(stream.default_filename)


def soundcloud(url):
  params = {
    "url": url
    } 
  response = requests.post("https://api.downloadsound.cloud/track", json=params).json()
  
  mp3 = response['url']
  title = response['title']
  user = response["author"]["username"]
  likes = response["author"]["likes_count"]
  
  return {
    "mp3" : mp3,
    "title" : title,
    "likes" : likes, # @ELHYBA & @Source_Ze
    "username" : user,
  }

@app.callback_query_handler(
    func= lambda callback: callback.data == "soundcloud")
async def sound(callback: CallbackQuery):
    user_id = callback.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await listener.listen_to(m=callback , text=caption)
    await app.delete_message(user_id, answer.id)
    await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="Processing...")
    url = answer.text
    try:
        response = soundcloud(url)
    except KeyError:
        await app.edit_message_text(chat_id=user_id,message_id=answer.output.id ,text="الرابط غير صالح")
        return # @ELHYBA & @Source_Ze
    bot = await app.get_me()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● title : {response['title']}\n● Likes : {response['likes']}\n\n● Uploaded By : [{bot_name}]({bot_url})"
    await app.send_audio(
        chat_id=user_id,
        audio=response["mp3"],
        caption=caption,
    )
    await app.delete_message(user_id, answer.output.id) # @ELHYBA & @Source_Ze
    

@app.message_handler(
    func= lambda message: others["options"]["forward_from_users"] and message.from_user.id not in admins,
    chat_types=["private"],
    content_types=["text", "audio", "voice", "video", "document", "photo"])
async def forward_from_users(message: Message):
    for adminn in admins:
        try:
            await app.forward_message(
                adminn,
                from_chat_id = message.from_user.id,
                message_id = message.id # @ELHYBA & @Source_Ze
            )
        except:
            continue
    await app.reply_to(
        message,
        "-> تم إرسال رسالتك للمطور!"
    )

def keyboard():
    keys = [
    [
        Button(# @ELHYBA & @Source_Ze
            "- التوجيه من الأعضاء ✅️ -" if others.get("options")["forward_from_users"] else "- التوجيه من الأعضاء ❌️ -",
             callback_data="forward_from_users"), # DONE
        Button(
            "- تنبيه الأعضاء الجدد ✅️ -" if others.get("options")["new_members_notice"] else "- تنبيه الأعضاء الجدد ❌️ -", 
            callback_data="new_members_notice") # DONE
    ],
    [
        Button("- إضافة قناه -", callback_data="add_channel"), # DONE
        Button("- القنوات الحاليه -", callback_data="current_channels"), # DONE
        Button("- حذف قناه -", callback_data="remove_channel") # DONE
    ],
    [
        Button("- التخزين -", callback_data="send_storage") # DONE
    ]
    ]
    return keys    

async def main():
    print((await app.get_me()).full_name)
    await app.infinity_polling()
# @ELHYBA & @Source_Ze
if __name__ == "__main__":
    loop.run_until_complete(main())