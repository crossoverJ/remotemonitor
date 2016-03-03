#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys,os
import time 
from ctlraspi import scr
import random
from textprocess import tproc
class  Proc_XML(object):
	def __init__(self,Msg):
		self.ReInfo={}
		self.xml_tree = ET.fromstring(Msg)
		self.ToUserName = self.xml_tree.find("ToUserName").text
		self.FromUserName = self.xml_tree.find("FromUserName").text
		self.ReInfo['ToUserName']=self.FromUserName
		self.ReInfo['FromUserName']=self.ToUserName
		self.CreateTime = self.xml_tree.find("CreateTime").text
		self.AgentID = self.xml_tree.find("AgentID").text
		self.Proc_msg = self.xml_tree.find("MsgType").text.lower()
		self.CreateTime = self.xml_tree.find("CreateTime").text
		self.Msg_list  ={'text':self.Msg_Proc_text ,
						'image':self.Msg_Proc_image ,
						'voice':self.Msg_Proc_voice ,
						'video':self.Msg_Proc_video ,
						'shortvideo':self.Msg_Proc_shortvideo ,
						'location':self.Msg_Proc_location,
						'event':self.Do_By_Event}
						
		if self.Proc_msg == 'event':
			self.Proc_event = self.xml_tree.find("Event").text.lower()		
			self.Event_list={'subscribe':self.Event_Proc_subscribe ,
							'unsubscribe':self.Event_Proc_unsubscribe ,
							'location':self.Event_Proc_location ,
							'click':self.Event_Proc_click ,
							'view':self.Event_Proc_view ,
							'scancode_push':self.Event_Proc_scancode_push ,
							'scancode_waitmsg':self.Event_Proc_scancode_waitmsg ,
							'pic_sysphoto':self.Event_Proc_pic_sysphoto ,
							'pic_photo_or_album':self.Event_Proc_pic_photo_or_album ,
							'pic_weixin':self.Event_Proc_pic_weixin ,
							'location_select':self.Event_Proc_location_select  ,
							'enter_agent':self.Event_Proc_enter_agent ,
							'batch_job_result':self.Event_Proc_batch_job_result}
		
		elif self.Proc_msg == 'text':
			self.Content = self.xml_tree.find("Content").text.encode("UTF-8")
			self.MsgId = self.xml_tree.find("MsgId").text
			
		elif self.Proc_msg == 'image':
			self.PicUrl = self.xml_tree.find("PicUrl").text
			self.MediaId = self.xml_tree.find("MediaId").text
			self.MsgId = self.xml_tree.find("MsgId").text
			
		elif self.Proc_msg == 'voice':
			self.MediaId = self.xml_tree.find("MediaId").text
			self.Format = self.xml_tree.find("Format").text
			self.MsgId = self.xml_tree.find("MsgId").text
			
		elif self.Proc_msg == 'video':
			self.MediaId = self.xml_tree.find("MediaId").text
			self.ThumbMediaId = self.xml_tree.find("ThumbMediaId").text
			self.MsgId = self.xml_tree.find("MsgId").text
		
		elif self.Proc_msg == 'shortvideo':
			self.MediaId = self.xml_tree.find("MediaId").text
			self.ThumbMediaId = self.xml_tree.find("ThumbMediaId").text
			self.MsgId = self.xml_tree.find("MsgId").text
	
		elif self.Proc_msg == 'location':
			self.Location_X = self.xml_tree.find("Location_X").text
			self.Location_Y = self.xml_tree.find("Location_Y").text
			self.Scale = self.xml_tree.find("Scale").text
			self.Label = self.xml_tree.find("Label").text
			self.MsgId = self.xml_tree.find("MsgId").text
		self.sMsg=Msg
	
	def Print_Info(self): #need to delete or override
		if self.Proc_msg == 'event':
			print 'Message Infomation-----------------------'
			print ' ToUserName','   == ',self.xml_tree.find("ToUserName").text
			print ' FromUserName',' == ',self.xml_tree.find("FromUserName").text
			print ' CreateTime','   == ',self.xml_tree.find("CreateTime").text
			print ' MsgType','      == ',self.xml_tree.find("MsgType").text
			print ' Event','        == ',self.xml_tree.find("Event").text
			print ' EventKey','     == ',self.xml_tree.find("EventKey").text
			print ' AgentID','      == ',self.xml_tree.find("AgentID").text	
			print '-----------------------------------------'
	def Do_By_Msg(self,sv):
		self.sv=sv
		return self.Msg_list[self.Proc_msg](self.xml_tree)
	def Do_By_Event(self,xml_handler):
		if self.Proc_msg != 'event':
			self.ReInfo['MsgType']='text'
			self.ReInfo['cont']='ERROR!!!please GUIxIA'
			return self.ReInfo
		self.ReInfo['MsgType']='text'
		self.ReInfo['cont']=self.Event_list[self.Proc_event](self.xml_tree)
		return self.ReInfo
		
	def Event_Proc_subscribe(self,xml_handler):
		print 'Event_Proc_subscribe'
		return 'The Event you request was done'
	def Event_Proc_unsubscribe(self,xml_handler):
		print 'Event_Proc_unsubscribe'
	
	def Event_Proc_location(self,xml_handler):
		print 'Event_Proc_LOCATION'
		
	def Event_Proc_click(self,xml_handler):
		print self.Proc_event
		Proc_event_key = self.xml_tree.find("EventKey").text
		print Proc_event_key
		if Proc_event_key=='take_picture':
			print 'remotec ：recieve capture command'
			self.sv.ctl([self.ReInfo['ToUserName']],['takepicture'])	
		elif Proc_event_key=='monitor_start':
			print 'remotec ：recieve record command'
			self.sv.ctl([self.ReInfo['ToUserName']],['monitorstart'])
		elif Proc_event_key=='monitor_stop':
			print 'remotec ：recieve record command'
			self.sv.ctl([self.ReInfo['ToUserName']],['monitorstop'])	
		return 'Recieved your request: '+Proc_event_key
		
	def Event_Proc_view(self,xml_handler):
		print 'Event_Proc_VIEW'
		
	def Event_Proc_scancode_push(self,xml_handler):
		print 'Event_Proc_scancode_push'
		
	def Event_Proc_scancode_waitmsg(self,xml_handler):
		print 'Event_Proc_scancode_waitmsg'
		
	def Event_Proc_pic_photo_or_album(self,xml_handler):
		print 'Event_Proc_pic_photo_or_album'
		
	def Event_Proc_pic_weixin(self,xml_handler):
		print 'Event_Proc_pic_weixin'
		
	def Event_Proc_location_select(self,xml_handler):
		print 'Event_Proc_location_select'
		
	def Event_Proc_enter_agent(self,xml_handler):
		print 'Event_Proc_enter_agent'
		
	def Event_Proc_pic_sysphoto(self,xml_handler):
		print 'Event_Proc_pic_sysphoto'
		
	def Event_Proc_batch_job_result(self,xml_handler):
		print 'Event_Proc_batch_job_result'
		
	def Msg_Proc_text(self,xml_handler):
		print 'Msg_Proc_text'
		self.ReInfo['MsgType']='text'
		tp=tproc()
		self.ReInfo['cont']=tp.proc(self.Content)
		return self.ReInfo	
	
	def Msg_Proc_image(self,xml_handler):
		print 'Msg_Proc_image'
		self.ReInfo['MsgType']='text'
		self.ReInfo['cont']='我不认识图片，别发了'
		return self.ReInfo
		
	def Msg_Proc_voice(self,xml_handler):
		print 'Msg_Proc_voice'
		self.ReInfo['MsgType']='text'
		self.ReInfo['cont']='我听不懂你在说啥，别说了'
		print self.ReInfo['cont']
		return self.ReInfo
	
	def Msg_Proc_video(self,xml_handler):
		print 'Msg_Proc_image'
		self.ReInfo['MsgType']='text'
		self.ReInfo['cont']='我并不想和你视频'
		return self.ReInfo
		
	def Msg_Proc_shortvideo(self,xml_handler):
		print 'Msg_Proc_shortvideo'
		self.ReInfo['MsgType']='text'
		self.ReInfo['cont']='视频我更看不懂了，别发了！！！'
		return self.ReInfo
	
	def Msg_Proc_location(self,xml_handler):
		print 'Msg_Proc_location'
		self.ReInfo['MsgType']='text'
		self.ReInfo['cont']='我并不知道你在哪里'
		return self.ReInfo
		
		
class Pack_XML():
	def __init__(self,wxcpt):
		print 'Init package XML'
		self.MY_TEMPLATES={}
		self.MY_TEMPLATES['text'] = """<xml>
<ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
<FromUserName><![CDATA[%(FromUserName)s]]></FromUserName>
<CreateTime>%(timestamp)s</CreateTime>
<MsgType><![CDATA[%(MsgType)s]]></MsgType>
<Content><![CDATA[%(cont)s]]></Content>
</xml>"""
		self.wxcpt=wxcpt
	def get(self,sReqNonce,sReqTimeStamp,Info):
		Info['timestamp'] = str(int(time.time()))
		sRespData=self.MY_TEMPLATES[Info['MsgType']] % Info
		print sRespData
		#sRespData="<xml><ToUserName><![CDATA[crossoverJ]]></ToUserName><FromUserName><![CDATA[wxb43cf56135719896]]></FromUserName><CreateTime>1452412296</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[this is a test]]></Content></xml>"
		ret,sEncryptMsg=self.wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)
		if( ret!=0 ):
			print "ERR: EncryptMsg ret: " + ret
			sys.exit(1)
		print 'package XML'
		return sEncryptMsg
		
		