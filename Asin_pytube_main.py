import os
import logging
import moviepy.editor as mp

pytube_logger = logging.getLogger('pytube')
pytube_logger.setLevel(logging.ERROR)
import pytube
import asyncio
from pytube import YouTube, Search
from get_path import PATH
#USERS = set()
#PATH = "C:\Python project\Youtube\Videos"
async def make_yt_object(url):
    try:
        youtube_object = YouTube(url)
    except:
        return False
    return youtube_object

async def check_video_availability(yt_obj):
    flag_available = yt_obj.check_availability()
    print(flag_available)
    if flag_available == None:
        return True
    else:
        return False

async def another_available_resolutions(yt_object, availbale_resolutions):
    res_list = {'144p', '240p', '360p', '480p', '720p', '1080p'}
    availbale_resolutions = set(availbale_resolutions)
    available_res_another = set()
    another_for_check = res_list - availbale_resolutions
    for res in another_for_check:
        filtered_streams = yt_object.streams.filter(res=res, adaptive=True)
        stream_list = list(filtered_streams)
        if stream_list != []:
            available_res_another.add(res)
    return available_res_another

async def check_available_resolutions(yt_object):
    res_list = ['144p', '240p', '360p', '480p', '720p', '1080p']
    available_res = set()
    for res in res_list:
        filtered_streams = yt_object.streams.filter(res=res, progressive=True)
        stream_list = list(filtered_streams)
        if stream_list != []:
            available_res.add(res)
    return available_res


async def get_name(video_id, user_id):
    return str(user_id) + video_id


async def mixing(name_of_file):
    video = mp.VideoFileClip(PATH + "/Temp_video/" + name_of_file + "temp.mp4")
    audio = mp.AudioFileClip(PATH + "/Temp_audio/" + name_of_file + "temp.mp3")
    video = video.set_audio(audio)
    video.write_videofile(PATH + "/" + name_of_file + ".mp4")
    print("MP4#NAME", PATH + "\\Temp_video\\" + name_of_file + "temp.mp4")
    print("MP3#NAME",PATH + "\\Temp_audio\\" + name_of_file + "temp.mp3")
    print("exit", PATH + "\\" + name_of_file + ".mp4")
    await del_temp_files(name_of_file)
    return name_of_file + ".mp4"


async def audio_download(name_of_file, yt_obj):
    yt_obj.streams.filter(only_audio=True).order_by('abr').desc().first().download(output_path=PATH + "/Temp_audio",
                                                                                           filename=name_of_file + "temp.mp3")

async def another_download(flag_resolution, video_id, user_id, youtube_object): #обавить сведение звука и видео
    name_of_file = await get_name(video_id, user_id)
    for_video = "/Temp_video"
    if flag_resolution == "a.144":
        youtube_object.streams.filter(adaptive=True, file_extension='mp4', res="144p").order_by(
            'resolution').desc().first().download(
            output_path=PATH + for_video, filename=name_of_file + "temp.mp4")
       # return name_of_file + ".mp4"
    elif flag_resolution == "a.240":
        youtube_object.streams.filter(adaptive=True, file_extension='mp4', res="240p").order_by(
            'resolution').desc().first().download(
            output_path=PATH + for_video, filename=name_of_file + "temp.mp4")
        #return name_of_file + ".mp4"
    elif flag_resolution == "a.360":
        youtube_object.streams.filter(adaptive=True, file_extension='mp4', res="360p").order_by(
            'resolution').desc().first().download(
            output_path=PATH + for_video, filename=name_of_file + "temp.mp4")
        #return name_of_file + ".mp4"
    elif flag_resolution == "a.480":
        youtube_object.streams.filter(adaptive=True, file_extension='mp4', res="480p").order_by(
            'resolution').desc().first().download(
            output_path=PATH + for_video, filename=name_of_file + "temp.mp4")
        #return name_of_file + ".mp4"
    elif flag_resolution == "a.720":
        youtube_object.streams.filter(adaptive=True, file_extension='mp4', res="720p").order_by(
            'resolution').desc().first().download(
            output_path=PATH + for_video, filename=name_of_file + "temp.mp4")
        # return name_of_file + ".mp4"
    elif flag_resolution == "a.10":
        youtube_object.streams.filter(adaptive=True, file_extension='mp4', res="1080p").order_by(
            'resolution').desc().first().download(
            output_path=PATH + for_video, filename=name_of_file + "temp.mp4")
    await audio_download(name_of_file, youtube_object)
    name_of_file_to_send = await mixing(name_of_file)
    #task_mixing = asyncio.create_task(mixing(name_of_file))
    #name_of_file_to_send = await task_mixing
    #loop = asyncio.new_event_loop()
   # asyncio.set_event_loop(loop)
    #name_of_file_to_send = loop.run_until_complete(mixing(mixing(name_of_file)))
    #loop.close()

    return name_of_file_to_send

