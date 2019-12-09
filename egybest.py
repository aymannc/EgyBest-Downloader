import os
import sys

import requests
from bs4 import BeautifulSoup
from pySmartDL import SmartDL
from selenium import webdriver


class EgyBest:
    search_base_url = "https://nero.egybest.site/explore/?q="
    chrome_driver = None

    def __init__(self):
        self.search_url = None
        self.content_url = None
        self.content_type = None
        self.chosen_seasons_numbers_list = []
        self.chosen_seasons_url_list = []

        self.chosen_episodes_number_list = []
        self.chosen_episodes_url_list = []
        self.downloadable_episodes_url_list = []

    def get_search_url(self):
        self.search_url = self.search_base_url + \
                          self.get_string_input("What are you searching for ? :")

    def get_content_url(self):
        print("Searching for results !!!")
        res = self.get_bs4_result(self.search_url, "a", "movie")

        for i, link in enumerate(res, 1):
            content_type = None
            try:
                content_type = self.get_url_type(link['href']).upper()
                print(i, " ->", link.contents[4].text, ", Type : ", content_type, ",", "IMDB Rating :",
                      link.contents[0].i.i.text)
            except:
                print(i, " ->", link.contents[2].text,
                      ", Type : ", content_type)
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
        self.content_type = self.get_url_type(self.content_url)

    def init_chrome_driver(self):
        print("Initializing chrome driver")
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('log-level=3')
            # chrome_options.add_argument('--headless')
            self.chrome_driver = webdriver.Chrome(options=chrome_options)
        except:
            print("Could't initialize chrome , make sure to install it !!")
            print(input("Hello"))
            sys.exit()

    def destroy_chrome_driver(self):
        try:
            self.chrome_driver.close()
        except Exception as e:
            print(e)

    def start_download(self, url,
                       option: "Get download link 0,Append to IDM 1" = 1) -> "Returns the url":

        self.chrome_driver.get(url)
        print("Accessing EgyBest page")
        target_button = self.chrome_driver.find_elements_by_class_name(
            'btn.g.dl.nop._open_window')[0]
        target_button.click()
        print("Accessing the download page")
        self.chrome_driver.close()
        self.chrome_driver.switch_to.window(
            self.chrome_driver.window_handles[0])
        target_button = self.chrome_driver.find_element_by_xpath(
            "/html/body/div[1]/div/p[2]/a[1]")
        while 1:
            target_button = self.chrome_driver.find_element_by_xpath(
                "/html/body/div[1]/div/p[2]/a[1]")
            try:
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
                    if option == 1:
                        result = os.system(
                            F'"C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe" /d {url} /n /a')
                        print("Couldn't add it" if result else "Added to IDM")
                    return url
            except Exception as e:
                print("Exception ", e)
                self.chrome_driver.switch_to.window(
                    self.chrome_driver.window_handles[0])

    def download_seasons(self, url=None):
        if url is None:
            url = self.content_url
        res = self.get_bs4_result(url, "div", "movies_small")[0]
        seasons_list = res.find_all("a")
        number_of_seasons = len(seasons_list)
        while number_of_seasons:
            print(F"There're {number_of_seasons} seasons ")
            choice = self.get_string_input(
                "Do you want to download all seasons or specific ones, type['all' or 'spec']:")
            if choice == 'all':
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
        for i in self.chosen_episodes_number_list.sort():
            self.chosen_seasons_url_list.append(seasons_list[i]['href'])

        print("Gathering episodes Urls")
        print("chosen_seasons_url_list", self.chosen_seasons_url_list)
        for url in self.chosen_seasons_url_list:
            res = self.get_bs4_result(url, "div", "movies_small")[0]
            episodes_list = res.find_all("a")
            number_of_eps = len(episodes_list)
            if number_of_eps:
                print(F"There're {number_of_eps} episodes ")
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
            print("Eps list", episodes_list)
            print("chosen Ep list", self.chosen_episodes_number_list)

            for i in self.chosen_episodes_number_list.sort():
                ep_link = episodes_list[i]["href"]
                self.downloadable_episodes_url_list.append(
                    self.start_download(ep_link))
                self.chosen_episodes_url_list.append(ep_link)
            print(self.downloadable_episodes_url_list)
            print(self.chosen_episodes_url_list)
        return True

    def start(self):
        while 1:
            while not self.content_type:
                self.get_search_url()
                self.get_content_url()
            if not self.chrome_driver:
                self.init_chrome_driver()
            if self.content_type == "series":
                self.download_seasons()
            elif self.content_type == "movie":

                result = self.start_download(self.content_url, option=0)
                if result:
                    print(result)
                    obj = SmartDL(result, "./Download")
                    obj.start()
                    print("Path to file :", obj.get_dest())
            try:
                choice = self.get_int_input("Do you want to restart ? : (1/0)")
                if not choice:
                    break
            except:
                break
        self.destroy_chrome_driver()

    @staticmethod
    def get_int_input(output_msg):
        try:
            return int(input(output_msg))
        except:
            return None

    @staticmethod
    def get_string_input(output_msg):
        return str(input(output_msg)).lower()

    @staticmethod
    def get_bs4_result(url, html_tag, class_name):
        print("Requesting link !")
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.find_all(html_tag, class_=class_name)

    @staticmethod
    def get_url_type(url):
        try:
            return url.split("/")[3]
        except:
            print("Couldn't found any results ")
        return None


if __name__ == "__main__":
    # TODO check if the IDM is installed and ask user for download option ,add threads
    egy = EgyBest()
    egy.start()
    egy.destroy_chrome_driver()
