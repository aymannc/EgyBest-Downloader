import json
from os import path
import Core.appConfigurator as configurator
from termcolor import colored, cprint


class SettingsManager:
    search_base_url = "https://nero.egybest.site/explore/?q="
    available_qualities = ['1080', '720', '480', '360', '240']
    chrome_drive =None
    settings = {}
    def __init__(self):
        self.current_version = '1.0.2'
        self.default_quality = "1080"
        self.search_url = None
        self.content_url = None
        self.content_type = None
        self.content_name = None
        self.chosen_seasons_numbers_list = []
        self.chosen_seasons_url_list = []
        self.chosen_episodes_number_list = []
        self.chosen_episodes_url_list = []
        self.downloadable_episodes_url_list = []
        self.first_run = True
        self.setting_file_name = "settings.json"
        self.chrome_driver_location =""

    def check_for_settings_Json(self):
        if path.exists(self.setting_file_name):
            cprint('\nSetting File is available',"green") 
            self.retrive_settings()
            self.reconfigure_app()
        else:
            cprint('\n'+"Settings file is not avialable runing first time configurations","red")
            self.run_app_configurator()

    def retrive_settings(self):
            print('Welcome to Egy-best Movie - Series Scrapper')
            with open(self.setting_file_name,"r") as settings_file:
                json_settings = json.loads(settings_file.read())
                for key in json_settings:
                    cprint(key+":"+str(json_settings[key]),"green")
            
    def run_app_configurator(self):
        #Choose default quality for scrapping links
        cprint('\nruning App configurator', "blue")
        # Step 01 check for exiting updates.
        cprint('\nStep 01: check for exiting updates.',"blue")
        configurator.version_check(self.current_version)

        cprint('\nStep 02: choosing correct video quality for future downloads.',"blue")
        configurator.choose_default_quality(self)
        
        cprint('\nStep 03: getting chrome driver.',"blue")
        configurator.get_chrome_driver_location(self)
        
        cprint('\nStep 04: Saving settings to file.',"blue")
        settings = {
           "chrome_driver_location" : self.chrome_driver_location,
           "default_quality" : self.default_quality,
           "available_qualities":self.available_qualities,
           "first_run":False,
           "setting_file_name":self.setting_file_name
           
        }
        self.save_settings(settings=settings)

    def save_settings(self,settings):
        with open(self.setting_file_name,"w") as settings_file:
            json.dump(settings,settings_file,indent=3)
            settings_file.close()
        cprint('\nSettings file has been saved correctely','green')
            
    def reconfigure_app(self):
        response = input('\nDo you want to reconfigure the APP (y/n) ?:')
        if response not in ("n", "no"):
            self.run_app_configurator()
        else:
            cprint('\n Thanks, lets downloads stuff !',"green")

        
            

