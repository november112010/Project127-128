from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# WIKIPEDIA Bright STARS DATA URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

scarped_data = []



def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "new"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        scarped_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)


brown_dwarf_data_1= pd.read_csv("brown_dwarfs.csv")

for td in scarped_data:
    replaced = []
    for el in td: 
        el = el.replace("\n", "")
        replaced.append(el)
    scarped_data.append(replaced)

print(scarped_data)


headers = ["star_name","radius", "mass", "distance_data"]
new_dwarf_1 = pd.DataFrame(scarped_data,columns = headers)
new_dwarf_1.to_csv('brown_dwarfs.csv',index=True, index_label="id")