async def download(flag_resolution, video_id, user_id, youtube_object):
    name_of_file = await get_name(video_id, user_id)
    if flag_resolution == "f.144":
        youtube_object.streams.filter(progressive=True, file_extension='mp4', res="144p").order_by(
            'resolution').desc().first().download(
            output_path=PATH, filename=name_of_file + ".mp4")
        return name_of_file + ".mp4"
    elif flag_resolution == "f.240":
        youtube_object.streams.filter(progressive=True, file_extension='mp4', res="240p").order_by(
            'resolution').desc().first().download(
            output_path=PATH, filename=name_of_file + ".mp4")
        return name_of_file + ".mp4"
    elif flag_resolution == "f.360":
        youtube_object.streams.filter(progressive=True, file_extension='mp4', res="360p").order_by(
            'resolution').desc().first().download(
            output_path=PATH, filename=name_of_file + ".mp4")
        return name_of_file + ".mp4"
    elif flag_resolution == "f.480":
        youtube_object.streams.filter(progressive=True, file_extension='mp4', res="480p").order_by(
            'resolution').desc().first().download(
            output_path=PATH, filename=name_of_file + ".mp4")
        return name_of_file + ".mp4"
    elif flag_resolution == "f.720":
        youtube_object.streams.filter(progressive=True, file_extension='mp4', res="720p").order_by(
            'resolution').desc().first().download(
            output_path=PATH, filename=name_of_file + ".mp4")
        return name_of_file + ".mp4"
    elif flag_resolution == "f.10":
        youtube_object.streams.filter(progressive=True, file_extension='mp4', res="1080p").order_by(
            'resolution').desc().first().download(
            output_path=PATH, filename=name_of_file + ".mp4")
        return name_of_file + ".mp4"
    elif flag_resolution == "f.a":
        youtube_object.streams.filter(only_audio=True).order_by('abr').desc().first().download(output_path=PATH,
                                                                                               filename=name_of_file + ".mp3")
        return name_of_file + ".mp3"

async def my_logger(user_id, user_name, yt_obj, flag_search=False):
    way_to_home = os.getcwd()
    log_string = f"\n{user_id}    {user_name}     {yt_obj.video_id}     {flag_search}"
    try:
        name = yt_obj.title
        log_string += f"    {name}"
    except:
        pass
    with open(way_to_home + "/log.txt", "a") as file:
        file.write(log_string)

async def search_youtube(search_request):
    if len(str(search_request)) > 60:
        return False
    else:
        search_results_list = []
        counter = 0
        search_request_object = Search(search_request)
        print("search_ob", search_request_object)
        for result in search_request_object.results:
            print("result", result)
            search_results_list.append(result)
            counter += 1
            if counter > 5:
                break
        #search_results_list = search_results_list.reverse()
        print("f", search_results_list)
        return search_results_list

async def get_weight(yt_obj, available_res):
    weight = dict()
    for res_i in available_res:
        filtered_streams = yt_obj.streams.filter(progressive=True, file_extension='mp4', res=res_i)
        weight_temp = filtered_streams.first().filesize
        weight[res_i] = str(weight_temp)
        print("res",str(weight_temp))
    return weight

async def get_another_weight(yt_obj, another_res):
    another_weight = dict()
    for res_i in another_res:
        filtered_streams = yt_obj.streams.filter(file_extension='mp4', res=res_i, adaptive=True, type="video")
        weight_temp = filtered_streams.first().filesize
        print("TEMP_ANOTHER", weight_temp)
        another_weight[res_i] = str(weight_temp)
        print("res", str(weight_temp))
    return another_weight

async def availbale_formats_information(yt_obj, availbale_res, another_available_res, weight_dict, another_weight_dict):
    title_text = ""
    all_resolutions = ("144p", "240p", "360p", "480p", "720p", "1080p")
    # weight_dict = await get_weight(yt_obj, availbale_res)
    # another_weight_dict = await get_another_weight(yt_obj, another_available_res)
    OK_res = []
    print("AN", another_weight_dict)
    for res in all_resolutions:
        if res in availbale_res:
            #weight_dict = await get_weight(yt_obj, availbale_res)
            weight = weight_dict[res]
            if int(weight) // (1024 * 1024) == 0:
                weight = "<1"
                title_text += f"✅   {res}:   {weight} МБ\n"
                OK_res.append(res)
            elif int(weight) // (1024 * 1024) > 60:
                title_text += f"🚫   {res}:   Файл слишком большой\n"
            else:
                weight = int(weight) // (1024 * 1024)
                title_text += f"✅   {res}:   {weight} МБ\n"
                OK_res.append(res)
        elif res in another_available_res:
            weight = another_weight_dict[res]
            if int(weight) // (1024 * 1024) == 0:
                weight = "<1"
                title_text += f"⚡  {res}    {weight} МБ\n"
                OK_res.append(res)
            elif int(weight) // (1024 * 1024) > 60:
                title_text += f"🚫   {res}:   Файл слишком большой\n"
            else:
                weight = int(weight) // (1024 * 1024)
                title_text += f"⚡  {res}    {weight} МБ\n"
                OK_res.append(res)
        else:
            title_text += f"❌   {res}\n"
    filtered_streams = yt_obj.streams.filter(only_audio=True)
    weight_audio = filtered_streams.first().filesize
    if int(weight_audio) // (1024 * 1024) == 0:
        weight_audio = "<1"
    else:
        weight_audio = int(weight) // (1024 * 1024)
    title_text += f"✅   MP3: {weight_audio} МБ"
    return (title_text, OK_res)



def get_users():
    print("GET_USERS")
    way = os.getcwd()
    name = "/users.txt"
    with open(way + name, "r") as file:
        for user in file:
            USERS.add(int(str(user).replace(";", "")))
    return USERS


async def make_users(user_id):
    way_to_home = os.getcwd()
    users_string = user_id
    with open(way_to_home + "/users.txt", "a") as file:
        file.write(str(users_string) + ';')



async def del_temp_files(name_of_file):
    os.remove(PATH + "\\Temp_video\\" + name_of_file + "temp.mp4")
    os.remove(PATH + "\\Temp_audio\\" + name_of_file + "temp.mp3")
