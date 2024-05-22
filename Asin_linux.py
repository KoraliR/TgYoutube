from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from Asin_pytube_main_stable import make_yt_object, check_video_availability, check_available_resolutions, download, PATH, my_logger, search_youtube

import logging

pytube_logger = logging.getLogger('pytube')
pytube_logger.setLevel(logging.ERROR)

bot = AsyncTeleBot('7154888656:AAFMHu-3ImBYGhybMWw5nsH1ry7B8L9GIwg')
#main_dictionaries
dict_yt_obj = dict()
dict_messeges_to_del_inline = dict()
dict_messeges_to_del_inline_search = dict()
#
async def manual_download(video_id, caal):
    link_for_download = "https://www.youtube.com/watch?v=" + video_id
    print("download_link", link_for_download)
    yt_object = await make_yt_object(link_for_download)
    print("yt", yt_object)
    if not yt_object:
        pass #видео не сущетсвует
    else:
        flag_availability = check_video_availability(yt_object)
        if flag_availability:
            dict_yt_obj[yt_object.video_id] = yt_object
            available_resolutios = await check_available_resolutions(yt_object)
            inline_keyboard = await markup(available_resolutios, yt_object.video_id)
            await my_logger(caal.from_user.id, caal.from_user.username, yt_object)
            mes = await bot.send_message(caal.from_user.id,
                                         f"🎦 {yt_object.title}\n👤 {yt_object.author}\n🕰 {yt_object.length // 60} минут\nВыберите формат для скачивания видео:",
                                         reply_markup=inline_keyboard)
            dict_messeges_to_del_inline[caal.from_user.id] = mes
        else:
            pass #видео не доступно




async def send(name_of_file, user_id, yt_obj):
    flag_type = name_of_file.split(".")[-1]
    path_to_file = PATH + "\\"+ name_of_file
    title = f"{yt_obj.title}\n#{str(yt_obj.author).replace(' ', '')}"
    if flag_type == "mp4":
        print("mp4")
        try:
            await bot.send_video(user_id, video=open(path_to_file, 'rb'), caption=title)
        except Exception as error:
            if "Error code: 413" in str(error):
                await bot.send_message(user_id, "Файл слишком большой. Попробуйте уменьшить качество")
            print("ERROR", error)
    elif flag_type == "mp3":
        try:
            await bot.send_audio(user_id, audio=open(path_to_file, 'rb'), caption=title)
        except Exception as error:
            if "Error code: 413" in str(error):
                await bot.send_message(user_id, "Файл слишком большой. Попробуйте уменьшить качество")
            print("ERROR", error)


async def make_download_markup(video_id):
    download_markup = InlineKeyboardMarkup()
    call_back_download = "s." + str(video_id)
    download_markup.add(InlineKeyboardButton("Скачать", callback_data=call_back_download))
    return download_markup


async def markup(available_list, video_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    video_360 = f"f.360:{video_id}"
    video_480 = f"f.480:{video_id}"
    video_720 = f"f.720:{video_id}"
    video_10 = f"f.10:{video_id}"
    audio = f"f.a:{video_id}"
    if '360p' in available_list:
        markup.add(InlineKeyboardButton("360p", callback_data=video_360))
    if '480p' in available_list:
        markup.add(InlineKeyboardButton("480p", callback_data=video_480))
    if '720p' in available_list:
        markup.add(InlineKeyboardButton("720p", callback_data=video_720))
    if '1080p' in available_list:
        markup.add(InlineKeyboardButton("1080p", callback_data=video_10))
    markup.add(InlineKeyboardButton("Аудио", callback_data=audio))
    return markup



@bot.message_handler(commands=["start"])
async def hello(message):
    text = f"Привет, {message.from_user.first_name}. Я простой бот для скачивания youtube роликов\nОтправь мне ссылку на видео и я его скачаю"
    await bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=["search"])
