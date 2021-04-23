import os
import subprocess
from multiprocessing import Process
from typing import NamedTuple
import json

from config import Config
from utils.id_gen import id_generator
import pathlib

p = pathlib.Path(__file__).parent.absolute()
os.chdir(p)


class FFProbeResult(NamedTuple):
    return_code: int
    json: dict
    error: str


def ffprobe(file_path) -> FFProbeResult:
    if os.name == 'nt':
        command = r'./ffprobe'
    elif os.name == 'posix':
        command = 'ffprobe'
    command_array = [command,
                     "-v", "quiet",
                     "-print_format", "json",
                     "-show_format",
                     "-show_streams",
                     file_path]

    result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)
    return FFProbeResult(return_code=result.returncode,
                         json=json.loads(result.stdout),
                         error=result.stderr)


def transcoding(path_temp, path_o):
    metadata = ffprobe(path_temp).json
    for stream in metadata['streams']:
        if stream["codec_type"] == "video":
            if 'h264' in stream['codec_name']:
                cv = 'copy'
            else:
                cv = 'h264'
    f = open("ffmpeg_log.txt", "w")
    if os.name == 'nt':
        command = r'./ffmpeg'
        shell = False
    elif os.name == 'posix':
        command = 'ffmpeg'
        shell = True
    p = subprocess.call(
        '{} -i {} -metadata:s:a:0 language=rus -c:v {} -c:a copy -b:v 2M -sn {}'.format(command,
                                                                                         path_temp, cv,
                                                                                         path_o), stderr=f, shell=shell)
    os.remove(path_temp)


def save_video(anime_id, ep, dub, video, ffmpeg_tr: bool):
    # 2 часа ночи, а я мучаюсь с этими путями :( ПАМАГИТЕ
    cur_path = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join('static', 'video', str(anime_id))
    full = os.path.join(cur_path, directory)
    """Возращает путь info.json в случае успеха"""
    if not os.path.exists(full):
        os.mkdir(full)
    full_dub_path = os.path.join(full, dub)
    if not os.path.exists(full_dub_path):
        os.mkdir(full_dub_path)

    _, filename = os.path.splitext(video.filename)
    name = id_generator() + filename
    if ffmpeg_tr:
        path_temp = os.path.join(cur_path, 'temp', name)
        path_o = os.path.join(full_dub_path, name)
        video.save(path_temp)
        p = Process(target=transcoding, args=(path_temp, path_o))
        p.start()
    else:
        path = os.path.join(full_dub_path, name)
        video.save(path)
    info_path = os.path.join(full, 'info.json')
    if not os.path.exists(info_path):
        with open(info_path, 'w') as data:
            json.dump({}, data)

    with open(info_path, 'r') as data:
        info: dict = json.load(data)
        info_dub = info.get(dub)
        web_path = f'{anime_id}/{dub}/{name}'
        if info_dub:
            info_dub[ep] = web_path
        else:
            info[dub] = {ep: web_path}
    with open(info_path, "w") as data:
        json.dump(info, data)

    return directory
