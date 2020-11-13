import requests
from colorama import init
from termcolor import cprint

from Core.egybest import EgyBest
from Core.settings_manager import SettingsManager

if __name__ == "__main__":
    # use Colorama to make Termcolor work on Windows too
    init()
    # initiate Settings Manager class
    settings_manager = SettingsManager()
    # check for the proprieties.json file
    settings_manager.check_for_proprieties_file()

    # check for updates and if the website is up and running

    settings_manager.check_for_connectivity_and_updates()

    # check if the settings file is Available
    settings_manager.check_for_saved_settings()

    egy = EgyBest(settings_manager.get_settings_dictionary())
    while True:
        # ToDo : save VidStream links in SQLite db, so we won't have to scrape EgyBest each time
        # ToDo : make a bash file for env conf
        try:
            egy.start()
        except requests.exceptions.ConnectionError:
            cprint("\nError,please check your internet connection then press Enter!! #code:2", "red")
            input()
        except Exception as e:
            cprint("\n" + str(e), "red")
            choice = EgyBest.get_string_input("\nDo you want to restart ? ([n,no] / yes : any key)", "blue")
            if choice in ('n', 'no'):
                egy.exit()
