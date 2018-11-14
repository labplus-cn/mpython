#coding:utf-8

import _thread
import socket
import json
import hashlib
import time

Server_IP = "www.bigiot.net"
Server_Port = 8282

class Device:
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.reciver_thread = threading.Thread(target=self.reciver_loop,args=())
		self.ID = None
		self.Busy = False
		self.__ret_data__ = None
		self.connect()
		_thread.start_new_thread(self.reciver_loop, ())
		self.cb=None
		self.checkinOK=False

#Connect Server
	def connect(self):
		self.socket.connect((Server_IP,Server_Port))

#Send data, and wait for a return
	def socket_send(self,str):
		self.Busy = True
		self.socket.send(str)
		start_time = time.time()
		while self.Busy:
			time.sleep(0.1)
			if time.time()-start_time > 1:
				return None
		return json.loads(""+self.__ret_data__)

#Receive data callback 
	def tcp_recv_callback(self,ret):
		#print (ret)
		pass

#Sockets receive data
	def reciver_loop(self):
		while True:
			res =  self.socket.recv(1024)
			self.tcp_recv_callback(res[:-1])
			res = json.loads(res)
			try:
				M = res["M"]
			except Exception as e:
				print(e.args)	
			if M == "b":
				self.socket.send('{"M":"status"}\n')
				continue
			elif M == "WELCOME TO BIGIOT":
				continue
			elif M == "checkinok":
				self.checkinOK=True
				self.ID = res["ID"]
			elif M == "say" and res["C"] is not None:
				self.cb(res["C"])
				continue
			if self.Busy == True:
				if M != "say":
					self.__ret_data__ = json.dumps(res)
					self.Busy = False

	def isCheckin(self):
		return self.checkinOK


#Device login
	def checkin(self,ID,K):
		self.ID = ID
		self.K = K
		obj = {"M":"checkin","ID":ID,"K":K}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

	def say_callback(self,f):
		self.cb = f

		
#Speak to other people
	def say(self,ID,C,SIGN=None):
		obj = {"M":"say","ID":ID,"C":C,"SIGN":SIGN}
		obj = json.dumps(obj)+"\n"
		self.socket.send(obj)

#Check online
	def isOL(self,ID):
		obj = {"M":"isOL","ID":ID}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

#Get the device status
	def status(self):
		obj = {"M":"status"}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

#Send an alert
	def alert(self,C,B):
		obj = {"M":"alert","C":C,"B":B}
		obj = json.dumps(obj)+"\n"
		self.socket.send(obj)

#Get the server time
	def time(self,F="stamp"):
		obj = {"M":"time","F":F}
		obj = json.dumps(obj)+"\n"
		return self.socket_send(obj)

#Forced to log out
	def checkout(self,ID,K):
		obj = {"M":"checkout","ID":ID,"K":K}
		obj = json.dumps(obj)+"\n"
		self.checkinOK=False
		return self.socket_send(obj)

#Submit data to the data interface
	def update(self,data):
		obj = {"M":"update","ID":self.ID[1:],"V":data}
		obj = json.dumps(obj)+"\n"
		#print (obj)
		self.socket.send(obj)
