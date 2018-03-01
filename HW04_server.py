'''
Created on Feb 25, 2018

@author: Brian Bell
'''

import _thread as thread
import re
from socket import *
from HW04_email import Email

SERVER_HOST = ''    # All available interfaces
SERVER_PORT = 5031

complete_emails = []
GOODBYE = "221 %s closing connection\r\n" % getfqdn()

class State(object):
    '''
    Parent class for other SMTP states. Should not be initialized.
    '''
    def __init__(self, email):
        self.next = self
        self.response = "State not initiated correctly.\r\n"
        self.email = email
    
    def isQuit(self, input):
        if re.match("^quit*.", input.lower()):
            self.response = GOODBYE
            return True
        return False
    
    def getResponse(self):
        return self.response
    
    def nextState(self):
        return self.next
    
    def getEmail(self):
        return self.email.getFullEmail()
    
class BeginState(State):
    '''
    Waits for 'HELO xxx' from client. All other messages except 'quit' are ignored.
    '''
    def __init__(self):
        super().__init__(Email())
        self.response = "503 5.5.2 Send hello first\r\n"
      
    def parseInput(self, input):
        if self.isQuit(input): return
        if re.match("^HELO*.", input) and len(input.split()) >= 2:
            self.response = "250 %s Hello %s\r\n" % (serverIP, input.split()[1]) # TODO: Check response format
            self.next = WaitState(self.email)
            
    
class WaitState(State):
    '''
    Waits for 'MAIL FROM xxx' from client. ALl other messages except 'quit' are ignored.
    '''
    def __init__(self, email):
        super().__init__(email)
        self.response = "503 5.5.2 Need mail command\r\n"

        
    def parseInput(self, input):
        if self.isQuit(input): return
        if re.match("^MAIL FROM*.", input) and len(input.split()) >= 3:
            self.response = "250 2.1.0 Sender OK\r\n"
            self.next = MailFromState(self.email)
            self.email.buildEmail(input)
            
class MailFromState(State):
    '''
    Waits for 'RCPT TO xxx' from client. ALl other messages except 'quit' are ignored.
    '''
    
    def __init__(self, email):
        super().__init__(email)
        self.response = "503 5.5.2 Need rcpt command\r\n"
    
    def parseInput(self, input):
        if self.isQuit(input): return
        if re.match("^RCPT TO*.", input) and len(input.split()) >= 3:
            self.response = "250 2.1.5 Recipient OK\r\n"
            self.next = RcptToState(self.email)
            self.email.buildEmail(input)

class RcptToState(State):
    '''
    Waits for 'DATA' from client. ALl other messages except 'quit' are ignored.
    '''
    def __init__(self, email):
        super().__init__(email)
        self.response = "503 5.5.2 Need data command\r\n"
        
    def parseInput(self, input):
        if self.isQuit(input): return
        if re.match("^DATA.*", input):
            self.response = "354 Start mail input; end with <CRLF>.<CRLF>\r\n"
            self.next = Writing(self.email)

class Writing(State):
    '''
    Reads data into email body until '.' on its own line received.
    '''
    def __init__(self, email):
        super().__init__(email)
        self.response = ""   # No response sent while reading
        self.data = ""
        
    def parseInput(self, input):
        self.data += input
        if re.match("^\.", input):
            self.response = "250 Message received and to be delivered\r\n"
            self.next = Finished(self.email)
            print(self.data)
            self.email.buildEmail(self.data)

class Finished(State):
    '''
    This state indicates a completed email.
    '''
    def __init__(self, email):
        super().__init__(email)
        self.response = ""
        self.next = BeginState()
           

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
            self.connection.send(self.response.encode())
            
            if type(self.state) is Finished:
                complete_emails.append(self.state.getEmail())
                self.state = BeginState()
           
            if self.response == GOODBYE: break

        self.connection.close()
        
    def readData(self, input):
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
