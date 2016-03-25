#/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
import threading
import os,sys
import pickle
import time

class servr():
	def __init__(self):
		print 'servr class init'
		self.RECV_BUFFER=4096
		self.TIME_OUT=200
		self.evtq=threading.Event()
		self.connlist=[]
		self.connlists=[]
	def run(self,host,port):
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.bind((host,port))
		self.s.listen(5)
		self.servthd=threading.Thread(target=self.run_internal)
		self.servthd.start()
	def run_internal(self):
		self.connlist.append(self.s)
		print "servr.run_internal : server started!"
		while not self.evtq.isSet():
			print "servr.run_internal : waiting new msg!"
			rd_sk,wt_sk,er_sk=select.select(self.connlist,[],[],self.TIME_OUT)
			print "servr.run_internal : something new coming"
			if not rd_sk:
				print "servr.run_internal : waiting time out,no heartbeat recieved"
				continue
			print "servr.run_internal : recieve msg! "
			for sk in rd_sk:
				if sk == self.s:
					conn,addr=self.s.accept()
					self.connlist.append(conn)
					print "servr.run_internal : New client connect :addr=%s" % str(addr)
				else:
					try:
						result=sk.recv(self.RECV_BUFFER)
						print result
						if not result:
							print "servr.run_internal : close socket because of recv empty"
							self.rm_socket(sk)							
					except:
						print "servr.run_internal : close socket because of recv ERROR"
						self.rm_socket(sk)
	def rm_socket(self,sk):
		self.connlist.remove(sk)
		sk.close()
		print "servr.rm_socket : socket offline "
	def quit(self):
		print "servr.quit : time to quit "
		self.evtq.set()
		print "servr.quit : send quit event,waiting thread quit "
		self.servthd.join()
		print "servr.quit : thread quited "
		for sock in self.connlist:
			try:
				sock.close()
			except:
				pass
		self.s.close()
		print "servr.quit : close socket "
	def ctl(self,name,action):
		ctl_th=threading.Thread(target=self.ctl_internal,args=(name,action,))
		ctl_th.start()
	def ctl_internal(self,name,action):
		ctldata={'name':[],
					'actionlist':[]}
		ctldata['name']=name
		ctldata['actionlist']=action
		str= pickle.dumps(ctldata)
		print len(self.connlist)
		for sk in self.connlist:
			if sk == self.s:
				print "servr.ctl_internal : main socket is ",sk
				continue
			try:
				print "servr.ctl_internal : try to send massage to" ,sk
				data=sk.sendall(str)
				print 'servr.ctl_internal : send massage to ',sk
			except Exception,e:
				print "servr.ctl_internal : ERROR ",Exception,":",e
				print "servr.ctl_internal : send massage failed "
				self.rm_socket(sk)
		
'''	
class connecthread():
	def __init__(self,conn,addr):
		self.conn=conn
		self.addr=addr
	def run(self):
		self.condthd=threading.Thread(target=self.cthd)
		self.heartbeathd=threading.Thread(target=self.hthd)
		condthd.setDeamon(True)
		heartbeathd.setDeamon(True)
		self.locks=threading.Lock()
		self.condq=threading.Condition()
		self.heartbeathd.start()
	def cthd(self):
		if self.locks.acquire(5)
			self.conn.sendall('msg')
			self.loacks.release()
		else:
			print 'connecthread : ERROR! wait to send msg timeout '
		print 'cthd : out'
	def hthd(self):
		while not self.condq.isSet():
			self.condq.wait(60)
			if self.locks.acquire(5)
				self.conn.sendall('heartbeat')# or recv???
				self.loacks.release()
			else:	
				print 'connecthread : ERROR! wait for connect lock timeout '
		print 'hthd : out'
	def sendctl(self,msg):
		self.evt.set()
		self.msg=msg
		#if new msg come while last msg is sending
		self.condthd.start()
	def quit(self):
		self.condq.set()
		self.condthd.join()
		self.heartbeathd.join()
'''
if __name__ == '__main__':
	host='120.24.42.148'
	port=6123
	sv=servr()
	sv.run(host,port)
	time.sleep(100)
	print "time over"
	sv.quit()
		
	
