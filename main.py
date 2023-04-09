import os 
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
import openai
from utils import get_image


load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key = OPENAI_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hola, soy el OisTiBot. Como estás?')


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    prompt = ' '.join(args)
    res = openai.Image.create(
        prompt=prompt,
        n=1,
        size='256x256'
    )
    image_url = res['data'][0]['url']
    img = get_image(image_url)
    img.save('./img/tmp.png')
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo='./img/tmp.png')
    os.remove('./img/tmp.png')


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_KEY).build()
    start_handler = CommandHandler('start', start)
    image_handler = CommandHandler('image', image)
    app.add_handlers([start_handler, image_handler])
    app.run_polling()
