import time
import numpy as np
import os
import json
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tensorflow.keras.models import load_model
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

my_url = "https://1xbet.com/en/allgamesentrance/crash/"
model = load_model('model5.h5')

"""
from requests_html import HTMLSession

session = HTMLSession()
r = session.get(my_url)

r.html.render()
container = r.html.find('#xgames-crash')
l = container.find('div')
print(list)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0]<200 or pixdata[x, y][1]<200 or pixdata[x, y][2]<200  :
                pixdata[x, y] = (0, 0, 0, 255)
"""


def standard(get_img):
    pixdata = get_img.load()
    for y in range(get_img.size[1]):
        for x in range(get_img.size[0]):
            if pixdata[x, y][0] < 200 or pixdata[x, y][1] < 200 or pixdata[x, y][2] < 200:
                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)
    img_array = np.array(get_img)
    new_array = []
    for a in range(80):
        new_array.append([])
        for j in range(260):
            if (img_array[a][j] == np.array([255, 255, 255, 255])).all():
                new_array[a].append(1)

            else:
                new_array[a].append(0)
    return new_array


def standard1(get_img):
    img_array = np.array(get_img)
    new_array = []
    for a in range(80):
        new_array.append([])
        for j in range(260):
            if (img_array[a][j] == np.array([255, 255, 255, 255])).all():
                new_array[a].append(1)

            else:
                new_array[a].append(0)
    return new_array


blank = model.predict(x=np.array([standard1(Image.open("blank.png"))]))

options = webdriver.ChromeOptions()
options.headless = True
serv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=serv, options=options)
driver.get(my_url)
driver.set_window_size(2000, 2000)

container = driver.find_element(By.CLASS_NAME, "crash-game__wrap")
path = 'screen_shot.png'

timer = driver.find_element(By.CLASS_NAME, "crash-timer__counter")

'''
while True:
    container.screenshot(path)
    img_notCropped = Image.open(path)
    img = img_notCropped.crop((850,320,1110,400))

    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0]<200 or pixdata[x, y][1]<200 or pixdata[x, y][2]<200  :
                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)

    counter += 1
    s="test"+str(counter)+".png"
    img.save("train1/"+s)
    time.sleep(0.5)
'''

old_prediction = np.array([[]])
results={}
save_timer = time.time()
try:
    while True:
        if time.time() - save_timer > 900:
            with open('data.txt', 'w') as outfile:
                json.dump(results, outfile)
            save_timer = time.time()
            print("saved")
        if timer.text == "1":
            while True:
                container.screenshot(path)
                img_notCropped = Image.open(path)
                img = img_notCropped.crop((850, 320, 1110, 400))
                prediction = model.predict(x=np.array([standard(img)]))
                if prediction == old_prediction and prediction != blank:
                    #i = int(prediction[0][0] + 0.5)

                    # if i in results.keys():
                    #     results[i] = results[i] + 1
                    # else:
                    #     results[i] = 1

                    i = float(str(prediction[0][0])[:3])
                    for j in range(16):
                        a = 1 + j/10
                        if i >= a:
                            if a in results.keys():
                                results[a] = results[a] + 1
                            else:
                                results[a] = 1

                    print(results)
                    break
                else:
                    old_prediction = prediction
                time.sleep(0.1)
        time.sleep(0.5)
except KeyboardInterrupt:
    print ('KeyboardInterrupt exception is caught')
    with open('data.txt', 'w') as outfile:
        json.dump(results, outfile)