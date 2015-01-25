#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from bottle import Bottle

app = Bottle()

@app.route("/index")
@app.route("/")
def route_index():
    return "Index"


bottle.run(app=app, host='127.0.0.1', port=8080,  server='wsgiref' , debug=True, reloader=True)