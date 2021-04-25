import logging, random
from telegram import InlineKeyboardButton,InlineKeyboardMarkup, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import  CallbackQueryHandler
from secrets import token_urlsafe
from flask import session

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def generate_authcode():
    code=random.randint(100000,999999)
    return code

def start(update, context):
   # keyboard=[ InlineKeyboardButton(text="Schedular Intro",callback_data=1),
   # InlineKeyboardButton(text="get otp",callback_data=2)
    keyboard=[]
    keyboard.append([InlineKeyboardButton(text="About Schedular",callback_data="intro")])
    keyboard.append([InlineKeyboardButton(text="get otp",callback_data="get_otp")])
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
            import models
            session = models.Session()
            try:
                otp = models.Otp.insert_record_in_otp(session,tg_user)
                context.bot.send_message(chat_id=update.effective_chat.id,text="OTP "+str(otp)+"   generated for  "+tg_user)
            finally:
                session.close()

def run():
    token='1779556887:AAGML8Sgy6DDBl6MW2FKO0Flz9KOGaPfkUA'    #Token generated while creating telegram bot. 
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start",start))
    updater.dispatcher.add_handler(CommandHandler("authcode",generate_authcode))
    updater.dispatcher.add_handler(CallbackQueryHandler(query_handler,pass_user_data=True, pass_chat_data=True))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    run()