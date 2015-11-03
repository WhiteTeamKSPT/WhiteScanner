__author__ = 'pitochka'

import requests
import os
from time import sleep

__SERVER__ = 'whiteteam.cloudapp.com'
__TASKS__  = '/worker/tasks'
__IMAGES__ = '/worker/download'
__UPLOADS__ = '/home/pitochka/server/Input'

class getTask():
    def get(self):
        while True:
            self.info = requests.get(str(__SERVER__) + str(__TASKS__))
            if not self.info:
                sleep(15)
            else:
                print 'task recived'
                self.listinfo = self.info.json()
                print self.listinfo

                user = self.listinfo["user"]
                set = self.listinfo["set"]
                size = self.listinfo["size"]

class getImages():
    def get(self, user, set, size):
        if not os.path.isdir(os.path.join(__UPLOADS__, user)):
            os.makedirs(user)
        setPath=os.path.join(__UPLOADS__,user,str(set))
        if not os.path.isdir(setPath):
            os.makedirs(setPath)
        # Дальше создаю каталог для пользователя, если не создан, заливаю туда фотки и вызываю сфм
        # класс для вызова СФМ в startSFM.py, из main.py все вызывается