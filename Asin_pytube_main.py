import os
import logging

pytube_logger = logging.getLogger('pytube')
pytube_logger.setLevel(logging.ERROR)
import pytube
import asyncio
from pytube import YouTube, Search
from get_path import PATH
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

async def check_available_resolutions(yt_object):
    res_list = ['360p', '480p', '720p', '1080p']
    available_res = set()
    for res in res_list:
        filtered_streams = yt_object.streams.filter(res=res, progressive=True)
        stream_list = list(filtered_streams)
        if stream_list != []:
            available_res.add(res)
    return available_res


async def get_name(video_id, user_id):
    return str(user_id) + video_id


async def download(flag_resolution, video_id, user_id, youtube_object):
    name_of_file = await get_name(video_id, user_id)
    if flag_resolution == "f.360":
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

async def my_logger(user_id, user_name, yt_obj):
    way_to_home = os.getcwd()
    log_string = f"\n{user_id}    {user_name}     {yt_obj.video_id}"
    try:
        name = yt_obj.title
        log_string += f"    {name}"
    except:
        pass
    with open(way_to_home + "\\log.txt", "a") as file:
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

