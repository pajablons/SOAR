import copy
import json
import os


# Container class for accessing json-based config settings
class Config:
    configPath = ''
    cfgDirectory = {}

    @staticmethod
    def setConfigPath(path: str):
        if not os.path.exists(path):
            raise ValueError(f"Config path does not exist: '{path}'")
        Config.configPath = path

    # Factory method for creating new config holders.  We cache the configs for repeated access.
    @staticmethod
    def getConfig(filename: str) -> dict:
        if filename not in Config.cfgDirectory.keys():
            truePath = os.path.join(Config.configPath, f"{filename}.json")
            if not os.path.exists(truePath):
                raise ValueError(f"File does not exist: '{truePath}'")
            with open(truePath, 'r') as conf:
                Config.cfgDirectory[filename] = json.load(conf)
        return copy.deepcopy(Config.cfgDirectory[filename])
