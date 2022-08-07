from configparser import ConfigParser

config = ConfigParser()

config["server_info"] = {
    "url": '127.0.0.1',
    "port": '3002'
}


with open("config.ini", "w") as f:
    config.write(f)
