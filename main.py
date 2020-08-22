from Core.UpdateChecker import check_for_updates
from Core.SettingsManager import SettingsManager
import json
import Core.contentsearch as searcher 
if __name__ == "__main__":


    #initate Settings Manager class
    SettingsManager = SettingsManager()

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