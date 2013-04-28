from modules.core.ircdprotocol import IRCDProtocol
from modules.modulehandler import ModuleHandler
from twisted.internet import protocol
import sys

class PseudoIRCProtocol(protocol.Protocol):

	def __init__(self, log, config):
		self.log = log
		self.config = config
		self.proto = IRCDProtocol(self, self.config)
		self.modhandler = ModuleHandler(self)

	def dataReceived(self, data):
		for l in data.split('\r\n'):
			cmd = l.split(' ')
			
			try:
				if cmd[0] == 'PING':
					self.proto.irc_PING(cmd)	

				if cmd[1] == "PRIVMSG":
					cmd = l.split(' ', 4)
					self.proto.irc_PRIVMSG(cmd)

				if cmd[1] == "QUIT":
					self.modhandler.callHook('quit', cmd[0], cmd[2])

			except:
				pass

			if self.config['debugmode']:
				self.log.output('[PROTOCOL]: ' + l)

	def connectionMade(self):
		self.log.output('Linked to %s:%s.' % (self.config['linkserver'], self.config['linkport']))
		self.proto.sendInitial()
		self.modhandler.loadModule('adminserv')
	