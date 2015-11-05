__author__ = 'ann'
import queue
import os
#Очередь заявок клиентов
class QueueOfRequest:
    def __init__(self,path):
        self.queue = []
        self.path=path
    #Добавление новой заявки. Указывается клиент, номер набора, количество фото в наборе
    def put(self,user,set):
        list=[];
        path=os.path.join(self.path,user,set)
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
            list.append(os.path.join(self.path,user,set,i))
        self.queue.append({'user': user, 'set': set,'size':sizeOfPath,'list':list})

