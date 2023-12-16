import os
from dotenv import load_dotenv
from telebot import TeleBot
import requests

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


bot = TeleBot(BOT_TOKEN)


def send_image(local_file_path):

    url = 'http://127.0.0.1:8000/uploadfiles/'
    file_path = f"https://api.telegram.org/file/bot{BOT_TOKEN}/photos/{local_file_path}"
    get_image_res = requests.get(file_path)
    read_files = {"files": (local_file_path, get_image_res.content)}
    response = requests.post(url, files=read_files)

    return "success" if response.status_code == 200 else "something went wrong..."


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.photo:
        file_id = message.photo[-1].file_id

        if file_id.endswith(".jpg"):
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path.replace("photos/", "")
            bot.send_message(message.chat.id, "Processing image...")
            print(f"sending image to server... {file_id}")
            status = send_image(file_path)

            if status == 200:
                bot.send_message(
                    "placeholder# details over here should be the description of idols. Callback is handled by 127.0.0.1 backend")
        else:
            bot.send_message(message.chat.id, "Please send a JPG file.")

    else:
        bot.send_message(
            message.chat.id, "Please send a valid photo that is in the JPG format")


@bot.message_handler(commands=['start', 'help'])
def message_handler(message):
    bot.send_message(
        message.chat.id, "Upload image(s) in .jpg format to continue")


bot.infinity_polling()
