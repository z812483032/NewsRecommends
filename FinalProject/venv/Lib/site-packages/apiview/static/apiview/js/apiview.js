function ApiViewWS(ws_path, common_listener, conn_ok, options){
    var _this = this;
    this.webSocketBridge = new channels.WebSocketBridge(options);
    this.listenerList = {};
    this.common_listener = common_listener;
    this.gen_reqid = function(){
        return "apiview_" + parseInt(Math.random() * 9000000000 + 1000000000) ;
    }
    this.conn = function(url, data, listener){
        var reqid = _this.gen_reqid();
        while(_this.listenerList.hasOwnProperty(reqid)){
            reqid = _this.gen_reqid();
        }
        _this.listenerList[reqid] = listener;
        var req = {path:url, reqid:reqid, data:data};
        _this.webSocketBridge.send(req);
    }
    this._listener = function(data, stream) {
        var reqid = data['reqid'];
        if(reqid === undefined){
            if (typeof _this.common_listener === "function") {
                _this.common_listener(data);
            }
            return;
        }
        var listener = _this.listenerList[reqid];
        delete _this.listenerList[reqid];
        if(!!listener){
            if (data["status_code"] == 200 && typeof listener.success === "function") {
                listener.success(data["data"]);
            }else if (typeof listener.error === "function") {
                listener.error(data, data["status_code"]);
            }
        }
    }
    this.ws_path = ws_path;
    this.webSocketBridge.connect(ws_path);
    this.webSocketBridge.listen(this._listener);
    if(typeof conn_ok === "function"){
        this.webSocketBridge.socket.addEventListener("open", conn_ok);
    }
};
