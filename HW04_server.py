'''
Created on Feb 25, 2018

@author: Brian Bell
'''

import _thread as thread
import re
from socket import *

SERVER_HOST = ''    # All available interfaces
SERVER_PORT = 5032

GOODBYE = "Goodbye!\r\n"

class State(object):
    def __init__(self):
        self.next = self
        self.response = "State not initiated correctly."
    
    def getResponse(self):
        return self.response
    
    def nextState(self):
        return self.next
    
class BeginState(State):
    '''
    Waits for 'HELO xxx' from client. All other messages except 'quit' are ignored.
    '''    
    def parseInput(self, input):
        print(input)
        if re.match("^quit*.", input.lower()):
            self.response = GOODBYE
        if re.match("^HELO*.", input) and len(input.split()) >= 2:
            print("wtf mate")
            self.response = "250 %s Hello %s\r\n" % (serverIP, input.split()[1])
            self.next = WaitState()
        else:
            self.response = "503 5.5.2 Send hello first\r\n"            
            
        
class WaitState(State):
    def parseInput(self, input):
        if re.match("^quit*.", input.lower()):
            self.response = GOODBYE

class MailFromState(State):
    def parseInput(self, input):
        if re.match("^quit*.", input.lower()):
            self.response = GOODBYE

class RcptToState(State):
    def parseInput(self, input):
        if re.match("^quit*.", input.lower()):
            self.response = GOODBYE

class Writing(State):
    def parseInput(self, input):
        if re.match("^quit*.", input.lower()):
            self.response = GOODBYE

class ClientConnection(object):
    
    def __init__(self, connection):
        self.connection = connection
        self.response = "Something weird happened."  # This should never be the sent response
        self.state = BeginState()
        self.respond220()
        self.__listen__()
        
    def respond220(self):
        response = "220 " + serverIP + " Service ready\r\n"
        self.connection.send(response.encode(encoding ='utf_8'))
        
    def __listen__(self):
        while True:
            data = self.connection.recv(10000)
            if not data: break
            d = data.decode()
            print("Received: " + d)
            self.readData(d)
            self.connection.send(self.state.getResponse().encode())
        self.connection.close()
        
    def readData(self, input):
        # read line and clean input (strip, upper, etc.)
        self.state.parseInput(input)
        self.response = self.state.getResponse()
        self.state = self.state.nextState()


def listen():
    '''
    Listens on socket for clients to connect. Dispatches them to a new thread.
    '''
    client_num = 1
    while True:
        connection, addr = sock_obj.accept()
        print("Server connected to by Client %d at %s" % (client_num, addr))
        client_num += 1
        thread.start_new_thread(ClientConnection, (connection,))
        
        
if __name__ == '__main__':
    sock_obj = socket(AF_INET, SOCK_STREAM)
    sock_obj.bind((SERVER_HOST, SERVER_PORT))
    serverIP = gethostname()
    sock_obj.listen(5)  # 5 pending connections before new ones rejected
    listen()
