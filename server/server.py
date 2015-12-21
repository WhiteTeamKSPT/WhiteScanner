import tornado
import tornado.ioloop
import tornado.web
import os
import tornado.websocket
from queueOfRequest import QueueOfRequest


__PORT__=8000
__FILENAME__='pid.txt'
__PATH_RES__='result'
readyModels={}
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
                raise tornado.web.HTTPError(500)
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
    def post(self):
        self.render("table.html",title="Requests",header="Table of requests",listOfRequests=requests.queue)
#Запрос от воркера на загрузку фотографии. Указывается клиент, номер набора, номер фотографии "/content/"
class Download(tornado.web.RequestHandler):
    def get(self,user,set,number):
        path=os.path.join(user,str(set),str(number))
        with open(path, 'rb') as file:
            try:
                image = file.read()
                self.finish(image)
                requests.get(user,set,number)
            except IOError:
                raise tornado.web.HTTPError(500, "No such file")
#Запрос от клиента на получение результата. Указывается клиент, номер набора
class Result(tornado.web.RequestHandler):
    def get(self,user,set):
        with open(os.path.join('result',user,str(set)), 'rb') as file:
            try:
                message = file.read()
                self.finish(message)
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
                readyModels[user]=file
            except IOError:
                raise tornado.web.HTTPError(500)
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
    def write_message(self,mess,binary=False):
        for user in readyModels.keys():
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
        (r"/worker/table/", Table)],debug=True)
       # (r"/content/(.*)", tornado.web.StaticFileHandler, {"path": __UPLOADS__})],

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