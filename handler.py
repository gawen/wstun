import tornado
import tornado.web
import tornado.websocket
import tornado.ioloop

import pytun

class TunnelWebSocketHandler(tornado.websocket.WebSocketHandler):
    @staticmethod
    def builder(name, tun = None):
        """ Class meta-builder.
        
            Returns a class object, not a class instance !
        
        """

        tun = tun if tun is not None else pytun.open()

        cls = type(name, (TunnelWebSocketHandler, ), {
            "tun": tun,
            "ioloop_state": False,

            "clients" : set(),
        })

        return cls

    def allow_draft76(self):
        return True

    def open(self):
        print "*** open"
        self.clients.add(self)
        self.update_ioloop()

    def on_close(self):
        print "*** close"
        try:
            self.clients.remove(self)
        except KeyError:
            pass

        self.update_ioloop()

    @classmethod
    def update_ioloop(cls):
        if cls.clients and not cls.ioloop_state:
            tornado.ioloop.IOLoop.instance().add_handler(cls.tun.fileno(), cls.tun_handler, tornado.ioloop.IOLoop.READ)
            cls.ioloop_state = True

        if not cls.clients and cls.ioloop_state:
            tornado.ioloop.IOLoop.instance().remove_handler(cls.tun.fileno())
            cls.ioloop_state = False

    def on_message(self, message):
        buf = message.decode("base64")
        self.broadcast(buf, except_ = self)

    @classmethod
    def tun_handler(cls, fd, events):
        assert cls.tun.fileno() == fd

        buf = cls.tun.recv()
        cls.broadcast(buf, except_ = cls.tun)

    @classmethod
    def broadcast(cls, buf, except_ = None):
        buf_b64 = buf.encode("base64")

        print ">", repr(buf)
        print (ord(buf[2]) << 8) | (ord(buf[3]) << 0)

        for client in cls.clients:
            if except_ == client:
                continue

            client.write_message(buf_b64)

        if except_ != cls.tun:
            cls.tun.send(buf)

