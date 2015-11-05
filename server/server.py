import tornado
import tornado.ioloop
import tornado.web
import os
import tornado.websocket
import json
from queueOfRequest import QueueOfRequest
from workerSocket import WSWorkerHandler

__UPLOADS__ = os.path.abspath(os.curdir)
__PORT__=8000
__FILENAME__=os.path.join(__UPLOADS__,'pid.txt')
__PATH_RES__=os.path.join(__UPLOADS__,'result')

#Загрузка клиентом фотографии. Указывается клиент, номер набора, номер фотографии
class Upload(tornado.web.RequestHandler):
    def post(self,user,set,number):
        if not os.path.isdir(user):
            os.makedirs(user)
        setPath=os.path.join(__UPLOADS__,user,str(set))
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
        self.render("table.html",title="Requests",header="Table of requests",listOfRequests=requests.queue)
#Запрос от воркера на загрузку фотографии. Указывается клиент, номер набора, номер фотографии
class Download(tornado.web.RequestHandler):
    def get(self,user,set,number):
        with open(os.path.join(__UPLOADS__ ,user,str(set),str(number)), 'rb') as file:
            try:
                image = file.read()
                self.finish(image)
            except IOError:
                raise tornado.web.HTTPError(500, "No such file")
#Запрос от клиента на получение результата. Указывается клиент, номер набора
class Result(tornado.web.RequestHandler):
    def get(self,user,set):
        with open(os.path.join(__UPLOADS__ ,'result',user,str(set)), 'rb') as file:
            try:
                message = file.read()
                self.finish(message)
            except IOError:
                raise tornado.web.HTTPError(500, "No such file")
#Загрузка от исполнителя 3d модели.Указывается клиент, номер набора
class UploadResult(tornado.web.RequestHandler):
    def post(self,user,set):
        if not os.path.isdir(os.path.join(__PATH_RES__,user)):
            os.makedirs(user)
        fname=os.path.join(__PATH_RES__,user,str(set))
        with open(fname, 'wb') as file:
            try:
                file.write(self.request.body)
            except IOError:
                raise tornado.web.HTTPError(500)
application = tornado.web.Application([
        (r"/client/finished/(?P<user>\w+)/(?P<set>\d+)", Finish),
        (r"/worker/task", Task),
        (r"/worker/download/(?P<user>\w+)/(?P<set>\d+)/(?P<number>\d+)", Download),
        (r"/client/result(?P<user>\w+)/(?P<set>\d+)", Result),
        (r"/worker/upload/(?P<user>\w+)/(?P<set>\d+)", UploadResult),
        (r"/client/upload/(?P<user>\w+)/(?P<set>\d+)/(?P<number>\d+)", Upload),
        (r"/content/(.*)", web.StaticFileHandler, {"path": __UPLOADS__})],debug=True)


if __name__ == "__main__":
#Запись в файл "pid.txt" pid процесса
    if os.path.isfile(__FILENAME__):
        print("Process is launched")
    else:
        file = open(__FILENAME__, "w")
        file.write(str(os.getpid()))
        file.close()
    requests=QueueOfRequest(__UPLOADS__)
    application.listen(__PORT__)
    tornado.ioloop.IOLoop.instance().start()
