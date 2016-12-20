# coding:utf-8

import re
from flask import Flask, jsonify
from service import ProxyService

app = Flask(__name__)

api_list = {
    'get a proxy': '/get/{proxy_type}',
    'delete a proxy': '/delete/{proxy_type}/{ip:port}',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/get/<proxytype>')
def get(proxytype):
    return jsonify(ProxyService().get(proxytype))


@app.route('/delete/<proxytype>/<ip_port>')
def delete(proxytype, ip_port):
    if not re.match("^\d{0,3}.\d{0,3}.\d{0,3}.\d{0,3}:\d+$", ip_port):
        return 'error with ip port'
    return jsonify(ProxyService().delete(proxytype, ip_port))


if __name__ == '__main__':
    app.run("127.0.0.1", 8888, debug=True)