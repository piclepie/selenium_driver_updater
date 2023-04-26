import requests
import re
import io
import zipfile
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup



def return_version_need(searchKey):
    # take parameter current_chrome_version. first 3 part
    downloadpage = "https://chromedriver.chromium.org/downloads"
    s = requests.Session()
    resposne = s.get(downloadpage)
    soup= BeautifulSoup(resposne.text,"html.parser")
    # a = soup.find(attrs={'href': 'https://chromedriver.storage.googleapis.com/index.html?path=110.0.5481.77/'})
    links = soup.find_all('a', href=lambda href: href and searchKey in href)[0] # type: ignore
    version_string = links.string.strip() # -> ChromeDriver 110.0.5481.77
    match = re.search(r' (\d+\.\d+\.\d+\.\d+)',version_string)
    if match:
        version_need = match.group(1)  #-> 110.0.5481.77
        print(version_need)
        return version_need
    else:
        return 0


def update_chromium_driver(version_need):
    """
       UPDATE Chromium driver update if erroe occured.
       Accept new version number
       download zip
       unzip
       delete old folder
       replace new driver
    """
    link = f'https://chromedriver.storage.googleapis.com/{version_need}/chromedriver_win32.zip'
    print(link)
    s = requests.Session()
    resposne = s.get(link)
    if resposne.status_code == 200:
        # request successful! 
        zip_file = io.BytesIO(resposne.content)
        with zipfile.ZipFile(zip_file,"r") as z:
            path = os.path.join(os.path.expanduser("~"),"Desktop","chromedriver_win32")
            try:
                #remove old file first
                shutil.rmtree(path)
                #remove folder then
                z.extractall(path)
                print("updated!")
            except:
                raise OSError('system error')
def main():
    path = os.path.join(os.path.expanduser("~"),"Desktop","chromedriver_win32\\chromedriver.exe")
    svs = Service(path)
    options_dvr = webdriver.ChromeOptions()
    options_dvr.add_argument('headless')
    try: 
        return webdriver.Chrome(service=svs, options=options_dvr) 
    except WebDriverException as e: # work on python 3.x
        msg = str(e)
        match = re.search(r' (\d+\.\d+\.\d+\.\d+)',msg)
        if match:
            print("Version Error. Needs a update")
            current_version = match.group(1)
            forsearch_current_version = ".".join(current_version.split(".")[:3])
            print(forsearch_current_version)
            version_need = return_version_need(forsearch_current_version)
            # download
            update_chromium_driver(version_need)
            return webdriver.Chrome(service=svs, options=options_dvr) 
        else:
            print("no new version found!")
            return 0


if __name__ == "__main__":
    main()

