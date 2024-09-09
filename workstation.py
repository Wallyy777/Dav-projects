import socket
from socket import timeout #need this or else we can't catch timeout exceptions?!?!
import time
import random

import requests
interval = 60

def main() :
		'''
		The main function.
		Loops one iteration of the protocol every "interval" seconds.
		'''
		while True :
				step() #loop one iteration of the protocol.
		
def step() :
		'''
		One iteration of the protocol
		The socket is created.
		Then the steps of one iteration of the protocol are taken by the client.
		Then the socket is closed.
		Then the program pauses for "interval" seconds.
		'''
		socket = connect("127.0.0.1", 23457)
		handleProtocol(socket)
		socket.close()
		print("sleep interval: " + str(interval))
		time.sleep(interval)

def connect(serverip, port) :
		'''
		Creates and returns a socket for communicating with the server.
		The timeout is set to 15 seconds.
		'''
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(15)
		s.connect((serverip, port))
		print("connected to server successfully.")
		return s

def packageMessage(s) :
		'''
		Appends the single "\n" character to the end of a message (required by protocol).
		'''
		return s + "\n"
# Connect to hq, sends message and handles response
def fwd_to_hq(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 12346))
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            print(f'Received response from HQ: {response}')
            if response == "ACKNOWLEDGED":
                print("Message successfully FWD to HQ\n")
            else:
                print("Failed to FWD message to HQ\n")
    except Exception as e:
        print("Error Forwarding message to HQ:\n", str(e))


def receiveMessage(socket) :
		'''
		Either receives a message from a socket, or, if the socket times out returns "CONTINUE".
		'''
		try :
				data = socket.recv(64).decode('utf-8')
				fwd_to_hq(data)
				return data
		except timeout as e:
				return "CONTINUE"
		#except Exception as e :
		#		print("ERROR_002: The unspeakable error has occured!")
				
def receivePost(socket) :
		'''
		Receives a post from the smart laundry device.
		returns either CONTINUE (because the server failed to send data)
		ERROR_001 (because the server sent a bad message)
		CLEAR_DATA (because the server sent a valid transaction that should be cleared)
		"" (because the server sent an empty post and no message should be sent to the server).
		'''
		message = receiveMessage(socket)
		if message == "CONTINUE" :
				return "CONTINUE"
		processedMessage = verifyData(message)
		print("data: " + processedMessage)
		if len(processedMessage) == 0 :
				return processedMessage
		if processedMessage.startswith("ERROR_001") :
				return "ERROR_001"
		return "CLEAR_DATA"
		
def handleProtocol(socket) :
		'''
		handles one iteration of the protocol.
		First, the get data message is sent.
		Then, a message is received.
		If no message was recieved, the protocol ends.
		If an empty message was recieved, "interval" must double, the protocol ends.
		If valid data was received, "interval" must be halved.
		The appropriate response must be sent (either CLEAR_DATA or ERROR_001)
		'''
		get = "GET_DATA"
		socket.send(packageMessage(get).encode('utf-8'))
		messageToSend = receivePost(socket)
		fwd_to_hq(messageToSend)
		
		if messageToSend == "CONTINUE" :
				return #end of protocol...
		if messageToSend == "" :
				doubleTime()
				return #end of protocol...
		if messageToSend == "CLEAR_DATA" :
				halfTime()
		socket.send(packageMessage(messageToSend).encode('utf-8'))

def halfTime() :
		'''
		halves the interval between iterations of the protocol.
		'''
		global interval
		if interval > 5 :
				interval = interval / 2
			
def doubleTime() :
		'''
		doubles the interval between iterations of the protocol.
		'''
		global interval
		if interval < 30*60 :
				interval = interval * 2
		
				
def verifyData(data) :
		'''
		verifies the format of the data.
		Prints useful error messages if something goes wrong.
		'''
		error = "ERROR_001"
		if data == "POST\n" :
				return ""
		if not data.startswith("POST") or not data.endswith("\n") :
				return error + " bad header/footer."
		data = data[0:len(data)-1] #strip off trailing "\n" character.
		elements = data.split(" ")
		if len(elements) != 7 :
				return error + " bad number of elements in post: " + str(len(elements))
		if len(elements[1]) != 16 or not elements[1].isdigit() :
				return error + " bad credit card number: " + elements[1]
		if not verifyDate(elements[2], True) :
				return error + " bad expiry date: " + elements[2]
		if not verifyDate(elements[3]) :
				return error + " bad usage date: " + elements[3]
		if not verifyTime(elements[5]) :
				return error + " bad start time: " + elements[5]
		if not verifyTime(elements[6]) :
				return error + " bad end time: " + elements[6]
		if len(elements[4]) != 6 or elements[4][3] != "." or not elements[4][0:3].isdigit() or not elements[4][4:6].isdigit() :
				return error + " bad charge amount: " + elements[4]
		return data[0:len(data)]
		
		
def verifyDate(string, includeDay = False) :
		'''
		verifies if a data is either in mm/dd/yyyy format (includeDay = True)
		or the data is in mm/yy format (includeDay = False).
		'''
		error = False
		success = True
		if includeDay :
				if len(string) != 5 or string[2] != '/' :
						return error
				if not string[0:2].isdigit() or not string[3:5].isdigit() :
						return error
				return success
		if len(string) != 10 :
				return error
		if string[2] != "/" or string[5] != "/" :
				return error
		if not string[0:2].isdigit() or not string[3:5].isdigit() or not string[6:10].isdigit() :
				return error
		return success

def verifyTime(string) :
		'''
		verifies the string is in hh:mm:ss format.
		'''
		error = False
		success = True
		if len(string) != 8 :
				return error
		if string[2] != ':' or string[5] != ':' :
				return error
		if not string[0:2].isdigit() or not string[3:5].isdigit() or not string[6:8].isdigit() :
				return error
		return success
		
#the following line runs the program.
if __name__ == "__main__" :
		main() #need to call this function.
