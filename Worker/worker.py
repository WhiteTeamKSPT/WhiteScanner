__author__ = 'pitochka'


import requests
from time import sleep
__SERVER__ = 'whiteteam.cloudapp.com'
__TASKS__  = '/worker/tasks'

class getTask():
    def get(self):
        while True
            self.info = requests.get(str(__SERVER__) + ' ' + str(__TASKS__))
            if not self.info:
                sleep(15)
            else:
                # здесь буду получать изображения

