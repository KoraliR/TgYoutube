from pytube import YouTube
import datetime as dt
PATH = "C:/Python project/Youtube/Videos/"



def check_video_available(youtube_object):
    try:
        flag_available = youtube_object.check_availability()
    except Exception as error:
        return error
    return flag_available
def youtube_object_init(url):
    youtube_object = YouTube(url)
    return youtube_object

def get_started(url):
    print("youtube_object_init_start")
    youtube_object = youtube_object_init(url)
    print("youtube_object_init_end")
    print("check_video_start")
    flag_available = check_video_available(youtube_object)
    print("check_video_end")
    if flag_available == None:
        return youtube_object
    else:
        return False

def get_name(user_id):
    date = str(dt.datetime.now())
    date = date.replace(" ", "")
    date = date.replace(":", "")
    date = date.replace(".", "")
    name_of_file = str(user_id) + str(date)
    return name_of_file


def download_main(url, user_id, flag, youtube_object):
    print("youtube_object_init_start2")
    #youtube_object = youtube_object_init(url)
    print("youtube_object_init_end2")
    print("get_name_start")
    name_of_file = get_name(user_id)
    print("get_name_end")
    if flag == 1: #лучшее
        print("downloadFlag1_start")
        youtube_object.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
            output_path=PATH, filename=name_of_file + ".mp4")
        return name_of_file + ".mp4"
    elif flag == 2:  # нормальное
        try:
            youtube_object.streams.filter(progressive=True, file_extension='mp4', res='480p').order_by(
                'resolution').desc().first().download(
                output_path=PATH, filename=name_of_file + ".mp4")
        except:
            try:
                youtube_object.streams.filter(progressive=True, file_extension='mp4', res='360p').order_by(
                    'resolution').desc().first().download(
                    output_path=PATH, filename=name_of_file + ".mp4")
            except:
                try:
                    youtube_object.streams.filter(progressive=True, file_extension='mp4', res='720p').order_by(
                        'resolution').desc().first().download(
                        output_path=PATH, filename=name_of_file + ".mp4")
                except:
                    return False
        return name_of_file + ".mp4"
    elif flag == 3: #аудио
        youtube_object.streams.filter(only_audio=True).order_by('abr').desc().first().download(output_path=PATH,
                                                                                   filename=name_of_file + ".mp3")
        return name_of_file + ".mp3"