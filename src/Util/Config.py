import copy
import json
import os


# Container class for accessing json-based config settings
class Config:
    configPath = ''
    cfgDirectory = {}

    # App driver sets the path to where config files are stored on startup
    @staticmethod
    def setConfigPath(path: str):
        # Error and end if the path doesn't exist
        if not os.path.exists(path):
            raise ValueError(f"Config path does not exist: '{path}'")
        Config.configPath = path

    # Factory method for creating new config holders.  We cache the configs for repeated access, but return copies.
    @staticmethod
    def getConfig(filename: str) -> dict:
        # Load the file if we haven't yet
        if filename not in Config.cfgDirectory.keys():
            # absolute path
            truePath = os.path.join(Config.configPath, f"{filename}.json")
            # Error if the file doesn't exist
            if not os.path.exists(truePath):
                raise ValueError(f"File does not exist: '{truePath}'")
            # Read in the file as a dict
            with open(truePath, 'r') as conf:
                Config.cfgDirectory[filename] = json.load(conf)
        # We return a deep copy of the config dict, so that each entity can modify its own config with updates
        return copy.deepcopy(Config.cfgDirectory[filename])
