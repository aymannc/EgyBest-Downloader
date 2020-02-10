# EgyBest Downloader (v 1.0.2)
<p align="center">
  <img src="https://lh3.googleusercontent._com/M9p9EOCX0Hi0EjHwvfFa34mPjIZmpAc2LLqSbW3I-4jnQCGnolHMo1uncSJuG12cQg" height="100" title="EgyBest logo">
</p>

Try to download `Supernatural` with its 316 episodes from EgyBest or any website, that's a lot of clicks and ads :( .

**EgyBest Downloader** gives you the possibility to download any movie or a Tv series from 
EgyBest without the annoying ads .
* ***Currently working on a Gui version*** 
## What's new 
* (v 1.0.2) : updating the search and ad closing algorithm, adding `Chose quality` option . 

* (v 1.1.0 ) :Soon,adding vlc online streaming option ,chose eps by range ,Jupiter lab for better visualisation 
and a beginners friendly demo for installing and running the code. 
## Important !!
* The goal from this programme is to gather download links for you .
* You'll find the downloads link on a local file with the following format `type-name-year.txt`  in the "LinkSaves" folder.

* You can add the links automatically to Internet download manager (IDM) and download them ,but if you don't like using 
IDM or don't have it installed or activated(see Prerequisites for a solution),
you can use the built in command line downloader or you can copy all the links and use `add batch download from clipboard` 
on your favorite download manager .

.
## Prerequisites
* To activate expired versions of IDM use [idm-trial-reset](https://github.com/J2TeaM/idm-trial-reset/releases/tag/v1.0.0) 
tool to reset the 30 days free trial .

* For the IDM functionalities you'll need IDM [Internet download manager](https://www.internetdownloadmanager.com/download.html)
 installed on the default directory .
```
C:\Program Files (x86)\Internet Download Manager
 ```
 or you can change the path inside the code .

* You'll need python installed on a windows machine .
* Latest version of google chrome (currently supporting chrome only).

## Installing

Clone the directory on your local machine  
```
git clone https://github.com/aymannc/EgyBest-Downloader
 ```
After cloning the project,install the "requirements.txt" on your virtualenv

```
pip install -r requirements.txt
```
## Running the programme
* Open the cmd on the containing folder and use 
```
(myenv) D:\EgyBest_1.0> python egybest.py
```
## Built With

* [Beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - Python library designed for quick turnaround projects like screen-scraping
* [Selenium](https://selenium.dev/) - It's library used for browser automation
* [pySmartDL](https://github.com/iTaybb/pySmartDL) - It's a python download manager

## Authors

* **Nait Cherif Ayman**- [aymannc](https://github.com/aymannc)

## License

This project is licensed under the MIT License 

## Acknowledgments

* Thank you EgyBest for the hard work you provide

## Q & A

soon
