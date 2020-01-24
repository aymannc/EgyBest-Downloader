import os
import sys

import requests
from bs4 import BeautifulSoup
from pySmartDL import SmartDL
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class EgyBest:
    search_base_url = "https://nero.egybest.site/explore/?q="
    chrome_driver = None

    def __init__(self):
        self.search_url = None
        self.content_url = None
        self.content_type = None
        self.content_name = None
        self.chosen_seasons_numbers_list = []
        self.chosen_seasons_url_list = []
        self.chosen_episodes_number_list = []
        self.chosen_episodes_url_list = []
        self.downloadable_episodes_url_list = []

    def reset(self):
        self.__init__()

    def get_search_url(self):
        try:
            self.search_url = self.search_base_url + \
                              self.get_string_input("What are you searching for ? :")
            # print(self.search_url)
        except:
            exit("search url")

    # function to get the download content
    def get_content_url(self):
        print("Searching for results !!!")
        res = self.get_bs4_result(self.search_url, "a", "movie")
        # Displaying the fitched linked
        for i, link in enumerate(res, 1):
            content_type = None
            try:
                content_type = self.get_url_type(link['href']).upper()
                print(i, " ->", link.contents[4].text, ", Type : ", content_type, ",", "IMDB Rating :",
                      link.contents[0].i.i.text,'\n')
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
        if not self.chrome_driver:
            print("Initializing chrome driver")
            try:
                caps = DesiredCapabilities().CHROME
                caps["pageLoadStrategy"] = "eager"
                chrome_options = webdriver.ChromeOptions()
                # chrome_options.add_argument('--log-level=3')
                # chrome_options.add_argument('--disable-logging')
                # chrome_options.add_argument('--headless')
                self.chrome_driver = webdriver.Chrome(executable_path="./Driver/chromedriver.exe",
                                                      options=chrome_options)
            except:
                print("Couldn't init chrome drivers")
                self.exit("init_chrome")

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

    def gather_download_link(self):
        self.init_chrome_driver()
        print("Accessing EgyBest page")
        self.chrome_driver.get(self.chosen_episodes_url_list[-1])
        self.chose_quality()
        print("Accessing the download page")
        self.chrome_driver.close()
        self.chrome_driver.switch_to.window(
            self.chrome_driver.window_handles[0])
        while 1:
            try:
                target_button = self.chrome_driver.find_element_by_xpath(
                    "/html/body/div[1]/div/p[2]/a[1]")
                if not target_button.get_attribute("href"):
                    print("Closing ads tab")
                    target_button.click()
                    self.chrome_driver.switch_to.window(
                        self.chrome_driver.window_handles[1])
                    self.chrome_driver.close()
                    self.chrome_driver.switch_to.window(
                        self.chrome_driver.window_handles[0])
                else:
                    print("Obtaining the download link")
                    url = target_button.get_attribute("href")
                    if url:
                        self.downloadable_episodes_url_list.append(url)
                        return
            except Exception as e:
                print(e)
                self.chrome_driver.switch_to.window(
                    self.chrome_driver.window_handles[0])

    def download_seasons(self, url=None):
        if url is None:
            url = self.content_url
        res = self.get_bs4_result(url, "div", "movies_small")[0]
        seasons_list = res.find_all("a")
        number_of_seasons = len(seasons_list)
        all_eps = False
        while number_of_seasons:
            print(F"There're {number_of_seasons} seasons ")
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

    def start(self, link=None):
        # Check if link provided is valid
        valid_link = False
        if link:
            self.content_type = self.get_url_type(link)
            if self.content_type:
                valid_link = True
        # if it's valid it wont enter the loop
        while not self.content_type:
            # shows that the link is trash
            if link:
                print("None valid link")
            # getting user input
            self.get_search_url()
            self.get_content_url()
        self.content_name = self.get_content_name(self.content_url if not valid_link else link)
        if self.content_type == "series":
            self.download_seasons()
        elif self.content_type == "movie":
            self.chosen_episodes_url_list.append(self.content_url if not valid_link else link)
            # print(self.chosen_episodes_url_list)
            self.gather_download_link()

        self.save_links_to_file()
        self.get_user_download_choice()

    @staticmethod
    def get_int_input(output_msg):
        try:
            return int(input(output_msg))
        except:
            return None

    @staticmethod
    def get_string_input(output_msg):
        try:
            return str(input(output_msg)).lower()
        except:
            exit("strig input")

    @staticmethod
    def get_bs4_result(url, html_tag, class_name):
        print("Requesting link !")
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.find_all(html_tag, class_=class_name)

    @staticmethod
    def get_url_type(url):
        # print(url)
        try:
            return url.split("/")[3]
        except:
            print("None valid link in get_url_type")
        return None

    @staticmethod
    def get_content_name(url):
        # print(url)
        try:
            return url.split("/")[4]
        except:
            print("None valid link in get_content_name")
        return None

    def exit(self, code):

        self.destroy_chrome_driver()
        sys.exit("\n Exited " + code)

    def chose_quality(self):
        target_button = self.chrome_driver.find_elements_by_class_name(
            'btn.g.dl.nop._open_window')[0]
        target_button.click()

    def get_user_download_choice(self):
        while 1:
            choice = self.get_string_input(
                "---> Links saved to file , Do you want to start [d]ownloading ,[a]ppend to IDM or [q]uit?,"
                "chose: (d/a/q)")
            if choice == "d":
                self.start_downloading()
                break
            if choice == "a":
                self.append_to_idm()
                break
            if choice == "q":
                break
            print("None valid option !")

    def start_downloading(self):
        print("Note : if your're using pycharm console, it won't show you progress bar !")
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
        print("Saving them to a file !")

    def save_links_to_file(self):
        base_dic = "LinkSaves/"
        os.makedirs(os.path.dirname(base_dic), exist_ok=True)
        # print(self.downloadable_episodes_url_list)
        with open(F"{base_dic}/{self.content_type}-{self.content_name}.txt", "w+") as f:
            for ep in self.downloadable_episodes_url_list:
                f.write(F"{ep}\n")

    def reset_chrome_driver(self):
        self.destroy_chrome_driver()
        self.init_chrome_driver()


if __name__ == "__main__":
    egy = EgyBest()
    link = "https://nero.egybest.site/movie/joker-2019/"
    try:
        while 1:
            egy.start()
            try:
                choice = egy.get_int_input("Do you want to restart ? : (1/0)")
                if choice == 0:
                    break
                egy.reset()
            except:
                break
    except Exception as e:
        egy.reset_chrome_driver()
        print(e)
    finally:
        egy.destroy_chrome_driver()
