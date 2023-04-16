import os 
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai
from utils import get_image


load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')
CHAT = os.getenv('CHAT_ID')

messages = []

openai.api_key = OPENAI_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hola, soy el OisTiBot. Como estás?')


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    prompt = ' '.join(args)
    chat_id = update.effective_chat.id
    if str(chat_id) == CHAT:
        res = openai.Image.create(
            prompt=prompt,
            n=1,
            size='256x256'
        )
        image_url = res['data'][0]['url']
        img = get_image(image_url)
        img.save('./img/tmp.png')
        await context.bot.send_photo(chat_id=chat_id, photo='./img/tmp.png')
        os.remove('./img/tmp.png')
    else:
        await context.bot.send_message(chat_id=chat_id, text='Lo siento, no se ha podido generar la imagen')


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    global messages
    message = update.message.text
    if str(chat_id) == CHAT:
        messages.append({'role': 'user', 'content': message})
        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        chat_res = res['choices'][0]['message']['content']
        messages.append({'role':'assistant', 'content': chat_res})
        await context.bot.send_message(chat_id=chat_id, text=chat_res)
    else:
        await context.bot.send_message(chat_id=chat_id, text=message)

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messages
    messages = []
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Conversación borrada con éxito')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_KEY).build()
    start_handler = CommandHandler('start', start)
    image_handler = CommandHandler('image', image)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
    new_chat_handler = CommandHandler('newchat', new_chat)
    app.add_handlers([start_handler, image_handler, chat_handler, new_chat_handler])
    app.run_polling()
