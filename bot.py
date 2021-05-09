import logging, random
from telegram import InlineKeyboardButton,InlineKeyboardMarkup, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import  CallbackQueryHandler
from secrets import token_urlsafe
from flask import session
import const, models
import requests

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start(update, context):
   # keyboard=[ InlineKeyboardButton(text="Schedular Intro",callback_data=1),
   # InlineKeyboardButton(text="get otp",callback_data=2)
    keyboard=[]
    keyboard.append([InlineKeyboardButton(text="About Schedular",callback_data="intro")])
    keyboard.append([InlineKeyboardButton(text="get otp",callback_data="get_otp")])
    keyboard.append([InlineKeyboardButton(text="add new group",callback_data="add_new_grp")])
    reply_markup=InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Welcome to auto-schedular. What would you like to do!",reply_markup=reply_markup)

def query_handler(update, context):
    query=update.callback_query
    if(query.data == "intro"):
        context.bot.send_message(chat_id=update.effective_chat.id,text="Auto Schedular is a python based project that provides an interface through which a user can post a message on multiple social media platforms on single click!")
    if(query.data == "get_otp"):
        tg_user=context.bot.username
#        tg_user_otp = str(token_urlsafe())
        if not tg_user:
            context.bot.send_message(chat_id=update.effective_chat.id,text="Please set your telegram username to login")
        else:    
            session = models.Session()
            try:
                otp = models.User.insert_record_in_user(session,tg_user)
                context.bot.send_message(chat_id=update.effective_chat.id,text="OTP "+str(otp)+"   generated for  "+tg_user)
            finally:
                session.close()
    if(query.data == "add_new_grp"):
        #    print(update.effective_message.chat)
        
        r = requests.get('https://api.telegram.org/bot'+const.tg_token+'/getUpdates')
        #r = r.json()
        """
        if not r['result']:
            context.bot.send_message(chat_id=update.effective_chat.id,text="Please add bot to the Group")
        else:
        """
        print(r['result'][0]['message']['chat']['id'])
        group_id = str(r['result'][0]['message']['chat']['id'])
        group_name = r['result'][0]['message']['chat']['title']
        send_message_url = 'https://api.telegram.org/bot'+const.tg_token+'/sendMessage'
        data ={
        'chat_id':group_id,
        'text':'Hi I am schedular bot. I can help you to publish your post on multiple platforms with a single click!'
        }
        requests.post(send_message_url,data=data)

        session = models.Session()
        try:
            tg_user_id = session.query(models.User.id).filter(models.User.tg_username==context.bot.username).all()
            u_id = tg_user_id[0][0]
            models.Group.add_group(session,group_id, group_name)
            models.Link.insert_record(session,u_id,group_id)
            context.bot.send_message(chat_id=update.effective_chat.id,text="Group added successfully")
        finally:
            session.close()

def run():
    token = const.tg_token    #Token generated while creating telegram bot. 
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start",start))
    updater.dispatcher.add_handler(CallbackQueryHandler(query_handler,pass_user_data=True, pass_chat_data=True))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    run()