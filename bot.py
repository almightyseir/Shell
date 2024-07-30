from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from misc import locateimg, fmtjson, fmtresponse
import os
from telegraph import upload_file
from db import adduser, userexists, isbanned, banuser, unbanuser
from datetime import datetime
from functools import wraps
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

#vars
token = "7086797887:AAHDNvTsVw7X0oSNZ2EwDn5mP0SPWvQ7490"
api = 27812175
api_hash = "3b22f834ae7661213a75492abba00b43"
helptext = "**GeoSpy Bot Help**\n\n**Commands**\n\n/start - Start the bot\n/help - Get help\nSend Any Photo - Get location information"
strttxt = "**Hello {}**\n\n**Welcome to GeoSpy Bot**\n\n**Use /help to get help**"
##buttons
startbutton = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Help", callback_data='help'),
            InlineKeyboardButton("About", callback_data='about')
        ]
    ]
)

helpbutton = InlineKeyboardMarkup([[InlineKeyboardButton("🔙Back", callback_data='back')]])
aboutbutton = InlineKeyboardMarkup([[InlineKeyboardButton("🔙Back", callback_data='back')]])
about_message = """
**About This Bot

Welcome to PhotoDetectiveBot, your smart assistant for geolocating photos and identifying their online sources!

What Can PhotoDetectiveBot Do?

- Geolocation: Send us any photo, and we'll use advanced algorithms to determine the location where it was taken. Perfect for travelers, researchers, or anyone curious about the origin of a picture.
- Source Identification: Have a photo you suspect might be fake or want to know more about? Upload any online image, and we'll track down its sources. Great for verifying authenticity, finding original posts, or uncovering more details.

How to Use:

1. Send a Photo: Upload any image from your device or share a URL of an online image.
2. Wait for Analysis: Our bot will process the photo and provide detailed information on its geolocation and potential online sources.
3. Receive Results: Get insights on where the photo was taken and links to its sources if available.

Ideal Use Cases:

- Verify Authenticity: If you suspect a photo might be fake or manipulated, our bot can help you find the original source and verify its authenticity.
- Explore Origins: Curious about where a stunning landscape or unique building in a photo is located? We can pinpoint the geolocation for you.
- Uncover Details: For journalists, researchers, or the simply curious, uncovering the background and sources of an image has never been easier.
- OSINT Investigations: If you're into open-source intelligence (OSINT) and need to dig deeper into the details of a photo, we've got you covered.
- Secret Agent Mode: Feeling like an FBI agent on a mission? Use our bot to track down the origins of a suspicious photo, and satisfy your inner detective!

"""



def ban_check(func):
    @wraps(func)
    def wrapper(client, message):
        if isbanned(message.from_user.id):
            bot.send_message(chat_id=message.chat.id, text="You are banned from using this bot.")
        else:
            return func(client, message)
    return wrapper


bot = Client("GeoSpy", api_id=api, api_hash=api_hash, bot_token=token)

fsubid = "-1002192831527"
def check_subscription(client, userid):
    try:
        user_status = client.get_chat_member(fsubid, userid)
        print(f"User status: {user_status.status}")  # Log the user's status for debugging
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        # Log or print the exception if needed
        print(f"Error checking subscription: {e}")
        return False

# Decorator for checking subscription
def fsub(func):
    @wraps(func)
    def wrapper(client, message):
        userid = message.from_user.id
        if check_subscription(client, userid):
            return func(client, message)
        else:
            message.reply(
                f"Hi {message.from_user.mention}, you are **not subscribed** to our channel. Please join to use this bot.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Channel", url="https://t.me/devautomation")]]
                )
            )
    return wrapper
#handle botquery
@bot.on_callback_query()
async def cb_data(bot,update):
    if update.data == 'help':
        await update.message.edit_text(text=helptext, reply_markup=helpbutton)
    elif update.data == 'about':
        await update.message.edit_text(text=about_message, reply_markup=aboutbutton)
    elif update.data == 'back':
        await update.message.edit_text(text=strttxt.format(update.from_user.first_name), reply_markup=startbutton)
@bot.on_message(filters.command("start"))
@fsub
@ban_check
def start(_, msg):
    user = msg.from_user
    exist = userexists(msg.chat.id)
    if not exist:
        date_of_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        adduser(msg.chat.id,user.first_name,user.dc_id,date_of_start)
        print(f"User added {msg.chat.id}" )
    bot.send_message(chat_id=msg.chat.id, text=strttxt.format(user.first_name), reply_markup=startbutton)

@bot.on_message(filters.command("help"))
@ban_check
def help(_, msg):
    helptext = "**GeoSpy Bot Help**\n\n**Commands**\n\n/start - Start the bot\n/help - Get help\nSend Any Photo - Get location information"
    bot.send_message(chat_id=msg.chat.id, text=helptext)

@bot.on_message(filters.photo)
@fsub
@ban_check
def photo(_, msg):
    processmsg = bot.send_message(chat_id=msg.chat.id, text="Processing...")
    path = f"DL/{msg.chat.id}.jpg"
    bot.download_media(msg, file_name=path)
    response = upload_file(path)
    try:
        os.remove(path)
    except:
        pass
    imgurl = f"https://graph.org/{response[0]}"
    response = locateimg(imgurl)
    newobj = fmtjson(response)
    message = fmtresponse(newobj)
    bot.send_message(chat_id=msg.chat.id, text=message)
    processmsg.delete()


@bot.on_message(filters.command("ban"))
def ban(_, msg):
    userid = msg.text.split()[1]
    banuser(userid)
    bot.send_message(chat_id=msg.chat.id, text=f"User {userid} has been banned.")

@bot.on_message(filters.command("unban"))
def unban(_, msg):
    userid = msg.text.split()[1]
    unbanuser(userid)
    bot.send_message(chat_id=msg.chat.id, text=f"User {userid} has been unbanned.")
    

bot.run()
