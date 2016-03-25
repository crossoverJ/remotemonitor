#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2
import json
import time 
import pickle
from urllib import urlencode
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class sdmsg():
	def __init__(self):
		self.typefunc={'text':self.sendtext}	
		# 管理组 ：test
		# 管理员 ：crossoverj
		self.info={  'AccessToken':'',
				'AT_time':0,
				'AT_expires_in':0,
				'Secret' :"0dvetk6Kivhbh27TKe_c0evcoZw-tZR7kSAhDojs7QQ9VyTO1NsTMb-8PaQa1X1I",
				'CorpID' :"wxb43cf56135719896"}
		try:
			info=open("access_info.pkl",'r')
			print info.readlines()
			info=open("access_info.pkl",'r')
		except:
			print 'ERROR!:open pkl file failed!'
			return
		infodata=pickle.load(info)
		info.close()
		try:
			if not infodata['AccessToken']=='' and not infodata['AT_time']==0:
				self.info=infodata
		except:
			print "ERROR! no data in pkl file!"
	def get_token_internal(self):
		geturl='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (self.info['CorpID'],self.info['Secret'])
		print geturl
		get_t=httplib2.Http()
		resp,content=get_t.request(geturl,'GET')
		print 'content type',type(content)
		try:
			result=json.loads(content)
		except:
			return False,''
		try:
			self.info['AccessToken']=result['access_token']
			self.info['AT_expires_in']=result['expires_in']
			self.info['AT_time']=time.time()
			print self.info['AccessToken']
			print self.info['AT_expires_in']
			print self.info['AT_time']
		except:
			return False
		try:
			fl=open("access_info.pkl",'w')
		except:
			print "ERROR!: can not open pkl file when try to store access token"
			return True
		pickle.dump(self.info,fl)
		fl.close()
		return True
	def get_token(self):
		t=time.time()-self.info['AT_time']
		if t > (self.info['AT_expires_in']-10) or self.info['AccessToken']=='':
			print 'Time out! Need to get a new token!'
			for i in range(0,3):
				if self.get_token_internal():
					print 'succeed'
					return True
				else:
					print 'wait to get token %d times' % (i)
					time.sleep(2)
			return False
		else:
			print "Don't need to fresh access token"
			return True
	def sendmsg(self,type,name,part,content):
		if not self.get_token():
			return False
		h=httplib2.Http()
		dict=self.typefunc[type](name,part,content)
		data = json.dumps(dict,ensure_ascii=False)
		print data
		#print info['AccessToken']
		wxurl='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % self.info['AccessToken']
		#print wxurl
		#wxurl='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN'
		#print urlencode(dict)
		resp,content=h.request(wxurl,'POST',
							data, 
							headers={'Content-Type': 'application/x-www-form-urlencoded'})
		#print resp
		print content
	def sendtext(self,name,part,content):
		#todo 数据合法性检查
		dict={ "touser" : str(name),
			   "toparty": str(part),
			   "msgtype": "text",
			   "agentid": 1,
			   "text": {
				   "content": content
			   },
			   "safe":"0"}
		print dict
		return dict
	def upload_image(self):
		if not self.get_token():#不是特别有必要判断access token，因为在调用时已经有sendmsg检查过，防止别处调用发生错误，所以添加判断
			return False
		upload_image_url= 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s' % (self.info['AccessToken'],'image')
		h=httplib2.Http()
		file=open("test.jpg",'r')
		content=file.read()
		data = [] 
		boundary = '---------------------------32404670520626'
		data.append('--%s' % boundary) 
		data.append('Content-Disposition: form-data; name="%s"; filename="%s"' %('test', 'test.jpg')) 
		data.append('Content-Length: %d' % len(content)) 
		data.append('Content-Type:application/x-jpg') 
		data.append('Content-Transfer-Encoding: binary\r\n') 
		data.append(content) 
		data.append('--%s--\r\n' % boundary) 
		sendcontent=str('\r\n'.join(data))
		
		resp,content=h.request(upload_image_url,'POST',
							sendcontent, 
							headers={'Content-Type': 'multipart/form-data; boundary=%s' % boundary})
		file.close()
		print resp
		print content
		
if __name__ == '__main__':
	#tempfile=open('info.pkl','wr')
	sd=sdmsg()
	sd.sendmsg('text','crossoverj',1,u'你好')
	#sd.upload_image()