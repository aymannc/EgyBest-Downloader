
from Core.appConfigurator import get_string_input
def start(self, link=None):
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
            get_search_url(self)
            get_content_url(self)
        self.content_name = self.get_content_name(self.content_url if not valid_link else link)
        if self.content_type == "series":
            self.download_seasons()
        elif self.content_type == "movie":
            self.chosen_episodes_url_list.append(self.content_url if not valid_link else link)
            # print(self.chosen_episodes_url_list)
            self.gather_download_link()

        self.save_links_to_file()
        self.get_user_download_choice()


def get_search_url(self):
        try:
            self.search_url = self.search_base_url + \
                              get_string_input("What are you searching for ? :")
            # print(self.search_url)
        except:
            exit("search url")

    # function to get the download content
def get_content_url(self):
        print("Searching for results !!!")
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