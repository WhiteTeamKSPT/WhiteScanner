__author__ = 'ann'
import queue
import os
#Очередь заявок клиентов
class QueueOfRequest:
    def __init__(self,path):
        self.queue = queue.Queue()
        self.path=path
    #Добавление новой заявки. Указывается клиент, номер набора, количество фото в наборе
    def put(self,user,set):
        path=os.path.join(self.path,user,set)
        files = os.listdir(path)
        sizeOfPath=len(files)
        self.queue.put({'user': user, 'set': set,'size':sizeOfPath})
    #Получение самой старой заявки или пустого списка, если очередь пуста
    def lastRequest(self):
        if self.queue.empty():
            return {}
        return self.queue.get()
    #Получение количества заявок
    def numberOfRequests(self):
        return self.queue.qsize()