#/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import commands
import time
import pickle
import threading

class scr():
	def __init(self):
		self.std=threading.Thread(target=self.start_internal)
		self.quit_flag=False
		self.newdata_flag=False
		self.ctldata={'name':[],
						'actionlist':[]}
	def start(self):
		if self.std.is_alive():
			print self.std.is_alive()
			return
		self.std.start()
	def start_internal(self):
		HOST='127.0.0.1'
		PORT=5000
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.bind((HOST,PORT))
		s.listen(1)
		cnt=0
		mask='intelligence.heart\n'
		while True:
			try:
				conn,addr=s.accept()
				print 'address is connect by:',addr
				data=conn.recv(4096)
				if data!=mask:
					conn.close()
					break
				while(!self.newdata_flag):
					if self.quit_flag:
						break
					time.sleep(0.1)
					str= pickle.dumps(self.ctldata)
					data=conn.sendall(str)
					self.reset_ctldata()
					print 'send'
				if self.quit_flag:
					conn.close()
					break
			except:
				print "connect error"
				cnt=0
				conn.close()
				break
		print 'out'
	def quit(self):
		self.quit_flag=True
	def ctl(name,action):
		print "actully going"
		self.ctldata['name']=name
		self.ctldata['actionlist']=action
		self.newdata_flag=True
	def reset_ctldata():
		self.newdata_flag=False
		self.ctldata={'name':[],
						'actionlist':[]}		
		
		