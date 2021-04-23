import configparser
import os


class __Config():
    def __init__(self, path):
        config = configparser.ConfigParser()
        config.read(path, encoding='utf-8')
        self.ip = config['SERVER']['ip']
        self.port = config['SERVER']['port']
        self.secret_key = config['SERVER']['secret_key']
        self.admins = map(int, config['ADMINS']['ids'].split())

Config = __Config(os.path.abspath('config.ini'))
