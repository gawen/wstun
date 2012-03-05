# wstun

`wstun` is a Python script which connects an tun/tap IP tunnel to a WebSocket, giving the ability to deal with IP or Ethernet packets in a browser.

For now, it is quite rudimental, but does the job.

`wstun` is under the MIT license.

## Why?

I don't know.

## No but ... seriously?

For the beautiz ! Connect two worlds which does not overlap. I have no doubt this is not something to be used in a "industrial" world, but I suppose some hackers would enjoy playing with IP, TCP and UDP with Javascript runned in a browser.

# How to use

For now, the script is under heavy development, and no example is really provided. But it's planned. If you have the hacker soul, you'd probably be satisfied.

First of all, `wstun` required [Tornado Web](https://github.com/facebook/tornado) and [pytun](https://github.com/Gawen/pytun) to be installed.
    
    $ pip install tornado pytun

Clone this repos and start the script `wstun.py` with the required privilege level to create a tun tunnel. You will probably need the root privilege.

    python wstun.py -C -i 192.168.142.1 -s 192.168.142.0/24 -p /tun -P 8888

This will creates the websocket `ws://localhost:8888/tun` streaming the raw packets broadcasted through the tunnel interface. The `-C` attribute will auto-configure the interface and the route to make it playable out of the box. This basically do

    $ ifconfig tunnel 192.168.142.1
    $ route add -net 192.168.142.0/24 dev tun0

To enjoy tunnels from your browser, include the `wstun.js` and `base64.js` files.

    <script type="text/javascript" src="base64.js"></script>
    <script type="text/javascript" src="wstun.js"></script>

Instantiate a connection to the websocket.

    tun = new WSTun("ws://localhost:8888/tun", onpacket);

`onpacket` is a callback called when a packet is received.

    onpacket = function(tun, packet) {
        // packet is the raw packet data.

        // Ping? Pong!
        tun.send(packet);
    };

# And then ?

Then, you'd need a IP stack to do something with the raw packets and do some magic. I'm currently working on one on my free time. If you want to contribute, contact me.

