from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("./chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink","planet_type","planet_radius","orbital_period","orbital_radius","eccentricity"]
planet_data = []
new_planet_data = []
def scrape():
    for i in range(1,428):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            current_page_no = int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if current_page_no<i :
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
                
            elif current_page_no>i :
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()

            else :
                 break
        for ul_tag in soup.find_all("ul",attrs={"class":"exoplanet"}) :
            li_tags = ul_tag.find_all("li") 
            tempList = []
            for index,li_tag in enumerate(li_tags):
                if index == 0 :
                    tempList.append(li_tag.find_all("a")[0].contents[0])
                else :
                    try:
                        tempList.append(li_tag.contents[0])
                    except:
                        tempList.append("")
            
            hyperlink_li_tag = li_tags[0]
            tempList.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(tempList)
        
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        tempList = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    tempList.append(td_tags.find_all("div",attr = {"class":"value"})[0].contents[0])
                except:
                    tempList.append("")

        new_planet_data.append(tempList)
                

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scrape()
for index,data in enumerate(planet_data):
    scrape_more_data(data[5])


final_planet_data =[]
for index,data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)

with open("scrapper_4.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)
