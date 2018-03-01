'''
Created on Feb 28, 2018

@author: Brian
'''

from socket import *
from HW04_email import *

SERVER_PORT = 5031
EMPTY = ''


class EmailBuilder:
    
    def __init__(self):        
        self.domain = EMPTY
        self.mailFrom = EMPTY
        self.rcptTo = EMPTY
        self.subject = EMPTY
        self.body = EMPTY
        
    def promptDomain(self):
        self.domain = input("Enter email server domain: ")
        print()
        
    def promptMailFrom(self):
        self.mailFrom = input("From: ")
        print()
    
    def promptRcptTo(self):
        self.rcptTo = input("To: ")
        print()
        
    def promptSubject(self):
        self.subject = input("Subject: ")
        
    def promptBody(self, body = ""):
        if body != '':
            text = input()
        else:
            text = input("Enter the message body, followed by a '.' on the last line.\n")
        body += text
        if text == '.':
            self.body = body
            return
        self.promptBody(body)
        
def promptServerAddress():
    #TODO: Validation
    addr = input("Enter server address: ")
    
    return addr

def buildEmail():
    builder = EmailBuilder()
    
    builder.promptDomain()
    builder.promptMailFrom()
    builder.promptRcptTo()
    builder.promptSubject()
    builder.promptBody()
    
    return builder

if __name__ == "__main__":
    sock_obj = socket(AF_INET, SOCK_STREAM)
    addr = promptServerAddress()
    sock_obj.bind((addr, SERVER_PORT))
    
    email = buildEmail()
    