#!/usr/bin/env python

import tornado
import tornado.web
import handler
import optparse
import os

TWSHandler = handler.TunnelWebSocketHandler.builder("TWSHandler")

def main():
    parser = optparse.OptionParser()

    parser.add_option("-P", "--listen-port", dest = "port", default = 8888, help = "Server listen port.")
    parser.add_option("-C", "--configure", default = False, action = "store_true", help = "Configure the interface with parameters ip, subnet, cidr.")
    parser.add_option("-i", "--ip", default = "192.168.142.1", help = "IP to configure (see -C).")
    parser.add_option("-s", "--subnet", default = "192.168.142.0/24", help = "Subnet to configure (subnet/cidr).")
    parser.add_option("-p", "--path", default = r"/", help = "WebSocket path.")

    (options, args) = parser.parse_args()

    tun = TWSHandler.tun

    # Configure iface
    if options.configure:
        print "Configure '%s' with %s (%s)." % (tun.name, options.ip, options.subnet, )

        def system(cmd):
            print "$ %s" % (cmd, )
            os.system(cmd)

        system("ifconfig %s %s" % (tun.name, options.ip, ))
        system("route add -net %s dev %s" % (options.subnet, tun.name, ))

    app = tornado.web.Application(
        [
            (options.path, TWSHandler),
        ],

        {
        }
    )

    app.listen(options.port)
    print "Tunnel is '%s'." % (tun.name, )
    print "Listening on port %s." % (options.port, )
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
