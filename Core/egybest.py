import os
import sys
import time
from enum import Enum
from typing import Tuple, Optional

import requests
from bs4 import BeautifulSoup
from pySmartDL import SmartDL
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import cprint


class Mode(Enum):
    AUTO_COMPLETE = "auto_complete"
    PAGE_BASED = "page_based"


class EgyBest:

    def __init__(self, settings: Optional[dict]):
        if settings:
            self.base_url: str = settings["base_url"]
            self.auto_complete_url: str = settings["auto_complete_url"]
            self.search_base_url: str = settings["search_base_url"]
            self.available_qualities: list = settings["available_qualities"]
            self.chrome_driver_location: str = settings["chrome_driver_location"]
            self.chosen_quality: str = settings["chosen_quality"]

        self.content_url = None
        self.content_type = None
        self.content_name = None

        self.chrome_driver = None
        self.first_run = None

        self.chosen_seasons_numbers_list = []
        self.chosen_seasons_url_list = []
        self.chosen_episodes_number_list = []
        self.chosen_episodes_url_list = []
        self.downloadable_episodes_url_list = []

    def reset(self):
        self.__init__()

    def start(self) -> None:
        """ Start the downloading process, This is the main entrance point """

        while True:
            # getting user input
            try:
                self.get_content_url(*self.get_link_from_keyword())
            except requests.exceptions.ConnectionError:
                cprint("Error,please check your internet connection then press Enter!!, #code:3", "red")
                input()
            except ValueError as e:
                cprint(str(e), "red")
                continue
            else:
                if self.content_type and self.content_url:
                    break
                else:
                    raise ValueError("There was an error during the extraction of the url")
        # Beginning the process of downloading based on the content_type
        if self.content_type == "series":
            self.download_seasons()
        elif self.content_type == "movie":
            self.chosen_episodes_url_list.append(self.content_url)
            self.gather_download_link()

        file_name = self.save_links_to_file()
        self.get_user_download_choice(file_name)

    def get_link_from_keyword(self, mode: Mode = Mode.AUTO_COMPLETE) -> Tuple[str, Mode]:
        """ Generate the page link from the user's input"""

        search_keyword = self.get_string_input("What are you searching for ? :")

        if mode == Mode.AUTO_COMPLETE:
            # Link : ../autoComplete.php?q=
            return (self.auto_complete_url + search_keyword), mode
        elif mode == Mode.PAGE_BASED:
            # Link : ../explore/?output_format=json&output_mode=movies_list&page=#&q=*
            return self.search_base_url.replace("#", 1).replace("*", search_keyword), mode
        else:
            raise ValueError("Mode value is not valid!")

    # function to get the download content
    def get_content_url(self, link: str, mode: Mode):
        """ Selecting the series/movie page """
        cprint("Searching for results !", "green")
        # Chose the method given the mode of scraping
        if mode == Mode.AUTO_COMPLETE:
            self.use_auto_complete(link)
        elif mode == Mode.PAGE_BASED:
            self.use_page_based(link)
        else:
            raise ValueError("None acceptable mode value!")

    def use_auto_complete(self, link: "the auto_complete link + keyword"):
        """ Using the auto complete link to get movies/series json data from a given keyword"""

        def print_content_name(_values):
            """Color printing the elements in the list"""
            for i, e in enumerate(_values, 1):
                content_type = e['u'].split('/')[0]
                print(f"\t{i} -> ", end=' ')
                cprint(f"{e['t']}", 'magenta', attrs=['concealed'], end=' ')
                print(", Type : ", end=' ')
                cprint(f"{content_type}", 'blue', attrs=['reverse'])

        r = requests.get(link)
        # checking the page availability
        if r.status_code == 200:
            # extracting the first element of the dict dynamically
            values = list(iter(r.json().values()))[0]
            if len(values) < 1:
                raise ValueError("\nNo result found, please try another keyword ! #code:4")
            print_content_name(values)
            # looking for user choice
            while True:
                try:
                    try:
                        # get the movies/series index
                        index = self.get_int_input("Enter link number :") - 1
                        if index < 0:
                            raise IndexError()
                    except ValueError as _:
                        raise IndexError()
                    else:
                        # Extracting the values from the sub-dict
                        selected_element = values[index]
                        self.content_url = self.base_url + selected_element['u']
                        self.content_type = selected_element['u'].split("/")[0]
                        self.content_name = selected_element['t']
                        break
                except IndexError as _:
                    retry = self.get_string_input(
                        "Non valid input ,retry ? ([n,no]/ yes : any key) :")
                    if retry.lower() in ['n', 'no']:
                        self.content_type = None
                        break

        else:
            cprint("\nThere was a problem connecting to EgyBest, please check you internet connection or try later ! ",
                   "red")

    def use_page_based(self, link):
        """Legacy code: using the html page response to extract the series/movie link"""
        # Legacy code
        res = self.get_bs4_result(self.search_url, "a", "movie")
        # Displaying the fetched linked
        for i, link in enumerate(res, 1):
            content_type = None
            try:
                content_type = self.get_url_type(link['href']).upper()
                print(i, " ->", link.contents[4].text, ", Type : ", content_type, ",", "IMDB Rating :",
                      link.contents[0].i.i.text, '\n')
            except:
                print(i, " ->", link.contents[2].text,
                      ", Type : ", content_type)
        # looking for user choice
        while res:
            try:
                self.content_url = res[self.get_int_input(
                    "Enter link number :") - 1]['href']
                break
            except:
                retry = self.get_string_input(
                    "Non valid input ,retry ? (y/n) :")
                if retry != "y":
                    self.content_type = None
                    return

        if not res:
            print("Didn't found a thing")
        elif self.content_url:
            self.content_type = self.get_url_type(self.content_url)

    # initializing chrome drivers
    def init_chrome_driver(self):
        """"Initializing chrome drivers"""
        # If there is no instance create one
        if not self.chrome_driver:

            self.first_run = True
            print("Initializing chrome Driver")
            try:
                # Creating chrome options
                caps = DesiredCapabilities().CHROME
                caps["pageLoadStrategy"] = "eager"
                chrome_options = webdriver.ChromeOptions()

                # prefs = {"profile.default_content_setting_values.cookies": 2,
                #          "profile.block_third_party_cookies": True,
                prefs = {"profile.managed_default_content_settings.images": 2,
                         "profile.default_content_settings.images": 2}
                chrome_options.add_experimental_option("prefs", prefs)

                chrome_options.add_argument('--incognito')
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--log-level=3')
                chrome_options.add_argument('--silent')

                self.chrome_driver = webdriver.Chrome(executable_path=self.chrome_driver_location,
                                                      options=chrome_options)
            except Exception as e:
                raise ConnectionError("Couldn't init chrome drivers" + str(e))

    # closing and destroying chrome driver instant
    def destroy_chrome_driver(self):
        try:
            if self.chrome_driver is not None:
                self.chrome_driver.close()
                print("Driver Closed")
            else:
                print("Driver already closed")
        except Exception as e:
            print(e)

    def make_egybest_happy(self):
        """Clicking on the search area to pop up ads and make EgyBest happy"""

        try:
            self.chrome_driver.find_element_by_css_selector(
                '#head > div > div.topsrch.suba_rel.nohide.td.vam > form > input.q.autoComplete') \
                .click()
            m = "\nClicking on an ad to make EgyBest happy this will take approximately 5s and will run 1 time only !"
            d = f"\n{'-' * len(m)}"
            cprint(d + m + d, "blue")
            time.sleep(5)
            self.close_popups()
        except Exception as _:
            pass

    def gather_download_link(self):
        self.init_chrome_driver()
        print("Accessing EgyBest page")

        # Open the link using selenium
        while len(self.chosen_episodes_url_list) > 0:
            try:
                self.chrome_driver.get(self.chosen_episodes_url_list[0])
                del self.chosen_episodes_url_list[0]
            except TimeoutException:
                response = self.get_string_input(
                    "\nThere was a problem connecting to the EgyBest,The site is down or you have some "
                    "connectivity issues"
                    "\nDo you want to retry (n,no)/yes:any key", "red")
                if response not in ["n", "no"]:
                    continue
                else:
                    self.exit()

        while True:
            if self.first_run:
                self.make_egybest_happy()
                self.first_run = False

            # Chose the link that corresponds with the selected quality
            self.chose_quality()
            in_download_page = True
            # Closing pop-up pages
            for handler in self.chrome_driver.window_handles:
                self.chrome_driver.switch_to.window(handler)
                if len(self.chrome_driver.window_handles) == 1 and "egybest" in self.chrome_driver.current_url:
                    in_download_page = False
                elif "vidstream" not in self.chrome_driver.current_url:
                    self.chrome_driver.close()
            if in_download_page:
                print("Accessing the download page")
                break
            input()

        timeout = 10
        while True:
            try:
                e = WebDriverWait(self.chrome_driver, timeout).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[1]/div/p/a[1]")))
                if not e.get_attribute("href"):
                    e.click()
            except TimeoutException:
                print("Timed out waiting for page to load")
            except StaleElementReferenceException as _:
                continue

            try:
                target_button = WebDriverWait(self.chrome_driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[contains(text(), "Download")][@href]')))
                self.close_popups()
                if not target_button.get_attribute("href"):
                    continue
            except TimeoutException as _:
                self.close_popups()
                continue
            print("Obtaining the download link")
            url = target_button.get_attribute("href")
            if url:
                self.downloadable_episodes_url_list.append(url)
                return

    def download_seasons(self, url=None):

        # ToDo : add range eps and clean this spaghetti code
        if url is None:
            url = self.content_url
        res = self.get_bs4_result(url, "div", "movies_small")[0]
        seasons_list = res.find_all("a")
        number_of_seasons = len(seasons_list)
        all_eps = False
        while number_of_seasons:
            print(
                F"There {'are' if number_of_seasons > 1 else 'is'} "
                F"{number_of_seasons} season{'s' if number_of_seasons > 1 else ''} ")
            choice = self.get_string_input(
                "Do you want to download all seasons or specific ones, type['all' or 'spec']:")
            if choice == 'all':
                all_eps = True
                self.chosen_seasons_numbers_list = [
                    i for i in range(1, number_of_seasons + 1)]
                break
            elif choice == 'spec':
                while 1:
                    chosen_number_seasons = self.get_int_input(
                        "Choose how many seasons :")
                    try:
                        if number_of_seasons >= chosen_number_seasons > 0:
                            break
                    except:
                        pass
                # ToDo : check and stop the duplicated seasons
                print("Add the seasons you want to download")
                for i in range(1, chosen_number_seasons + 1):
                    while 1:
                        choice = self.get_int_input(
                            F"{i} --> Choose a season from 1 to {number_of_seasons}:") if not None else 0
                        try:
                            if number_of_seasons >= choice >= 1:
                                print(F"Season {choice} Added")
                                self.chosen_seasons_numbers_list.append(choice)
                                break
                            else:
                                print("Non valid option")
                        except:
                            pass
                break
            print("Non valid option")

        self.chosen_seasons_numbers_list.sort()
        for i in self.chosen_seasons_numbers_list:
            self.chosen_seasons_url_list.append(seasons_list[-i]['href'])
        print("Gathering episodes Urls")
        # print("chosen_seasons_url_list", self.chosen_seasons_url_list)
        for url in self.chosen_seasons_url_list:
            res = self.get_bs4_result(url, "div", "movies_small")[0]
            episodes_list = res.find_all("a")
            number_of_eps = len(episodes_list)
            if number_of_eps:
                print(F"There're {number_of_eps} episodes in {' '.join(url.split('/')[-2].split('-')[1:])}")
                if all_eps:
                    choice = 'all'
                else:
                    choice = self.get_string_input(
                        "Do you want to download all episodes or specific ones, type['all' or 'spec']:")
                if choice == 'all':
                    self.chosen_episodes_number_list = [
                        i for i in range(1, number_of_eps + 1)]
                elif choice == 'spec':
                    while 1:
                        chosen_number_episodes = self.get_int_input(
                            "Choose how many episodes :")
                        try:
                            if number_of_eps >= chosen_number_episodes > 0:
                                break
                        except:
                            pass
                    print("Add the episodes you want to download")
                    for i in range(1, chosen_number_episodes + 1):
                        while 1:
                            # Todo : check for duplicated values on the array
                            choice = self.get_int_input(
                                F"{i} --> Choose an episode from 1 to {number_of_eps}:")
                            try:
                                if number_of_eps >= choice >= 1:
                                    print(F"Episode {choice} Added")
                                    self.chosen_episodes_number_list.append(
                                        choice)
                                    break
                                else:
                                    print("Non valid option")
                            except:
                                pass
            # print("chosen_episodes_number_list",
            #       self.chosen_episodes_number_list)
            # print("episodes_list", episodes_list)
            self.chosen_episodes_number_list.sort()
            for i in self.chosen_episodes_number_list:
                self.chosen_episodes_url_list.append(episodes_list[-i]["href"])
                self.gather_download_link()
            # print(self.downloadable_episodes_url_list)
            # print(self.chosen_episodes_url_list)
        return True

    @staticmethod
    def get_int_input(output_msg: str) -> int:
        """Getting input from user as an int"""
        cprint(output_msg, "green")
        return int(input())

    @staticmethod
    def get_string_input(output_msg: str, color="green") -> str:
        """Getting input from user as a string"""
        cprint(output_msg, color)
        return str(input()).lower()

    @staticmethod
    def get_bs4_result(url: str, html_tag: str, class_name: str):
        print("Requesting link, please wait!")
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.find_all(html_tag, class_=class_name)

    @staticmethod
    def get_url_type(url: str) -> str:
        # print(url)
        try:
            return url.split("/")[3]
        except IndexError as _:
            print("None valid link in get_url_type")
        else:
            return None

    @staticmethod
    def get_content_name(url: str) -> str:
        # print(url)
        try:
            return url.split("/")[4]
        except IndexError as _:
            print("None valid link in get_content_name")
        return None

    def exit(self, code="!"):
        self.destroy_chrome_driver()
        sys.exit("\nExited " + code)

    def close_popups(self):
        """ Closing all the popups by reversing the window_handles list"""
        for i in reversed(range(1, len(self.chrome_driver.window_handles))):
            self.chrome_driver.switch_to.window(self.chrome_driver.window_handles[i])
            self.chrome_driver.close()
        self.chrome_driver.switch_to.window(self.chrome_driver.window_handles[0])

    def close_notification_banner(self):
        """
        Closing the notification banner because we need to open a popup ad for and wait for somme seconds,
        to avoid having an infinite loop of the same page.
        """
        try:
            # Waiting for the banner to show
            timeout = 3
            try:
                WebDriverWait(self.chrome_driver, timeout).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#NotificationsAskMsg > p > a.NotificationIgnore.api"))) \
                    .click()
                self.close_popups()
            except TimeoutException:
                print("Timed out waiting for page to load")
        except Exception as ex:
            print(str(ex))

    def chose_quality(self):
        """Clicking the download link that corresponds to the chosen quality if that quality is note
        available we select the next best thing in line"""

        try:
            labels = self.chrome_driver.find_elements_by_xpath('//*[@id="watch_dl"]/table/tbody/tr')
            index = None
            for i, label in enumerate(labels, 1):
                if self.chosen_quality in label.text:
                    index = i
                    break
            if index is not None:
                element = self.chrome_driver.find_element_by_xpath(
                    F'//*[@id="watch_dl"]/table/tbody/tr[{index}]/td[4]/a[1]')
            else:
                element = self.chrome_driver.find_element_by_css_selector(
                    F'#watch_dl > table > tbody > tr > td.tar > a.nop.btn.g.dl._open_window')

            self.chrome_driver.get(self.base_url + element.get_attribute("data-url")[1:])
        except Exception as e:
            print(e)
            try:
                _ = self.chrome_driver.find_elements_by_class_name('msg_box.error.table.full')[0]
                print("There are no available download links !")
            except Exception as e:
                raise NotImplementedError("Some changes were made to EgyBest website please check for an update")
            self.exit()

    def get_user_download_choice(self, file_name):
        while 1:
            cprint(f"\n--->Links saved to {file_name.replace('//', '/')}", "blue")
            choice = self.get_string_input(
                "--->Do you want to start [d]ownloading ,[a]ppend to IDM or [q]uit?,"
                "chose: (d/a/q)")
            # if choice == "v":
            #     self.append_to_vlc()
            if choice == "d":
                self.start_downloading()
            elif choice == "a":
                self.append_to_idm()
            elif choice == "p":
                print("\n".join(self.downloadable_episodes_url_list))
            elif choice == "q":
                break
            else:
                print("None valid option !")

    def start_downloading(self):
        print("Note : if you're using pycharm console, it might not show you the progress bar !")
        if not self.downloadable_episodes_url_list:
            print("Array is empty")
        for i, ep_link in enumerate(self.downloadable_episodes_url_list):
            print("Starting to download :", ep_link)
            obj = SmartDL(ep_link, "./Downloads" + os.sep)
            obj.start()
            print("Download location :" + obj.get_dest())

    def append_to_idm(self):
        for i, ep_link in enumerate(self.downloadable_episodes_url_list):
            try:
                os.system(
                    F'"C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe" /d {ep_link} /n /a')
                print("+1 :", ep_link)
            except Exception as excep:
                print(F"Couldn't add {self.chosen_episodes_url_list[i]} \nException :{excep}")

    def save_links_to_file(self) -> str:
        # ToDo : Change the download folder to conf file
        base_dic = "LinkSaves/"
        os.makedirs(os.path.dirname(base_dic), exist_ok=True)
        file_name = F"{base_dic}/{self.content_type}-{self.content_name}.txt"
        with open(file_name, "w") as f:
            for ep in self.downloadable_episodes_url_list:
                f.write(F"{ep}\n")
        return file_name

    def reset_chrome_driver(self):
        self.destroy_chrome_driver()
        self.init_chrome_driver()

    def append_to_vlc(self):
        for i, ep_link in enumerate(self.downloadable_episodes_url_list):
            try:
                cmd = F'"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe" --playlist-enqueue "{ep_link}"'
                # print(cmd)
                os.system(F'cmd /c "{cmd}"')
                # print("done")
            except Exception as excep:
                print(F"Couldn't add {self.chosen_episodes_url_list[i]} \nException :{excep}")
