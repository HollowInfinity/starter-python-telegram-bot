import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from telegram import Update, Bot
from pydantic import BaseModel

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict

app = FastAPI()

# Load variables from .env file if present
load_dotenv()

# Read the variable from the environment (or .env file)
bot_token = os.getenv('Fuxxx')

from itertools import count
import logging
import os
import databass as db
from telegram import InputMediaAudio, Update,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler,MessageHandler,filters,ConversationHandler)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
words = ["打扮(dǎban)-переодеваться, наряжаться","打扰(dǎrǎo)-беспокоить, тревожить",
             "打招呼(dǎ zhāohu)-приветствовать, предупреждать","打针(dǎzhēn)-делать укол","打折(dǎzhé)-делать скидку",
             "注意(zhùyì)-обращать внимание","主意(zhǔyi)-идея, мысль","特意(tèyì)-намеренно, специально",
             "随意(suíyì)-по желанию, по усмотрению","得意(déyì)-удачный, удачливый"]
left = InlineKeyboardButton(text="⬅",callback_data="left_button")
right = InlineKeyboardButton(text="➡",callback_data="right_button")
keyboard = InlineKeyboardMarkup([[left,right]])

async def start_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    startMessage = f"""
🤖Прив,{update.effective_user.first_name}!С вами говорит mvp-бот FUXI🤖\n
🔥Мы только запустились,но уже кое-что умеем🔥\n
Благодаря нам ты сможешь изучать китайский с удобством,да еще и на практике подкрепишь знания😸😺\n
Пользуйся командами из выпадающего меню слева от ввода сообщения,или тыкай по ним прямо из этого сообщения:\n
/about - 💡кто мы такие и что делаем💡\n
/remember - 📝запомним новые слова📝\n 
/pass3\n
/start - 😼вызывай это сообщение сколько угодно,我很乐意跟你赌😼"""
    await update.message.reply_text(startMessage)


async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    aboutMessage = f"""
🙂Тебе интересно узнать больше об этом боте?Круто🙃\n
На самом деле данный Telegram-бот всего лишь MVP,демоверсия если угодно,нашего словаря FUXI!\n
Что же это?\n
FUXI - мобильное приложение,которое ответит на отсутствие хороших словарей для изучающих китайский язык людей\n
Большой объем слов с профессиональным переводом и множеством значений,указания контекста,примеры употребления с озвучкой и тренировочный режим\n
Зачем хранить на телефоне несколько приложений,когда есть FUXI?\n
Оставляй обратную связь!Любые вопросы и предложения сюда @HollowInfinity\n"""
    await update.message.reply_text(aboutMessage)

async def remember_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global count_for_button
    count_for_button = 0
    message = "Ну что,начинаем учить?"
   #with open(r"D:\voices\1 word.ogg","rb") as voice:
   #    data = voice.read()
    audio_id = db.audio_1
    await update.message.reply_text(message)
    #await update.message.reply_text(words[0],reply_markup=keyboard)
    await update.message.reply_audio(audio=audio_id,caption=words[0],reply_markup=keyboard) 

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global count_for_button
    query = update.callback_query
    if query.data == "left_button" and count_for_button != 0:
            count_for_button-=1
    if query.data == "right_button" and count_for_button != 9:
            count_for_button+=1
    message = f"""
{words[count_for_button]}\n
"""
    try:
        #await query.edit_message_text(text=f"{message}",reply_markup=keyboard)
        await query.edit_message_caption(caption=f"{message}",reply_markup=keyboard)
        await query.edit_message_media(media=InputMediaAudio(media=db.pack_1[count_for_button] ,caption=f"{message}"))
        await query.edit_message_reply_markup(reply_markup=keyboard)
    except:
        await query.answer()

async def human_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message =  "Мы пока плохо говорим на человеческом,используй команды" 
    await update.message.reply_text(message)
    
async def file_dealer(update: Update, context: ContextTypes.DEFAULT_TYPE):
      await update.message.reply_text(update.message.audio.file_id)
    

def main() -> None:
    app = ApplicationBuilder().token(os.environ["Fuxxx"]).build()

    app.add_handler(CommandHandler(["start","help"], start_message))
    app.add_handler(CommandHandler("about", about_us))
    #app.add_handler(CommandHandler())
    app.add_handler(CommandHandler("remember", remember_command))
    app.add_handler(MessageHandler(filters.AUDIO,file_dealer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,human_answer))
    app.add_handler(CallbackQueryHandler(button))   
    app.run_polling(drop_pending_updates=True)
    
if __name__ == '__main__':
    main()
