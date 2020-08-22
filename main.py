from Core.UpdateChecker import check_for_updates
from Core.SettingsManager import SettingsManager
import json
import Core.contentsearch as searcher 
import requests
from termcolor import cprint
from slack import WebClient
import os
import time



if __name__ == "__main__":


    client = WebClient(token='xoxb-1329250213920-1305440281394-zZo4oxvoptqBu3SrbvRx3oWJ')

    def test_egy_best(base_url):
        response = requests.get(base_url)
        if response.status_code == 200:
                cprint("Egybest website is available","green")
                client.chat_postMessage(channel ="#general", text="Egybest is up and runing")
        else:
                cprint("Egybest website is down","red")
                #client.chat_postMessage(channel ="#general", text="Egybest is down")
                #exit(cprint("App is not usable without egybest website up and runing","red"))

    #initate Settings Manager class
    SettingsManager = SettingsManager()

    
    while True:
        #Test connnectivity to egybest 
        test_egy_best(SettingsManager.base_url)
        time.sleep(60)
    #check if Json Settings is Available
    SettingsManager.check_for_settings_Json()

    searcher.start(SettingsManager)
    


    #initatne Egybest scrapper class
    
    # egy = EgyBest()
    # #check for updates on the original github repository
    # check_for_updatens(egy.current_version)
    
    

    # # link = "https://nero.egybest.site/movie/joker-2019/"480
    # try:
    #     while 1:
    #         egy.start()
    #         try:
    #             choice = egy.get_int_input("Do you want to restart ? : (1/0)")
    #             if choice == 0:
    #                 break
    #             egy.reset()
    #         except:
    #             break
    # except Exception as e:
    #     egy.reset_chrome_driver()
    #     print(e)
    # finally:
    #     egy.destroy_chrome_driver()