async def search(message):
    search_request = message.text
    if search_request.strip() == "/search":
        await bot.send_message(message.from_user.id, "Запрос не может быть пустым.")
        return
    search_request = search_request.split()
    search_request = search_request[1:]
    print(search_request)
    search_request = " ".join(search_request)
    search_results = await search_youtube(search_request)
    if search_results == False:
        await bot.send_message(message.from_user.id, "Поисковой запрос не должен превышать 60 символов.")
    else:
        await bot.send_message(message.from_user.id, f"По запросу {search_request} найдены самые релевантные результаты:")
        dict_messeges_to_del_inline_search[message.from_user.id] = []
        print("search_res_1", search_results)
        for result in search_results:
            video_title = result.title
            video_maker = result.author
            video_len = result.length
            mark_up_for_download_mes = await make_download_markup(result.video_id)
            mes = await bot.send_message(message.from_user.id, f"{video_title}\n{video_maker} \n{video_len}", reply_markup=mark_up_for_download_mes)
            temp_list_from_dict = dict_messeges_to_del_inline_search[message.from_user.id]
            temp_list_from_dict.append(mes)
            dict_messeges_to_del_inline_search[message.from_user.id] = temp_list_from_dict
        await bot.send_message(message.from_user.id, "Поиск завершён.")


@bot.message_handler(commands=["help"])
async def help(message):
    help_str1 = "Отправь мне ссылку на youtube ролик и я его скачаю \n"
    help_str2 = "Я могу скачать видео в любом доступном видео формате и в аудио\n"
    help_str3 = "Можешь воспользоваться командой /search и найти любое видео на youtube"
    help_all_str = help_str1 + help_str2 + help_str3
    await bot.send_message(message.from_user.id, help_all_str)

@bot.message_handler(content_types=["text"])
async def start(message):
    message_text = message.text
    #
    print(message.from_user.id)
    #
    yt_obj = await make_yt_object(message_text)
    if not yt_obj:
        await bot.send_message(message.from_user.id, "Ссылка не корректна!")
    else:
        flag_availability = await check_video_availability(yt_obj)
        if flag_availability:
            dict_yt_obj[yt_obj.video_id] = yt_obj
            available_resolutios = await check_available_resolutions(yt_obj)
            inline_keyboard = await markup(available_resolutios, yt_obj.video_id)
            await my_logger(message.from_user.id, message.from_user.username, yt_obj)
            mes = await bot.send_message(message.chat.id,
                                   f"🎦 {yt_obj.title}\n👤 {yt_obj.author}\n🕰 {yt_obj.length // 60} минут\nВыберите формат для скачивания видео:",
                                   reply_markup=inline_keyboard)
            dict_messeges_to_del_inline[message.from_user.id] = mes
        else:
            await bot.send_message(message.from_user.id, "Видео недоступно")
        print(flag_availability)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('f.'))
async def callback_query(call): #f.360:video_i1d
    print("Caall")
    call_data_list = str(call.data).split(":")
    print(f"Call_data_list {call_data_list}")
    video_id = call_data_list[-1]
    print(f"video_id {video_id}")
    flag_resolution = call_data_list[0]
    print(flag_resolution, "flag_res")
    print(dict_messeges_to_del_inline)
    print(call.message.from_user.id)
    inline_message_to_del = dict_messeges_to_del_inline[call.from_user.id]
    print(inline_message_to_del, "del to")
    print("f")
    await bot.delete_message(inline_message_to_del.chat.id, inline_message_to_del.message_id)
    del dict_messeges_to_del_inline[call.from_user.id]
    yt_obj = dict_yt_obj[video_id]
    del dict_yt_obj[video_id]
    name_of_file = await download(flag_resolution, video_id, call.from_user.id, yt_obj)
    await send(name_of_file, call.from_user.id, yt_obj)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('s.'))
async def search(call):
    print("gggg")
    print("call", call)
    video_id = str(call.data).split(".")[-1]
    messages_to_del = dict_messeges_to_del_inline_search[call.from_user.id]
    print("messages_to_del", dict_messeges_to_del_inline_search)
    for mes in messages_to_del:
        await bot.delete_message(mes.chat.id, mes.message_id)
    await manual_download(video_id, call)

asyncio.run(bot.polling())