import os
from search import make_message
import telebot
import time
from json import loads
#from telegram import Bot, InputMediaPhoto

f = open("token.txt", "r")
BOT_TOKEN = f.read()
f.close()
f = open("settlementsCodes.txt", "r")
codes = loads(f.read())
f.close()
print(codes)

bot = telebot.TeleBot(BOT_TOKEN)

def send_media_group_with_urls(chat_id, photo_urls, text, video_urls = None):
    media_group = [telebot.types.InputMediaPhoto(media=url) for url in photo_urls]
    media_group_with_video = media_group
    if video_urls:
        for url in video_urls:
            #print("url = " + str(telebot.types.InputMediaVideo(media=url)))
            media_group.append(telebot.types.InputMediaVideo(media=url)) 
    #print(media_group)
    #print(len(media_group))
    #try:
    if len(media_group) > 10:
        bot.send_media_group(chat_id, media=media_group[:9])
        bot.send_media_group(chat_id, media=media_group[9:-1])
    else:
        bot.send_media_group(chat_id, media=media_group)
    #except:
    #    if len(media_group) > 10:
    #        bot.send_media_group(chat_id, media=media_group[:9])
    #        bot.send_media_group(chat_id, media=media_group[9:-1])
    #    else:
    #        bot.send_media_group(chat_id, media=media_group)
    bot.send_message(chat_id, text)



@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    #chat_id = message.chat.id

@bot.message_handler(commands=["photo", "image"])
def send_photo(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "מחפש דירות")
    msg = make_message()
    for i in msg:
        photo_urls = msg[i]["photos"]
        video_urls = msg[i]["videos"]
        #print(photo_urls)
        #print(video_urls)
        text = msg[i]["desc"]

    

    # Send the photos as a media group with text to the chat
        try:
            send_media_group_with_urls(chat_id, photo_urls, text, video_urls)
        except:
            print('sent without video')
            send_media_group_with_urls(chat_id, photo_urls, text)
        time.sleep(2)
    apartments_sent = len(msg.keys())
    finished_message = "נשלחו %s דירות" %(apartments_sent)
    bot.send_message(chat_id, finished_message)
   


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    chat_id = message.chat.id
    call = message.chat
    # List of photo URLs to send
    stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}

    markup = telebot.types.InlineKeyboardMarkup()
    i =0
    for key, value in codes.items():
        i +=1
        print(type(key), type(value))
        markup.add(telebot.types.InlineKeyboardButton(text=key, callback_data=value))
        if i>4: break
    bot.send_message(chat_id, text='choose', reply_markup=markup)
    #print(message)
    """if (call.data.startswith("['value'")):
        print('inside')
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=chat_id, show_alert=True,
                                text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)
    """

@bot.callback_query_handler(func=lambda call:True)
def answer(callback):
    
    print(callback.data)


bot.infinity_polling()