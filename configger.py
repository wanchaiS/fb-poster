import os
import shutil
import json

# -------------------------------------------------------------------------------------------
# loads config settings file
# -------------------------------------------------------------------------------------------


def get_config():

    # default/local configuration file
    defaultConfigFile = os.getcwd() + "/defaultConfig.json"
    localConfigFile = os.getcwd() + "/localConfig.json"

    # hard-check default config exists
    if not os.path.exists(defaultConfigFile):
        print("")
        print("Oops: Default config file '" +
              defaultConfigFile + "' file not found")
        print("Check you have the full/latest deploy installed")
        exit()

    # create local config file from default if not exist
    if not os.path.exists(localConfigFile):
        shutil.copy2(defaultConfigFile, localConfigFile)

    # load default config
    with open(defaultConfigFile) as c:
        defaultConfig = json.load(c)

    # load local config
    with open(localConfigFile) as c:
        localConfig = json.load(c)

    return localConfig
