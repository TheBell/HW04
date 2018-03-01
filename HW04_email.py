'''
Created on Feb 28, 2018

@author: b_e_l
'''
import re

def validateEmailAddress(addr):
    # Regex from http://emailregex.com/
    return re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", input)

class Email:
    def __init__(self):
        self.mailFrom = False
        self.rcptTo = False
        self.data = False
        
    def buildEmail(self, input):
        if not input: return False
        
        if re.match("^MAIL FROM .*", input):
            self.mailFrom = re.match("^MAIL FROM (.*)", input).group(1)
        
        elif re.match("^RCPT TO .*", input):
            self.rcptTo = re.match("^RCPT TO (.*)", input).group(1)
        
        else:
            self.data = input
            
        return True
        
        
    def isComplete(self):
        return self.mailFrom and self.rcptTo and self.data
    
    def getFullEmail(self):
        # TODO: Finish proper format
        return "%s\r\n%s\r\n%s\r\n" (self.mailFrom, self.rcptTo, self.data)
        
        