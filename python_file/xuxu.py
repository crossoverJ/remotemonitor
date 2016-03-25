#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
from flask import Flask 
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import make_response
from flask import session
from flask import Response

def gen():
	print ' '

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def remotec():
	vurl=url_for('static', filename='video/lll.mp4')
	oggurl=url_for('static', filename='video/lll.ogg')
	return render_template('vdd.html',vurl=vurl,oggurl=oggurl)
@app.route('/le/',methods=['GET','POST'])
def le():
	print 'beautiful'
	return 'beauty'
if __name__ == '__main__':
	app.run(host='127.0.0.1',debug=False,port=5044)