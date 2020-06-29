# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:06:51 2020

@author: vijaynchakole

https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d
"""
from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
import io
from PIL import Image
import hashlib
import requests

copy_img_url = []

# wd = webdriver.Chrome("C:\\Users\\hp\\Desktop\\chromedriver_win32\\chromedriver.exe") #incase you are chrome

#wd.get('https://google.com')

#search_box = wd.find_element_by_css_selector('input.gLFyf')
#search_box.send_keys('Dogs')
#wd.quit()


"""
folder_path = "C:\\Users\\hp\\Desktop\\Naaniz ML Internship" 
url = "https://miro.medium.com/max/2560/1*MzV56PC6o8gjEU9lyGuR1Q.jpeg"
image_content = requests.get(url).content
image_file = io.BytesIO(image_content)
image = Image.open(image_file).convert('RGB')
file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
with open(file_path, 'wb') as f:
    image.save(f, "JPEG", quality=85)

"""



# image scraping

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))
    global copy_img_url
    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results  (img.rg_ic)  # div.bRMDJf.islir
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd") #img.class_name
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb') #img.class_name
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
                    copy_img_url.append(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(1)
            load_more_button = wd.find_element_by_css_selector(".mye4qd") # or "div.YstHxe"
            if load_more_button: 
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls




def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        

    try:
       #image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")
        
        
        
def search_and_download(search_term:str,driver_path:str,target_path='./images',number_images=100):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
        
    #for elem in res:
     #   persist_image(target_folder,elem)
    
        


# image collection completed for ...
# "shrikhand", "thalipeeth", "vada pav", "Bisi Bele Bhaat", "kesari bath", "Mysore pak"
"""
categories = ["modak",Dharwad pedha,
              "Chiroti"]    

"""

categories = "kim jong un"
DRIVER_PATH = "C:\\Users\\hp\\Desktop\\chromedriver_win32\\chromedriver.exe"

#DRIVER_PATH = "C:\\Users\\hp\\Desktop\\Naaniz ML Internship\\chromedriver.exe"

search_and_download(categories , DRIVER_PATH)
        
len(copy_img_url)

fd = open("kim jong un.txt", "a+")

for url in copy_img_url :  
    fd.write(str(url))
    fd.write("\n")
    

copy_img_url = []

fd.write("hello world")
fd.write("\n")
fd.write("bye bye wolrd")

fd.close()


fd = open("putin.txt", "r")
text = fd.readlines()


len(text)
type(text)
text

target_path = "C:\\Users\\hp\\Desktop\\Naaniz ML Internship\\images"
search_term = "putin"

target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))
global copy_img_url

for elem in text :
    persist_image(target_folder,elem)
