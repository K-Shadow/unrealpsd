from twisted.internet import protocol, reactor
from modules.core.logger import Logger
from modules.core.config import Config
from pseudoircprotocol import PseudoIRCProtocol
import copy

log = Logger()
conf = Config()

### Loading config settings and setting as variables ###
options = {}
options['servername'] = conf.getOption('server', 'name')
options['connectpass'] = conf.getOption('server', 'connectpass')
options['serverdesc'] = conf.getOption('server', 'description')
options['netname'] = conf.getOption('server', 'networkname')
options['linkserver'] = conf.getOption('link', 'server')
options['linkport'] = conf.getInt('link', 'port')
options['debugmode'] = conf.getBoolean('server', 'debug')

class PseudoIRCFactory(protocol.ClientFactory):

	def __init__(self):
		self.protocol = PseudoIRCProtocol(log, options)
		pass

	def buildProtocol(self, addr):
		return self.protocol
	
	def clientConnectionLost(self, connector, reason):
		log.output('Connection lost, reconnecting.')
		self.reloadmods = copy.copy(self.protocol.modhandler.modules)

		for module in self.protocol.modhandler.modules.keys():
			self.protocol.modhandler.unloadModule(module)
				
		connector.connect()

		for module in self.reloadmods:
			self.protocol.modhandler.loadModule(module)

	def clientConnectionFailed(self, connector, reason):
		reactor.stop()

log.output('UnrealPSD starting up.')
factory = PseudoIRCFactory()
reactor.connectTCP(options['linkserver'], options['linkport'], factory)
reactor.run()