import os

from twitch_talkbot.config import BotConfig
from twitch_talkbot.talkbot import Talkbot

CONFIG_FILE = os.path.join(os.path.expanduser('~'), 'twitch_talkbot_config.json')


def main():
    if not os.path.isfile(CONFIG_FILE):
        c = BotConfig()
        c.save_to_file(CONFIG_FILE)
        print("Unable to find config file. Created default in '%s', please "
              "enter appropriate values and re-run." % CONFIG_FILE)
        return

    config = BotConfig(CONFIG_FILE)
    b = Talkbot(config)
    b.run()

if __name__ == "__main__":
    main()
