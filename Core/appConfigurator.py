from termcolor import cprint
from Core.UpdateChecker import check_for_updates

def choose_default_quality(SettingsManager):
    
    response = get_string_input(F"\nThe default quality is {SettingsManager.default_quality} do you want to change it ?(y/n)")
    if response not in ("n", "no"):
        response = ""
        while response not in SettingsManager.available_qualities:
            response = get_string_input(F'\nPlease make sure to chose one of the available qualities : {SettingsManager.available_qualities} : ')
            SettingsManager.default_quality = response
        cprint('\nSucess:Quality Set as ' + SettingsManager.default_quality, "green")

def get_chrome_driver_location(SettingsManager):
    response = get_string_input('\nPlease past the link to your chrome driver location:')
    SettingsManager.chrome_driver_location = response


#@staticmethod
def get_string_input(output_msg):
        try:
            return str(input(output_msg)).lower()
        except:
            exit("User exited the app")




def version_check(current_version):
    check_for_updates(current_version)