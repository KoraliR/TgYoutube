from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from Asin_pytube_main import make_yt_object, check_video_availability, check_available_resolutions, download, PATH, my_logger, search_youtube
from Asin_pytube_main import availbale_formats_information, make_users, another_available_resolutions
import logging
from Asin_pytube_main import another_download, get_weight, get_another_weight

ADMIN_ID = 1310436261

#USERS = get_users()
#USERS = set()

#print(USERS)

pytube_logger = logging.getLogger('pytube')
pytube_logger.setLevel(logging.ERROR)

bot = AsyncTeleBot('')
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
        await bot.send_message(caal.from_user.id, "Видео не доступно(")
        return
    else:
        flag_availability = await check_video_availability(yt_object)
        if flag_availability:
            dict_yt_obj[yt_object.video_id] = yt_object
            available_resolutios = await check_available_resolutions(yt_object)
            #
            another_res = await another_available_resolutions(yt_object, available_resolutios)
            # проверка веса
            weight_casual = await get_weight(yt_object, available_resolutios)
            weight_another = await get_another_weight(yt_object, another_res)

            # конец проверки веса
            title_about_video, OK_res = await availbale_formats_information(yt_object, available_resolutios, another_res, weight_casual, weight_another)
            #
            inline_keyboard = await markup(available_resolutios, yt_object.video_id, another_res, OK_res)
            await my_logger(caal.from_user.id, caal.from_user.username, yt_object, True)
            mes = await bot.send_message(caal.from_user.id,
                                         f"🎦 {yt_object.title}\n👤 {yt_object.author}\n🕰 {yt_object.length // 60} минут\n{title_about_video}\nВыберите формат для скачивания видео:",
                                         reply_markup=inline_keyboard)
            dict_messeges_to_del_inline[caal.from_user.id] = mes
        else:
            await bot.send_message(caal.from_user.id, "Видео не доступно(")
            return




async def send(name_of_file, user_id, yt_obj):
    flag_type = name_of_file.split(".")[-1]
    path_to_file = PATH + "/"+ name_of_file
    title = f"{yt_obj.title}\n#{str(yt_obj.author).replace(' ', '')}\n\n@skachattbot"
    print("INFO", name_of_file, user_id, yt_obj, "STOPINFO", sep="\n")
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


async def markup(available_list, video_id, another_res, OK_res):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    video_144 = f"f.144:{video_id}"
    video_240 = f"f.240:{video_id}"
    video_360 = f"f.360:{video_id}"
    video_480 = f"f.480:{video_id}"
    video_720 = f"f.720:{video_id}"
    video_10 = f"f.10:{video_id}"
    video_144a = f"a.144:{video_id}"
    video_240a = f"a.240:{video_id}"
    video_360a = f"a.360:{video_id}"
    video_480a = f"a.480:{video_id}"
    video_720a = f"a.720:{video_id}"
    video_10a = f"a.10:{video_id}"
    audio = f"f.a:{video_id}"
    if '144p' in available_list and "144p" in OK_res:
        markup.add(InlineKeyboardButton("144p", callback_data=video_144))
    elif '144p' in another_res and "144p" in OK_res:
        markup.add(InlineKeyboardButton("144p", callback_data=video_144a))
    if '240p' in available_list and "240p" in OK_res:
        markup.add(InlineKeyboardButton("360p", callback_data=video_240))
    elif '240p' in another_res and "240p" in OK_res:
        markup.add(InlineKeyboardButton("240p", callback_data=video_240a))
    if '360p' in available_list and "360p" in OK_res:
        markup.add(InlineKeyboardButton("360p", callback_data=video_360))
    elif '360p' in another_res and "360p" in OK_res:
        markup.add(InlineKeyboardButton("360p", callback_data=video_360a))
    if '480p' in available_list and "480p" in OK_res:
        markup.add(InlineKeyboardButton("480p", callback_data=video_480))
    elif '480p' in another_res and "480p" in OK_res:
        markup.add(InlineKeyboardButton("480p", callback_data=video_480a))
    if '720p' in available_list and "720p" in OK_res:
        markup.add(InlineKeyboardButton("720p", callback_data=video_720))
    elif '720p' in another_res and "720p" in OK_res:
        markup.add(InlineKeyboardButton("720p", callback_data=video_720a))
    if '1080p' in available_list and "1080p" in OK_res:
        markup.add(InlineKeyboardButton("1080p", callback_data=video_10))
    elif '1080p' in another_res and "1080p" in OK_res:
        markup.add(InlineKeyboardButton("1080p", callback_data=video_10a))
    markup.add(InlineKeyboardButton("Аудио", callback_data=audio))
    markup.add(InlineKeyboardButton("Не надо!", callback_data="f.del"))
    return markup

def make_inline_dell_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Удалить результаты", callback_data="s.dell"))
    return markup

@bot.message_handler(commands=["start"])
async def hello(message):
    # global USERS
    # user_id = message.from_user.id
    # if user_id in USERS:
    #     pass
    # else:
    #     await make_users(user_id)
    #     USERS = get_users()
    text = f"Привет, {message.from_user.first_name}. Я простой бот для скачивания youtube роликов\nОтправь мне ссылку на видео и я его скачаю"
    await bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=["search"])
