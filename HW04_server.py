'''
Created on Feb 25, 2018

@author: Brian Bell
'''

import _thread as thread
import re
from socket import *

SERVER_HOST = ''    # All available interfaces
SERVER_PORT = 5037

class State(object):
    
    def __init__(self):
        pass
    
    

class InitialState(State):
    
    def __init__(self):
        pass
    
    def parseInput(self, input):
        if re.match("^quit*.", input):
            return False
    

class ClientConnection(object):
    
    def __init__(self, connection):
        self.connection = connection
        self.state = InitialState()
        self.__listen__()
        

        
    def __listen__(self):
        while True:
            data = self.connection.recv(10000)
            if not data: break
            print("Echo: " + data.decode())
            self.state = self.readLine(data.decode())
            if not self.state: break
            self.connection.send(self.state.getresponse().encode())
        self.connection.close()
        
    def readLine(self, input):
        # read line and clean input (strip, upper, etc.)
        return self.state.parseInput(input)

        

def handleClient(connection):
    '''
    Keeps connection open with client. Receives input and sends response as string of bytes. 
    '''
    while True:
        data = connection.recv(1024)
        state = InitialState()
        if not data: break
        reply = ''
        connection.send(reply.encode())
    connection.close()

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
    sock_obj.listen(5)  # 5 pending connections before new ones rejected
    listen()
