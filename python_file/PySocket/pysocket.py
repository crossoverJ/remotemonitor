#/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import commands
import time
import pickle
HOST='120.24.42.148'
PORT=5000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
cnt=0
while True:
	try:
		conn,addr=s.accept()
		print 'address is connect by:',addr
		result=''
		while 1:
			data=conn.recv(4096)
			cnt+=1
			if data=='':
				print 'over'
				rec= pickle.loads(result)
				print rec
				st=open("reciv.jpg",'wb')
				st.write(rec['file'])
				st.close()	
				break
			result+=data
			print cnt,':',str(data)
	except:
		print "connect error"
		cnt=0
		conn.close()
		break
