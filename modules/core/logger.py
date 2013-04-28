from time import strftime, localtime

### Handles formatting output to console with timestamps. ###

class Logger:
    
    def __init__(self):
        pass
    
    def output(self, data):
        out = '['+ self.getLocalTime() +'] '+ data
        print out
        
    def getLocalTime(self):
        return strftime('%a, %d %b %Y %X', localtime())