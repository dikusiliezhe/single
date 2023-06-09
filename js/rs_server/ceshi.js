var requests = [];

if (typeof (XMLHttpRequest) == 'undefined')
    var XMLHttpRequest = function () {
        var request = null;

        if(window.XMLHttpRequest){ //Mozilla,Safari,Opera,IE7等
				request = new XMLHttpRequest();
			}else if(window.ActiveXObject){
				try{
					request = new ActiveXObject("Msxml2.XMLHTTP"); //IE较新版本
				}catch(e){
					try {
						request = new ActiveXObject("Microsoft.XMLHTTP");//IE较老版本
					}catch(e){
						request = null;
					}
				}		
			}

        // try {
        //     request = new ActiveXObject('Msxml2.XMLHTTP');
        // } catch (e) {
        //     try {
        //         request = new ActiveXObject('Microsoft.XMLHTTP');
        //     } catch (ee) {
        //         request = new XMLHttpRequest();
        //     }
        // }
        console.log(request)
        return request;
    }

function ajax_stop() {
    for (var i = 0; i < requests.length; i++) {
        if (requests[i] != null)
            requests[i].abort();
    }
}

function ajax_create_request(context) {
    for (var i = 0; i < requests.length; i++) {
        if (requests[i].readyState == 4) {
            requests[i].abort();
            requests[i].context = context;
            return requests[i];
        }
    }

    var pos = requests.length;

    requests[pos] = Object();
    requests[pos].obj = new XMLHttpRequest();
    requests[pos].context = context;

    return requests[pos];
}

function ajax_request(url, data, callback, context) {
    var request = ajax_create_request(context);
    // var request = new XMLHttpRequest();
    var async = typeof (callback) == 'function';

    if (async) request.obj.onreadystatechange = function () {
        if (request.obj.readyState == 4)
            callback(new ajax_response(request));
    }
    console.log(url)
    console.log(data)
    request.obj.open('POST', url, async);
    request.obj.send(data);

    if (!async)
        return new ajax_response(request);
}

function ajax_response(request) {
    this.request = request.obj;
    this.error = null;
    this.value = null;
    this.context = request.context;

    if (request.obj.status == 200) {
        try {
            this.value = object_from_json(request);

            if (this.value && this.value.error) {
                this.error = this.value.error;
                this.value = null;
            }
        } catch (e) {
            this.error = new ajax_error(e.name, e.description, e.number);
        }
    } else {
        this.error = new ajax_error('HTTP request failed with status: ' + request.obj.status, request.obj.status);
    }

    return this;
}

function enc(s) {
    return s.toString().replace(/\%/g, "%26").replace(/=/g, "%3D");
}

function object_from_json(request) {
    if (request.obj.responseXML != null && request.obj.responseXML.xml != null && request.obj.responseXML.xml != '')
        return request.obj.responseXML;

    var r = null;
    eval('r=' + request.obj.responseText + ';');
    return r;
}

function ajax_error(name, description, number) {
    this.name = name;
    this.description = description;
    this.number = number;

    return this;
}

ajax_error.prototype.toString = function () {
    return this.name + " " + this.description;
}

function json_from_object(o) {
    if (o == null)
        return 'null';

    switch (typeof (o)) {
        case 'object':
            if (o.constructor == Array)		// checks if it is an array [,,,]
            {
                var s = '';
                for (var i = 0; i < o.length; ++i) {
                    s += json_from_object(o[i]);

                    if (i < o.length - 1)
                        s += ',';
                }

                return '[' + s + ']';
            }
            break;
        case 'string':
            return '"' + o.replace(/(["\\])/g, '\\$1') + '"';
        default:
            return String(o);
    }
}

var ajaxVersion = '5.7.22.2';
var From_From_AnnoGoodsContext = {
    GetInfoAnnoGoods: function (infiID, callback, context) {
        return new ajax_request(this.url + '?_method=GetInfoAnnoGoods&_session=rw', 'infiID=' + enc(infiID), callback, context);
    },
    GetInfoBidresult: function (infiID, callback, context) {
        return new ajax_request(this.url + '?_method=GetInfoBidresult&_session=rw', 'infiID=' + enc(infiID), callback, context);
    },
    GetInfoDocQuestion: function (infiID, callback, context) {
        return new ajax_request(this.url + '?_method=GetInfoDocQuestion&_session=rw', 'infiID=' + enc(infiID), callback, context);
    },
    url: 'http://116.62.209.227:9002/ajax/From_From_AnnoGoodsContext,App_Web_vrvyg3ou.ashx'
}
var detialInfo = From_From_AnnoGoodsContext.GetInfoAnnoGoods('4556').value;
console.log(detialInfo)