async def search(message):
    # global USERS
    # user_id = message.from_user.id
    # if user_id in USERS:
    #     pass
    # else:
    #     await make_users(user_id)
    #     USERS = get_users()
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
        mes3 = await bot.send_message(message.from_user.id, f"По запросу: {search_request} -  найдены самые релевантные результаты:")
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
        mes2 = await bot.send_message(message.from_user.id, "Поиск завершён.", reply_markup=make_inline_dell_keyboard())
        temp_list_from_dict.append(mes2)
        temp_list_from_dict.append(mes3)
        dict_messeges_to_del_inline_search[message.from_user.id] = temp_list_from_dict



@bot.message_handler(commands=["help"])
async def help(message):
    # global USERS
    # user_id = message.from_user.id
    # if user_id in USERS:
    #     pass
    # else:
    #     await make_users(user_id)
    #     USERS = get_users()
    help_str1 = "Отправь мне ссылку на youtube ролик и я его скачаю \n"
    help_str2 = "Я могу скачать видео в любом доступном видео формате и в аудио\n"
    help_str3 = "Можешь воспользоваться командой /search и найти любое видео на youtube"
    help_all_str = help_str1 + help_str2 + help_str3
    await bot.send_message(message.from_user.id, help_all_str)


@bot.message_handler(commands=["set"])
async def set(message):
    if message.from_user.id == ADMIN_ID:
        #for user in USERS:
            #bot.forward_message(user, message.chat.id, message.id, protect_content=True)
        pass
    else:
        await bot.send_message(message.from_user.id, "Попробуйте /help")






@bot.message_handler(content_types=["text"])
async def start(message):
    # global USERS
    # user_id = message.from_user.id
    # if user_id in USERS:
    #     pass
    # else:
    #     await make_users(user_id)
    #     USERS = get_users()
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
            #
            another_res = await another_available_resolutions(yt_obj, available_resolutios)
            #
            # проверка веса
            weight_casual = await get_weight(yt_obj, available_resolutios)
            weight_another = await get_another_weight(yt_obj, another_res)

            # конец проверки веса
            title_about_video, OK_res = await availbale_formats_information(yt_obj, available_resolutios,
                                                                            another_res, weight_casual, weight_another)
            #
            inline_keyboard = await markup(available_resolutios, yt_obj.video_id, another_res, OK_res)
            await my_logger(message.from_user.id, message.from_user.username, yt_obj, False)
            #
            #title_about_video = await availbale_formats_information(yt_obj, available_resolutios, another_res)
            #
            #inline_keyboard = await markup(available_resolutios, yt_obj.video_id, another_res)
            #await my_logger(message.from_user.id, message.from_user.username, yt_obj)
            mes = await bot.send_message(message.chat.id,
                                   f"🎦 {yt_obj.title}\n👤 {yt_obj.author}\n🕰 {yt_obj.length // 60} минут\n{title_about_video}\nВыберите формат для скачивания видео:",
                                   reply_markup=inline_keyboard)
            dict_messeges_to_del_inline[message.from_user.id] = mes
        else:
            await bot.send_message(message.from_user.id, "Видео недоступно")
        print(flag_availability)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('f.'))
async def callback_query(call): #f.360:video_i1d
    print("Caall")
    if call == "f.del":
        inline_message_to_del = dict_messeges_to_del_inline[call.from_user.id]
        await bot.delete_message(inline_message_to_del.chat.id, inline_message_to_del.message_id)
        del dict_messeges_to_del_inline[call.from_user.id]
    else:

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
    if call == "s.dell":
        messages_to_del = dict_messeges_to_del_inline_search[call.from_user.id]
        for mes in messages_to_del:
            await bot.delete_message(mes.chat.id, mes.message_id)
    else:
        print("gggg")
        print("call", call)
        video_id = str(call.data).split(".")[-1]
        messages_to_del = dict_messeges_to_del_inline_search[call.from_user.id]
        print("messages_to_del", dict_messeges_to_del_inline_search)
        for mes in messages_to_del:
            await bot.delete_message(mes.chat.id, mes.message_id)
        await manual_download(video_id, call)


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('a.'))
async def another_callback(call):
    print("CAL", call)
    call_data_list = str(call.data).split(":")
    video_id = call_data_list[-1]
    flag_resolution = call_data_list[0]
    inline_message_to_del = dict_messeges_to_del_inline[call.from_user.id]
    await bot.delete_message(inline_message_to_del.chat.id, inline_message_to_del.message_id)
    del dict_messeges_to_del_inline[call.from_user.id]
    yt_obj = dict_yt_obj[video_id]
    del dict_yt_obj[video_id]
    #
    print(yt_obj)
    #
    name_of_file = await another_download(flag_resolution, video_id, call.from_user.id, yt_obj)
    await send(name_of_file, call.from_user.id, yt_obj)




#

#
asyncio.run(bot.polling())
