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
__DOWNLOADSPATH__ = '/home/pitochka/server/Input/'
__UPLOADSPATH__ = '/home/pitochka/server/Output/'


class getTask():
    def __init__(self):
        pass

    def __call__(self):
        while True:
            url =  __SERVER__ + __TASKS__
            info = requests.post(url)
            if not info.status_code == 200:
                print 'waiting...'
                sleep(15)
            else:
                print 'task recived'
                data = json.loads(info.text)
                #print data
                user = data["user"]
                set = data["set"]
                size = data["size"]
                print user, set, size
                a = getImages()
                a(user, set, size)

class getImages():
    def __init__(self):
        pass

    def __call__(self, user, set, size):
        setPath = os.path.join(__DOWNLOADSPATH__, user)
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

        setPath=os.path.join(setPath, str(set))
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

        print setPath
        for i in range(1, size + 1):
            url = __SERVER__ + __DOWNLOADIMAGES__ + user + '/' + str(set) + '/' + str(i) + '/'
            print url
            img = requests.get(url, stream = True)
            if not img.status_code == 200:
                print "error: can not download images"
                break
            else:
                img_file = os.path.join(setPath, str(i) + '.jpg')
                with open(img_file, 'wb') as f:
                    for chunk in img_file:
                        f.write(chunk)
        print 'download completed'

class loadModel():
    def __init__(self, user, set, filename):
        self.user = user + '/'
        self.set = set + '/'
        self.filename = filename

    def __call__(self):
        print __UPLOADSPATH__ + self.user + self.set + 'model.nvm'
        print __SERVER__ + __UPLOADMODELS__ + self.user + self.set
        files = {'model.nvm': open(__UPLOADSPATH__ + self.user + self.set + 'model.nvm', 'rb')}
        r = requests.post(__SERVER__ + __UPLOADMODELS__ + self.user + self.set, files=files)
        print'done.'