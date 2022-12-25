# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 21:57:06 2022

@author: RGPeart
"""


### scrap hotel.com    https://fr.hotels.com/


##df_hotel : nom ,note, nombre étoile, prix, address, localisation, link


import time
import datetime
import re
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import commonFunctions

monthCorrespondances = {
    "01": "january",
    "02": "february",
    "03": "march",
    "04": "april",
    "05": "may",
    "06": "june",
    "07": "july",
    "08": "august",
    "09": "september",
    "10": "october",
    "11": "november",
    "12": "december",
}

# éléments de recherche

city = "New York"
date_set = "06-11-2023"
current_date = datetime.date.today()
set_adults = "2"
set_kids = "2"
chambre = "1"

date_day, date_month, date_year = commonFunctions.separateAmericanDate(date_set)
if len(str(date_month)) == 2:
    month = monthCorrespondances.get(str(date_month))
else:
    month = monthCorrespondances.get("0" + str(date_month))
date_month_year = month + " " + str(date_year)
next_day = int(date_day) + 1
date_end_set = str(date_month)+"-"+str(next_day)+"-"+str(date_year)

if len(str(current_date.month)) == 2:
    month = monthCorrespondances.get(str(current_date.month))
else:
    month = monthCorrespondances.get("0" + str(current_date.month))
current_date_month_year = month + " " + str(current_date.year)

# ouverture de la page
driver = webdriver.Firefox()
driver.get("https://fr.hotels.com/")
time.sleep(5)

# accepting cookies
driver.find_element(by="xpath",
                    value="//button[@class='osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept']").click()
time.sleep(5)

# configuration de la recherche

driver.find_element(by="xpath", value="//div[@class='uitk-field has-floatedLabel-label has-no-placeholder']").click()

time.sleep(5)
search_dest = driver.find_element(by="id", value="location-field-destination")
dest = search_dest.send_keys(city, Keys.ENTER)
time.sleep(5)

driver.find_element(by="id", value="d1-btn").click()
time.sleep(2)

date_text = driver.find_element(by="xpath", value="//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text
button_list = driver.find_elements(by="xpath",
                                   value="//button[@class='uitk-button uitk-button-medium uitk-button-only-icon uitk-layout-flex-item uitk-button-paging']")

while date_text != current_date_month_year:
    button_list[0].click()
    date_text = driver.find_element(by="xpath",
                                    value="//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text



while date_text != date_month_year:
    button_list[1].click()
    date_text = driver.find_element(by="xpath",
                                    value="//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text


select_date = driver.find_element(by="xpath", value="//button[@data-day='11']").click()

driver.find_element(by="xpath",
                    value="//button[@class='uitk-button uitk-button-medium uitk-button-has-text uitk-button-primary uitk-layout-flex-item uitk-layout-flex-item-flex-shrink-0 dialog-done']").click()

driver.find_element(by="xpath", value="//button[@aria-label='1 chambre, 2 pers.']").click()

adult = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")
kid = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

btn = driver.find_elements(by="xpath", value="//button[@class='uitk-layout-flex-item uitk-step-input-touch-target']")

while adult != "1":
    btn[0].click()
    adult = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")

while adult < set_adults:
    btn[1].click()
    adult = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")

while kid != "0":
    btn[2].click()
    kid = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

while kid < set_kids:
    btn[3].click()
    kid = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

if set_kids == "2":
    select_element = driver.find_element(by="id", value='child-age-input-0-0')
    select_object = Select(select_element)
    select_object.select_by_index(10)
    select_element = driver.find_element(by="id", value='child-age-input-0-1')
    select_object = Select(select_element)
    select_object.select_by_index(5)

driver.find_element(by="xpath",
                             value="//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary uitk-button-floating-full-width']").click()

# rechercher
driver.find_element(by="xpath",
                    value="//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary']").click()
time.sleep(15)


# Scrap

i = 0

while i < 10:
    more = driver.find_element(by="xpath", value="//button[@data-stid='show-more-results']")
    driver.execute_script("arguments[0].click();", more)
    time.sleep(3)
    i += 1

for i in range(20):
    driver.find_element(by="css selector", value="body").send_keys(Keys.PAGE_DOWN)

link_list = driver.find_elements(by="xpath", value="//a[@class = 'listing__link uitk-card-link']")

prices = list(map(lambda price: price.text, driver.find_elements(by="xpath",
                                                                 value="//div[contains(@class, 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')]")))


# grade = list(map(lambda note: note.text, driver.find_elements(by="xpath", value="//span[contains(@class, 'uitk-type-300 uitk-type-bold all-r-padding-one')]")))
# print(grade)
# print(len(grade))

name = list(map(lambda hotel: hotel.text, driver.find_elements(by="xpath",
                                                               value="//h3[contains(@class, 'uitk-heading-5 truncate-lines-2 all-b-padding-half pwa-theme--grey-900 uitk-type-heading-500')]")))


links = list(map(lambda hotel_link: hotel_link.get_attribute("href"),
                 driver.find_elements(by="xpath", value="//a[contains(@class, 'listing__link uitk-card-link')]")))


address = []
stars = []
localisation = []
grade = []
start_date = []
end_date = []
nb_adult = []
nb_kid = []
nb_chambre = []

print(len(name))

for link in link_list:
    print(link_list.index(link))

    driver.execute_script("arguments[0].click();", link)

    driver.implicitly_wait(20)

    # Changer de fenêtre

    driver.switch_to.window(driver.window_handles[1])

    # Scrap name, address, stars

    address_hotel = driver.find_element(by="xpath",
                                        value="//div[@class='uitk-text uitk-type-300 uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width uitk-text-default-theme']").text

    grade_text = driver.find_element(by="xpath",
                                     value="//h3[@class='uitk-heading-5 uitk-spacing uitk-spacing-padding-blockend-three']").text
    grades_extraction = re.search('([0-9]+),([0-9]+)', grade_text)
    if grades_extraction == None:
        grades = None
    else:
        grades = grades_extraction.group(0)

    span_list = driver.find_elements(by="xpath", value="//span[@class='is-visually-hidden']")
    star_text = span_list[10].get_attribute("innerHTML")
    star = re.search('([0-9]+)\.([0-9]+)', star_text)
    if star == None:
        stars_hotel = '0'
    else:
        stars_hotel = star.group(0)

    # ajout aux listes

    grade.append(grades)
    address.append(address_hotel)
    stars.append(stars_hotel)
    start_date.append(date_set)
    end_date.append(date_end_set)
    nb_adult.append(set_adults)
    nb_kid.append(set_kids)
    nb_chambre.append(chambre)

    # on ferme l'onglet

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

localisation = list(
    map(lambda add: commonFunctions.getLocalisationFromAdd(add) if address is not None else np.nan, address))


df = pd.DataFrame(list(zip(name, grade, stars, prices, address, localisation, start_date, end_date, nb_adult, nb_kid, nb_chambre, links)),
                  columns=['name', 'grade','stars', 'prices','address', 'gps', 'start_date','end_date', 'nb_adult','nb_kid','nb_chambre', 'link' ])

# création du CSV

df.to_csv("csv/hotelsCom/hotelsCom_Juin2023_4.csv",index = False, sep=";")

