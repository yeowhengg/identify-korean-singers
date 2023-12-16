import os
from dotenv import load_dotenv
from telebot import TeleBot
import requests
import json

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')
print(API_URL)

bot = TeleBot(BOT_TOKEN)


def send_image(local_file_path) -> requests.Response:

    url = f'{API_URL}uploadfiles/'
    file_path = f"https://api.telegram.org/file/bot{BOT_TOKEN}/photos/{local_file_path}"
    get_image_res = requests.get(file_path)
    read_files = {"files": (local_file_path, get_image_res.content)}
    response = requests.post(url, files=read_files)

    return response


def get_details(path):
    url = f'{API_URL}getidoldetails/{path}'
    response = requests.get(url)

    return response


@bot.message_handler(content_types=['photo', 'text'])
def handle_photo(message):
    if message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path.replace("photos/", "")

        if file_path.endswith(".jpg"):
            photo_id_tag = message.id

            print(f"sending image to server... {file_path}")
            status = send_image(file_path)
            if status.status_code == 200:
                get_path = json.loads(
                    status.content.decode("utf-8"))['path'][0]

                details_status = get_details(
                    str(get_path).replace("/images", ""))

                if details_status.status_code == 200:
                    content = json.loads(details_status.content)[
                        "idol_details"]["idol_1"]
                    format_data = f"Name: {content['name']}\nAge: {content['age']}\nDoB: {content['dob']}\nGroup: {content['group']}\nSummary: {content['summary']}"

                    bot.send_message(message.chat.id, format_data,
                                     reply_to_message_id=photo_id_tag)

            else:
                bot.send_message(message.chat.id,
                                 "something went wrong.. please try again later..")

                print(status.raise_for_status())

        else:
            bot.send_message(message.chat.id, "Please send a JPG file.")

    else:
        bot.send_message(
            message.chat.id, "Please send a valid photo that is in the JPG format")


@bot.message_handler(commands=['start', 'help'])
def message_handler(message):
    bot.send_message(
        message.chat.id, "Upload image(s) in .jpg format to continue")


print("bot started")
bot.infinity_polling()
