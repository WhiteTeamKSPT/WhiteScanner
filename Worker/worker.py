__author__ = 'pitochka'

import requests
import os
from time import sleep

__SERVER__ = 'http://whiteteam.cloudapp.net:8080'
__TASKS__  = '/worker/tasks'
__IMAGES__ = '/worker/download'
__MODELS__ = '/worler/upload/'
__DOWNLOADS__ = '/home/pitochka/server/Input'
__UPLOADS__ = '/home/pitochka/server/Output/'


class getTask():
    def __init__(self):
        pass

    def __call__(self):
        while True:
            print __SERVER__ + __TASKS__
            self.info = requests.get(__SERVER__ + __TASKS__)
            if not self.info:
                print 'waiting...'
                sleep(15)
            else:
                print 'task recived'
                self.listinfo = self.info.json()
                print self.listinfo

                user = self.listinfo["user"]
                set = self.listinfo["set"]
                size = self.listinfo["size"]
                print user, set, size

class getImages():
    def __init__(self):
        pass

    def __call__(self, user, set, size):
        setPath = os.path.join(__DOWNLOADS__, user)
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

        setPath=os.path.join(setPath, str(set))
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

class loadModel():
    def __init__(self, user, set, filename):
        self.user = user + '/'
        self.set = set + '/'
        self.filename = filename

    def __call__(self):
        print __UPLOADS__ + self.user + self.set + 'model.nvm'
        print __SERVER__ + __MODELS__ + self.user + self.set
        files = {'model.nvm': open(__UPLOADS__ + self.user + self.set + 'model.nvm', 'rb')}
        r = requests.post(__SERVER__ + __MODELS__ + self.user + self.set, files=files)
        print'done.'