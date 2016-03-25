#/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import commands
import time
import pickle
import threading

class scr():
	def __init__(self):
		self.stding = threading.Thread(target=self.start_internal)
		self.quit_flag=False
		self.newdata_flag=False
		self.ctldata={'name':[],
						'actionlist':[]}
	def start(self):
		if self.stding.is_alive():
			print self.std.is_alive()
			return
		self.stding.start()
		print 'server start'
		print self
	def start_internal(self):
		print self
		HOST='120.24.42.148'
		PORT=5000
		HOST1='120.24.42.148'
		PORT1=6011
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			s.bind((HOST1,PORT1))
			s.listen(1)
		except Exception,e:
			print Exception,":",e
			print "open socket error"
			self.newdata_flag=True
			self.quit_flag=True
			return
		cnt=0
		mask='intelligence.heart\n'
		while True:
			print 'going to while'
			try:
				conn,addr=s.accept()
				print 'address is connect by:',addr
				data=conn.recv(4096)
				if data!=mask:
					conn.close()
					break
				print 'recieve'
				while not self.quit_flag:
					while not self.newdata_flag:
						if self.quit_flag:
							print 'recieve quit signal'
							break
						if self.newdata_flag:
							print 'recieve new data!!!!!'
							break
						time.sleep(0.1)
						print 'waiting',self.newdata_flag
					print 'new data!!'
					str= pickle.dumps(self.ctldata)
					data=conn.sendall(str)
					self.reset_ctldata()
					print 'send'
				if self.quit_flag:
					print 'recieve quit signal'
					conn.close()
					break
			except Exception,e:
				print Exception,":",e
				print "connect error"
				cnt=0
				conn.close()
				continue
		print 'out'
	def qt(self):
		print 'qt in'
		self.quit_flag=True
		print 'qt out'
		print self.quit_flag
	def ctl(self,name,action):
		print 'new data -----------------------------------'
		print self
		self.ctldata['name']=name
		self.ctldata['actionlist']=action
		self.newdata_flag=True
	def reset_ctldata(self):
		self.newdata_flag=False
		self.ctldata={'name':[],
						'actionlist':[]}		
if __name__ == '__main__':
	cl=scr()
	cl.start()
	time.sleep(7)
	cl.ctl(['crossoverj'],['takepicture'])
	time.sleep(5)
	cl.qt()
	print 'send quit'
		