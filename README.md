# EgyBest Downloader (v 1.0)
Download a film or a Tv series from EgyBest without the annoying ads .
* Currently working on a Gui version 

## Important !!
The goal from this script is to gather download links and add them to Internet download manager (IDM) ,
but if you don't like using IDM or don't have it installed or activated(see below for solution ),
you'll find the downland links on a file in the "LinkSaves" folder so you can download it 
manually or by using the built in function

### Prerequisites
* Working version of IDM [Internet download manager](https://www.internetdownloadmanager.com/download.html)
 installed on the default directory .
```
C:\Program Files (x86)\Internet Download Manager
 ```
 or you can change it inside the code .
* To activate expired versions of IDM use [idm-trial-reset](https://github.com/J2TeaM/idm-trial-reset/releases/tag/v1.0.0) 
tool to reset the 30 days free trial .
* You'll need python installed on a windows machine .
* Latest version of google chrome (currently supporting chrome only).

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Installing

Clone the directory on your local machine  
```
git clone https://github.com/aymannc/EgyBest-Downloader
 ```
After cloning the project,install the "requirements.txt" on your virtualenv

```
pip install -r requirements.txt
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
