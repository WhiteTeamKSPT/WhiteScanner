import tornado
import tornado.ioloop
import tornado.web
import os
import tornado.websocket
from queueOfRequest import QueueOfRequest
import json

__PORT__=8000
__FILENAME__='pid.txt'
__PATH_RES__='result'
readyModels=[]
__UPLOADS__ = os.path.abspath(os.curdir)
#Загрузка клиентом фотографии. Указывается клиент, номер набора, номер фотографии
class Upload(tornado.web.RequestHandler):
    def post(self,user,set,number):
        if not os.path.isdir(user):
            os.makedirs(user)
        setPath=os.path.join(user,str(set))
        if not os.path.isdir(setPath):
            os.makedirs(setPath)
        fname=os.path.join(setPath,str(number))
        with open(fname, 'wb') as file:
            try:
                file.write(self.request.body)
            except IOError:
                raise tornado.web.HTTPError(500,"Error in the received file")
#Добавление заявки на обработку. Указывается клиент, номер набора
class Finish(tornado.web.RequestHandler):
    def post(self,user,set):
        try:
            requests.put(user,set)
        except IOError:
            raise tornado.web.HTTPError(500,"No such client or set")
#Получение самой старой заявки, если заявки есть
class Task(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json")
        self.finish(requests.lastRequest())
class Table(tornado.web.RequestHandler):
    def get(self):
        self.render("table.html",title="Requests",header="Table of requests",listOfRequests=requests.queue)
#Запрос от воркера на загрузку фотографии. Указывается клиент, номер набора, номер фотографии
class Download(tornado.web.RequestHandler):
    def get(self,user,set,number):
        path=os.path.join(user,str(set),str(number))
        with open(path, 'rb') as file:
            try:
                image = file.read()
                self.finish(image)
                requests.get(user,set,number)
            except (IOError,FileNotFoundError):
                raise tornado.web.HTTPError(500, "No such file")
#Запрос от клиента на получение результата. Указывается клиент, номер набора
class Result(tornado.web.RequestHandler):
    def get(self,user,set):
        try:
            with open(os.path.join('result',user,str(set)), 'rb') as file:
                message = file.read()
                self.finish(message)
                req={'user': user, 'set': set}
                if req in readyModels:
                    readyModels.remove(req)
        except IOError:
            raise tornado.web.HTTPError(500, "No such file")
#Загрузка от исполнителя 3d модели.Указывается клиент, номер набора
class UploadResult(tornado.web.RequestHandler):
    def post(self,user,set):
        path=os.path.join(__PATH_RES__,user)
        if not os.path.isdir(path):
            os.makedirs(path)
        fname=os.path.join(path,str(set))
        with open(fname, 'wb') as file:
            try:
                file.write(self.request.body)
                req={'user': user, 'set': set}
                if(not (req in  readyModels)):
                        readyModels.append(req)
            except IOError:
                raise tornado.web.HTTPError(500,"Error in the received file")
        EchoWebSocket.clients[user].write_message("NOTIFY")
#Просмотреть готовые модели
class Models(tornado.web.RequestHandler):
    def post(self, user):
        self.set_header("Content-Type", "text/plain")
        sets = [r['set'] for r in readyModels if r['user'] == user]
        self.finish(';'.join(sets))

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    clients = {}
    def open(self,user):
        if user not in EchoWebSocket.clients:
            EchoWebSocket.clients[user]= self
    def on_close(self):
        for user  in EchoWebSocket.clients.keys():
            if(self==EchoWebSocket.clients[user]):
               del(EchoWebSocket.clients[user])
               return
    def on_message(self,mess,binary=False):
        print(readyModels)
        for req in readyModels:
            if(EchoWebSocket.clients[req["user"]]==self):
                self.write_message("NOTIFY")
    def check_origin(self, origin):
        return True

application = tornado.web.Application([
        (r"/client/finished/(?P<user>\w+)/(?P<set>\d+)/", Finish),
        (r"/client/connect/(?P<user>\w+)/", EchoWebSocket),
        (r"/worker/task/", Task),
        (r"/worker/download/(?P<user>\w+)/(?P<set>\d+)/(?P<number>\d+)/", Download),
        (r"/client/result/(?P<user>\w+)/(?P<set>\d+)/", Result),
        (r"/worker/upload/(?P<user>\w+)/(?P<set>\d+)/", UploadResult),
        (r"/client/upload/(?P<user>\w+)/(?P<set>\d+)/(?P<number>\d+)/", Upload),
        (r"/worker/table/", Table),
        (r"/client/models/(?P<user>\w+)/", Models),
        (r"/content/(.*)", tornado.web.StaticFileHandler, {'path':__UPLOADS__})],debug=True)

if __name__ == "__main__":
#Запись в файл "pid.txt" pid процесса
    if os.path.isfile(__FILENAME__):
        print("Process is launched")
    else:
        file = open(__FILENAME__, "w")
        file.write(str(os.getpid()))
        file.close()
    requests=QueueOfRequest()
    application.listen(__PORT__)
    tornado.ioloop.IOLoop.instance().start()
