__author__ = 'pitochka'

import requests
import os
from time import sleep

__SERVER__ = 'http://whiteteam.cloudapp.com:8000'
__TASKS__  = '/worker/tasks'
__IMAGES__ = '/worker/download'
__UPLOADS__ = '/home/pitochka/server/Input'

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
        setPath = os.path.join(__UPLOADS__, user)
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

        setPath=os.path.join(setPath, str(set))
        if not os.path.isdir(setPath):
            os.makedirs(setPath)

