import configparser


class Config:
    
    data = {}
    # singleton pattern
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Config,cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./battleship/config/mapconfig.conf')
        self.readConfig()

    def readConfig(self):
        for section in self.config.sections():
            self.data[section] = dict(self.config[section])
