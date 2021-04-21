import configparser
import pathlib

class __Config():
    def __init__(self, path):
        config = configparser.ConfigParser()
        config.read(path,encoding='utf-8')
        self.ffmpeg_path = config['FFMPEG']['ffmpeg_path']
        self.ffprobe_path = config['FFMPEG']['ffprobe_path']
        self.ip = config['SERVER']['ip']
        self.port = config['SERVER']['port']
        self.secret_key = config['SERVER']['secret_key']


Config = __Config('config.ini')
