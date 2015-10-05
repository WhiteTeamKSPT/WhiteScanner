import tornado
import tornado.ioloop
import tornado.web
import os
__UPLOADS__ = os.path.abspath(os.curdir)+"/"
__PORT__=8000
class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class Upload(tornado.web.RequestHandler):
    def post(self,user,number):
        fileinfo = self.request.files['filearg'][0]
        files = os.listdir(__UPLOADS__)
        for i in files:
            if(user==i):
                break
            if(i==files[len(files)-1]):
                os.mkdir(user)
        fname=user+"/"+str(number)
        fh = open(__UPLOADS__ + fname, 'wb')
        fh.write(fileinfo['body'])
        self.finish(fname + " is uploaded!! Check %s folder" %(__UPLOADS__+user))


application = tornado.web.Application([
        (r"/", Userform),
        (r"/upload/(?P<user>\w+)/(?P<number>\d+)", Upload)], debug=True)


if __name__ == "__main__":
    application.listen(__PORT__)
    tornado.ioloop.IOLoop.instance().start()