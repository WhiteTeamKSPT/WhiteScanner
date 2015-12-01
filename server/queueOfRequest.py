__author__ = 'ann'
import os
import json
#Очередь заявок клиентов
class QueueOfRequest:
    def __init__(self):
        self.queue = []
    #Добавление новой заявки. Указывается клиент, номер набора, количество фото в наборе
    def put(self,user,set):
        list=[]
        path=os.path.join(user,set)
        files = os.listdir(path)
        sizeOfPath=len(files)
        for req in self.queue:
            if(req['user']==user and req['set']==set):
                if(req['size']==sizeOfPath):
                    return
                else:
                    self.queue.remove(req)
                    break
        for i in files:
            list.append(os.path.join(os.path.abspath(os.curdir),path,i))
        self.queue.append({'user': user, 'set': set,'size':sizeOfPath,'list':list})
    #Получение самой старой заявки или пустого списка, если очередь пуста
    def lastRequest(self):
        if (len(self.queue)==0):
            return {}
        return json.dumps(self.queue[0])