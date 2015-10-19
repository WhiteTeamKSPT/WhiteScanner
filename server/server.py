import tornado
import tornado.ioloop
import tornado.web
import os
from queueOfRequest import QueueOfRequest
import json

__SEPARATOR__= "/"
__UPLOADS__ = os.path.abspath(os.curdir)+__SEPARATOR__
__PORT__=8000

#Загрузка клиентом фотографии. Указывается клиент, номер набора, номер фотографии
class Upload(tornado.web.RequestHandler):
    def post(self,user,set,number):
        if not os.path.isdir(user):
            os.makedirs(user)
        setPath=__UPLOADS__ +user+__SEPARATOR__+str(set)
        if not os.path.isdir(setPath):
            os.makedirs(setPath)
        fname=setPath+__SEPARATOR__+str(number)
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
        self.finish(json.dumps(requests.lastRequest()))
#Запрос от воркера на загрузку фотографии. Указывается клиент, номер набора, номер фотографии
class Download(tornado.web.RequestHandler):
    def get(self,user,set,number):
        with open(__UPLOADS__ +user+__SEPARATOR__+str(set)+__SEPARATOR__+str(number), 'rb') as file:
            try:
                image = file.read()
                self.finish(image)
            except IOError:
                raise tornado.web.HTTPError(500, "No such file")

application = tornado.web.Application([
        (r"/client/finished/(?P<user>\w+)/(?P<set>\d+)", Finish),
        (r"/worker/task", Task),
        (r"/worker/download/(?P<user>\w+)/(?P<set>\d+)/(?P<number>\d+)", Download),
        (r"/client/upload/(?P<user>\w+)/(?P<set>\d+)/(?P<number>\d+)", Upload)], debug=True)


if __name__ == "__main__":
    requests=QueueOfRequest(__UPLOADS__ ,__SEPARATOR__)
    application.listen(__PORT__)
    tornado.ioloop.IOLoop.instance().start()