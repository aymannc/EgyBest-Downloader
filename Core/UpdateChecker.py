import requests
from bs4 import BeautifulSoup
from termcolor import cprint

def check_for_updates(version):
    cprint('\nlooking for updates ,please wait !',"yellow")
    github_url = 'https://github.com/hamzaubi/EgyBest-Downloader'
    r = requests.get(github_url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        github_version = soup.select_one("#readme > div.Box-body > article > h1").text.split('v')[1][1:-1]
        if github_version != version:
            raise Exception(F"You have version {version} of the code please update to {github_version}!")
        else:
            cprint('\nApplication is up to date',"green")
    except Exception as e:
        exit(e)
