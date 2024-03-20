from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import getcwd, _exit
from sys import exit

def search(city='', neighborhood='', propertyGroup='', property='', roomsRatio='', priceRatio='', floor=''):
    try:
        user_options = Options()
        user_options.add_argument('--ignore-certificate-errors')
        user_options.add_argument('--ignore-ssl-errors')
        user_options.add_argument('--start-maximized')
        user_options.add_experimental_option("detach", True)
        link = 'https://www.yad2.co.il/realestate/rent?topArea=2&area=1&city=%s&neighborhood=%s&propertyGroup=%s&property=%s&rooms=%s&price=%s&floor=%s' %(city,neighborhood,propertyGroup,property,roomsRatio,priceRatio,floor)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=user_options)

        driver.get(link)
        #driver.maximize_window()
        #print('starting wait')
        #WebDriverWait(driver, 50).until(
        #    EC.presence_of_element_located((By.CLASS_NAME, 'feeditem table'))
        #)
        time.sleep(10)
        WebDriverWait(driver, 20).until(
            EC.url_contains('rent')
        )
        items = driver.find_elements(By.XPATH, "//*[@class='feeditem table']")
        print(len(items))
        properties = {}
        for item, i in zip(items, range(len(items))):
            item.click()
            driver.switch_to.window(driver.window_handles[1])
            text = driver.find_elements(By.XPATH, "//*[@data-testid='building-text']")
            values = driver.find_elements(By.XPATH, "//*[@class='building-item_itemValue__foth7']")
            address = driver.find_element(By.XPATH, "//*[@class='heading_heading__GHOZO']").get_attribute('innerHTML')
            rooms = text[0].get_attribute('innerHTML')
            floor = values[1].get_attribute('innerHTML')
            try:
                size = text[2].get_attribute('innerHTML')
            except:
                size = text[1].get_attribute('innerHTML')
            price = driver.find_element(By.XPATH, "//*[@data-testid='price']").get_attribute('innerHTML')
            description = driver.find_element(By.XPATH, "//*[@class='description_description__zFgQ8']").get_attribute('innerHTML')
            assets = {
                "Elevator" : False, "Disability" : False, "Tornado" : False, "Rav-Bariach" : False, "AC" : False, "Bars" : False, "Storage" : False, "Sun-Heated Boiler" : False, "Renovated" : False, "Shelter" : False, "Long-Range" : False, "Pets" : False, "Partners" : False
            }
            propertyAssets = driver.find_elements(By.XPATH, "//*[@data-testid='in-property-item']")
            for asset, key in zip(propertyAssets, assets.keys()):
                if not("disabled" in asset.get_attribute('class')):
                    assets[key] = True
            #print(len(assets), assets)
            #print('address = %s\nrooms = %s\nfloor = %s\nsize = %s\nprice = %s\ndescription = %s' %(address, rooms, floor, size, price, description))
            photos_elements = driver.find_elements(By.XPATH, "//*[@class='gallery-grid_gridItem___8kyD gallery-swiper_listItem__wXrFp']")
            photos = []
            videos = []
            for photo_element in photos_elements:
                try:
                    photos.append(photo_element.find_element(By.XPATH, ".//*[@data-testid='image']").get_attribute('srcset').split(', ')[-1].split('?')[0])
                except:
                    videos.append(photo_element.find_element(By.XPATH, ".//*[@class='cover-video_video__5h_F2']").get_attribute('src'))
            properties[i] = {"address" : address, "rooms" : rooms, "floor" : floor, "size" : size, "price" : price, "description" : description, "assets" : assets, "videos" : videos, "photos" : photos}
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        #time.sleep(3)
        
    except KeyboardInterrupt:
        print('Interrupted')
        driver.quit()
        try:
            exit(130)
        except SystemExit:
            _exit(130)




    driver.quit()
    return properties

def make_message():
    f = open("format.txt", "r", encoding="utf-8")
    format = f.read()
    f.close()
    print(format)
    properties = search('5000', '1520', 'apartments', '1', '4-5', '9000-10000')
    dict = {}
    assets = []
    for i in properties:
        for asset in properties[i]["assets"]:
            if properties[i]["assets"][asset]:
                print(asset)
                assets.append(asset)
        text = format %(properties[i]["address"], properties[i]["price"], properties[i]["rooms"], properties[i]["size"], properties[i]["floor"], properties[i]["description"], properties[i]["assets"])
        dict[i] = {"videos" : properties[i]["videos"], "photos" : properties[i]["photos"], "desc" : text}
    print(dict)
    return dict
        


if __name__ == '__main__':
    make_message()

"""
use all of the pip installs bellow to run
pip install selenium
pip install webdriver-manager
"""