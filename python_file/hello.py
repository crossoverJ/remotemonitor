#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask 
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import os,sys
from flask import request
from Process_XML import Proc_XML,Pack_XML
from socketserv import servr
import time
app = Flask(__name__)
host='120.24.42.148'
port=6123
sv=servr()
sv.run(host,port)

@app.route('/',methods=['GET', 'POST'])
def remotec():
	sToken = "intelligenceheart"
	sEncodingAESKey = "YJvpuukcFp9HiLGASa8gomMeVs4hK91spYKV27K4wKu"
	sCorpID = "wxb43cf56135719896"
	wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)	
	print 'in~!!!!!!!!!!!!'
	if request.method == 'GET':
		sVerifyMsgSig=request.args.get('msg_signature')
		sVerifyTimeStamp=request.args.get('timestamp')
		sVerifyNonce=request.args.get('nonce')
		sVerifyEchoStr=request.args.get('echostr')
		print sVerifyMsgSig
		print sVerifyTimeStamp
		print sVerifyNonce
		print sVerifyEchoStr
		ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
		if(ret!=0):
			print "ERR: VerifyURL ret: " , ret
			sys.exit(1)
		return sEchoStr
	elif request.method == 'POST':
		print '-------------------A New POST Request-------------------------------'
		sReqMsgSig=request.args.get('msg_signature')
		sReqTimeStamp=request.args.get('timestamp')
		sReqNonce=request.args.get('nonce')
		sReqData=request.data
		ret,sMsg=wxcpt.DecryptMsg( sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
		print sMsg
		Message=Proc_XML(sMsg)
		ReInfo=Message.Do_By_Msg(sv)
		print ReInfo
		RePackage=Pack_XML(wxcpt)
		RePack=RePackage.get(sReqNonce,sReqTimeStamp,ReInfo)
		print '--------------Return For The POST Request---------------------------'
		return RePack
		
		
if __name__ == '__main__':
	app.run(host='127.0.0.2',debug=False,port=5010)
	