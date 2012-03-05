var WSTun = function(url, onpacket) {
    this.url = url;
    this.onpacket = onpacket;

    if("WebSocket" in window) {
        this.socket = new WebSocket(url);

    } else {
        this.socket = new MozWebSocket(url);
    }

    var self = this;

    this.socket.onmessage = function(event) {
        buf = Base64.decode(event.data);

        self.onpacket(self, buf);
    };
};

WSTun.prototype.send = function(buf) {
    data = Base64.encode(buf)
    this.socket.send(data);
};

