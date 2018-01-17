import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

from tornado.options import define, options
from handlers import *

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/", MainHandler),
            (r"/wsocket", Socket_Sender),
            (r"/api/model/([0-9]+)", Strategy_Handler),
            (r"/api/model/output/", ModelOutputs_Handler),
            (r"/api/led/([0-9]+)", LED_Handler),
            (r"/api/buz/([0-9]+)", Buz_Handler),
            (r"/api/video/([0-9]+)", Live_Handler),
        ]
        settings = dict(
            cookie_secret="tornado_secret", 
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()