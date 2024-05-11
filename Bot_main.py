import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Pytube_main import get_started, download_main
from Pytube_main import PATH

TOKEN = "7154888656:AAFMHu-3ImBYGhybMWw5nsH1ry7B8L9GIwg"
bot = telebot.TeleBot(TOKEN)
main_dict = {}
message_to_del = {}
message_to_del_answer = {}

#PATH = "C:/Python project/Youtube/Videos/"


def send(name_of_file, user_id, key):
    print(name_of_file, "fdfdf")
    flag = name_of_file.split(".")[-1]
    print("Начал отрпавлять")
    path = PATH + name_of_file
    print(flag)
    mes_to_del = message_to_del_answer[user_id]
    bot.delete_message(mes_to_del.chat.id, mes_to_del.message_id)
    del message_to_del_answer[user_id]
    if flag == "mp4":
        print("mp4")
        try:
            bot.send_video(user_id, video=open(path, 'rb'))
        except Exception as error:
            if "Error code: 413" in str(error):
                bot.send_message(user_id, "Файл слишком большой. Попробуйте уменьшить качество")
            print("ERROR", error)
    elif flag == "mp3":
        try:
            bot.send_audio(user_id, audio=open(path, 'rb'))
        except Exception as error:
            if "Error code: 413" in str(error):
                bot.send_message(user_id, "Файл слишком большой. Попробуйте уменьшить качество")
            print("ERROR", error)
    del main_dict[key]

def markup(url):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    best_quality_callback = f"f.1:{url}"
    normal_quality_callback = f"f.2:{url}"
    audio_call_back = f"f.3:{url}"
    markup.add(InlineKeyboardButton("Лучшее качество", callback_data=best_quality_callback),
               InlineKeyboardButton("Нормальное качество", callback_data=normal_quality_callback),
               InlineKeyboardButton("Аудио", callback_data=audio_call_back))
    return markup


@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}. Отправь мне ссылку на youtube ролик и я его скачаю!")

@bot.message_handler(content_types=["text"])
def check_txt(message):
    message_txt = message.text
    if message_txt.startswith("h"):
        message_txt = message_txt.replace(" ", "")
        yt_object = get_started(message_txt)
        if not yt_object:
            bot.reply_to(message, "Видео недоступно(")
        else:
            message_txt = message_txt.replace("//", "/")
            main_dict[message_txt.split("/")[2]] = yt_object
            mes = bot.send_message(message.chat.id, f"Выберите формат для скачивания видео:",
                             reply_markup=markup(message_txt))
            message_to_del[message.from_user.id] = mes
    else:
        bot.reply_to(message, "Ссылка не корректна! Попробуйте ещё раз.")

@bot.callback_query_handler(func=lambda call:call.data.startswith('f.'))
def callback_query(call):
    call_data = call.data
    call_data = call_data.split(":")
    a = call_data[2]
    a = a.split("/")
    print("kjfskf",message_to_del)
    mes = message_to_del[call.from_user.id]
    bot.delete_message(mes.chat.id, mes.message_id)
    del message_to_del[call.from_user.id]
    if call_data[0] == "f.1":
        print(main_dict)
        mes1 = bot.send_message(call.from_user.id, "Скачиваю Ваше видео в наилучшем качестве!")
        message_to_del_answer[call.from_user.id] = mes1
        name = download_main(call_data[1], call.from_user.id, 1, main_dict[a[2]])
        send(name, call.from_user.id, a[2])
    elif call_data[0] == "f.2":
        print("A", a)
        print("main", main_dict)
        mes2 = bot.send_message(call.from_user.id, "Скачиваю Ваше видео в нормальном качестве!")
        message_to_del_answer[call.from_user.id] = mes2
        name = download_main(call_data[1], call.from_user.id, 2, main_dict[a[2]])
        if name == False:
            bot.send_message(call.from_user.id, "Ошибка в скачивании видео, попробуйте другой формат.")
        send(name, call.from_user.id, a[2])
    elif call_data[0] == "f.3":
        mes3 = bot.send_message(call.from_user.id, "Скачиваю Ваше видео как аудио!")
        message_to_del_answer[call.from_user.id] = mes3
        name = download_main(call_data[1], call.from_user.id, 3, main_dict[a[2]])
        send(name, call.from_user.id, a[2])

bot.infinity_polling()