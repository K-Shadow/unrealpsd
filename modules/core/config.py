from ConfigParser import SafeConfigParser
from logger import Logger

### Loads and parses the configuration file for the bot. ###

class Config:
    
    def __init__(self):
        self.log = Logger()
        
        try:
            self.conf = SafeConfigParser()
            self.file = 'unrealpsd.conf'
            self.conf.read(self.file)
        except:
            self.log.output('Error loading configuration file!')
            
    def getOption(self, section, option):
        try:
            return self.conf.get(section, option)
        except:
            self.log.output("Can\'t read configuration option!")
            
    def getInt(self, section, option):
        try:
            return self.conf.getint(section, option)
        except:
            self.log.output("Can\'t read configuration option!")

    def getBoolean(self, section, option):
        try:
            return self.conf.getboolean(section, option)
        except:
            self.log.output("Can\'t read configuration option!")
            
    def hasOption(self, section, option):
            return self.conf.has_option(section, option)
