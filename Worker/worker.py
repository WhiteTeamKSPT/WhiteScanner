# coding=utf8
__author__ = 'pitochka'

import requests
import os
import json
import shutil
from time import sleep

__SERVER__ = 'http://whiteteam.cloudapp.net:8080'
__TASKS__  = '/worker/task/'
__DOWNLOADIMAGES__ = '/worker/download/'
__UPLOADMODELS__ = '/worler/upload/'
__DOWNLOADSPATH__ = '/home/pitochka/server/Input/' #Директория с фотками от клинтов
__UPLOADSPATH__ = '/home/pitochka/server/Output/'#С моделями


class getTask():
    def __init__(self):
        pass

    def __call__(self):
        while True:
            url =  __SERVER__ + __TASKS__
            info = requests.post(url) #Смотрим заявки
            if not info.status_code == 200:
                print ('waiting for server request...')
                sleep(15)
            else:
                data = json.loads(info.text)
                if(data):
                    print ('task recived')
                    #print data
                    user = data["user"]
                    set = data["set"]
                    size = data["size"]
                    print (user, set, size)
                    a = getImages()
                    a(user, set, size)
                else:
                    print ('waiting...')
                    sleep(15)
            #Для проверки выгрузки готовой модели
            print ('load...')
            b=loadModel("us","1","hass.obj")
            b()

class getImages(): # Загрузка фото
    def __init__(self):
        pass

    def __call__(self, user, set, size):
        setPath = os.path.join(__DOWNLOADSPATH__, user) # Пробираеммся к директории
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

        setPath=os.path.join(setPath, str(set))
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

        print (setPath)
        for i in range(1, size + 1): # качаем файлы
            url = __SERVER__ + __DOWNLOADIMAGES__ + user + '/' + str(set) + '/' + str(i) + '/'
            print (url)
            img = requests.get(url, stream = True)
            if not img.status_code == 200:
                print ("error: can not download images")
                break
            else:
                img_file = os.path.join(setPath, str(i) + '.jpg') # Вот тут и был косяк
                with open(img_file, 'wb') as f: # другие варики - здесь: http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
                    #for chunk in img_file:
                    f.write(img.content)
        print ('download completed')

class loadModel():
    def __init__(self, user, set, filename): #Загрузка модели на сервер, мб не работает
        self.user = user + '/'
        self.set = set + '/'
        self.filename = filename

    def __call__(self):
        print (__UPLOADSPATH__ + self.user + self.set + self.filename )
        print (__SERVER__ + __UPLOADMODELS__ + self.user + self.set)
        with open(__UPLOADSPATH__ + self.user + self.set + self.filename, 'rb') as f:
            try:
                image = f.read()
                r = requests.post(__SERVER__ + __UPLOADMODELS__ + self.user + self.set, data = image)
                print ('done.')
            except (IOError,FileNotFoundError):
                print("Not such file")