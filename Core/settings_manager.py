import json
import time
from os import path
from typing import Optional

import requests
from bs4 import BeautifulSoup
from termcolor import cprint

from Core.app_configurator import set_download_quality, set_chrome_driver_location


class SettingsManager:
    """ The configuration class"""
    github_url = None
    proprieties_file_name = "proprieties.json"
    current_version = None
    base_url = None
    auto_complete_url = None
    search_base_url = None
    available_qualities = ['1080', '720', '480', '360', '240']
    chrome_driver_location = None
    setting_file_name = None
    chosen_quality = None

    def check_for_proprieties_file(self):
        """ Check and load the proprieties.json that contains app configuration"""
        if path.exists(self.proprieties_file_name):
            cprint(f'Loading {self.proprieties_file_name}', "green")
            self.retrieve_proprieties_file()
        else:
            cprint('' + "proprieties.json is doesn't exists, please download it from the repo !", "red")
            self.run_app_configurator()

    def retrieve_proprieties_file(self):
        """ Retrieve the proprieties file values"""
        with open(self.proprieties_file_name, "r") as settings_file:
            json_settings = json.loads(settings_file.read())
            try:
                self.current_version = json_settings['current_version']
                self.github_url = json_settings['github_url']
                self.base_url = json_settings['base_url']
                self.auto_complete_url = self.base_url + json_settings['auto_complete_url']
                self.search_base_url = self.base_url + json_settings['search_base_url']
                self.available_qualities = json_settings['available_qualities']
                self.setting_file_name = json_settings['setting_file_name']
            except KeyError:
                raise Exception("The are missing values in the proprieties file")

    def test_if_online(self) -> bool:
        """ check the return status of the website"""
        cprint("Testing connectivity to EgyBest", "green")
        response = requests.get(self.base_url)
        if response.status_code == 200:
            cprint("EgyBest website is available", "green")
            return True
        else:
            cprint("EgyBest website is down", "red")
            return False

    def check_for_saved_settings(self):
        """ Check and load the setting if they exist else run the app configurator"""
        if path.exists(self.setting_file_name):
            cprint('Settings file exists ', "green")
            configure = self.retrieve_settings()
            self.reconfigure_app(configure)
        else:
            cprint("Settings file is not available, running the app configurator!", "red")
            self.run_app_configurator()

    def retrieve_settings(self) -> Optional[bool]:
        """ Retrieve the application settings from the settings.json file """
        with open(self.setting_file_name, "r") as settings_file:
            json_settings = json.loads(settings_file.read())
            cprint(f"\n{'-' * 10}Current settings{'-' * 10}", "yellow")
            for k in json_settings:
                cprint(f"{k} : {json_settings[k]}", "blue")
            try:
                self.chosen_quality = json_settings["chosen_quality"]
                self.chrome_driver_location = json_settings["chrome_driver_location"]
            except KeyError as e:
                cprint(f"\nCoudn't retrieve settings, "
                       f"There are some missing value on the {self.setting_file_name} file!", "red")
                return True

    def run_app_configurator(self):
        """ Generate the settings file"""
        # Choosing the download quality
        cprint('Running App configurator', "blue")
        # Step 01 check for exiting updates.

        cprint('Step 01: Choose your preferable video quality for future downloads.', "blue")
        set_download_quality(self)

        cprint('Step 02: Checking the chrome driver.', "blue")
        set_chrome_driver_location(self)

        cprint('Step 03: Saving the settings file.', "blue")

        self.save_settings()

    def save_settings(self):
        """ Save the settings to the json file"""
        settings = {
            "chrome_driver_location": self.chrome_driver_location,
            "chosen_quality": self.chosen_quality
        }
        with open(self.setting_file_name, "w") as settings_file:
            json.dump(settings, settings_file, indent=3)
            settings_file.close()
        cprint('Settings file has been saved correctly', 'green')

    def reconfigure_app(self, configure=False):
        if configure:
            self.run_app_configurator()
        else:
            response = input('Do you want to reconfigure the APP (y/n) ?:')
            if response not in ("n", "no"):
                self.run_app_configurator()
        cprint('App is ready for use !', "green")

    def checking_for_updates(self):
        """ Check for repo updates form the github link """
        cprint('Looking for updates ,please wait !', "yellow")
        r = requests.get(self.github_url)
        soup = BeautifulSoup(r.text, "html.parser")
        github_version = soup.select_one("#readme > div.Box-body > article > h1").text.split('v')[1][1:-1]
        if github_version != self.current_version:
            cprint(F"\nYou have version {self.current_version} of the app please install version {github_version}! from"
                   F"\n{self.github_url}", 'red')
            exit()
        else:
            cprint('Application is up to date', "green")

    def get_settings_dictionary(self) -> dict:
        """ returns the settings as a dict"""
        return {
            "base_url": self.base_url,
            "auto_complete_url": self.auto_complete_url,
            "search_base_url": self.search_base_url,
            "available_qualities": self.available_qualities,
            "chrome_driver_location": self.chrome_driver_location,
            "chosen_quality": self.chosen_quality
        }

    def check_for_connectivity_and_updates(self):
        """Check for updates and if the website is up and running"""
        while True:
            try:
                # Checking for updates
                self.checking_for_updates()
                # Test connectivity to EgyBest
                if self.test_if_online():
                    break
                cprint("re-checking the site  in 10s!", "blue")
                time.sleep(10)
            except requests.exceptions.ConnectionError:
                cprint("Error,please check your internet connection then press Enter!! #code:1", "red")
                input()
