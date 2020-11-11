from os.path import isfile

from termcolor import cprint


def set_download_quality(settings_manager: 'SettingsManager'):
    """Chose the download quality of the videos from pre-defined qualities"""
    response = "y"
    if settings_manager.chosen_quality:
        response = get_string_input(
            F"\nThe download quality is {settings_manager.chosen_quality} do you want to change it ?(y/n)")
    if response not in ("n", "no"):
        while True:
            settings_manager.chosen_quality = get_string_input(
                F'\nPlease make sure to chose one of the following qualities : '
                F'{settings_manager.available_qualities}')
            if settings_manager.chosen_quality in settings_manager.available_qualities:
                break
        cprint(f'\nSuccess: the quality is {settings_manager.chosen_quality} now!', "green")


def set_chrome_driver_location(settings_manager: 'SettingsManager'):
    """ Set the chrome driver executable location"""
    response = "y"
    if settings_manager.chrome_driver_location:
        response = get_string_input(
            F"\nThe driver location is {settings_manager.chrome_driver_location} do you want to change it ?(y/n)")
    if response not in ("n", "no"):
        while True:
            settings_manager.chrome_driver_location = get_string_input(
                '\nPlease past the link to your chrome driver location:')
            try:
                if isfile(settings_manager.chrome_driver_location) and settings_manager.chrome_driver_location.endswith(
                        ".exe") and "chromedriver" in settings_manager.chrome_driver_location:
                    break
                else:
                    cprint("\nError: This is not a valid file path or not an executable ! ", "red")
            except Exception as _:
                cprint("This file path is not valid or doesn't exists !", "red")


def get_string_input(output_msg):
    try:
        return str(input(output_msg)).lower()
    except:
        exit("User exited the app")
