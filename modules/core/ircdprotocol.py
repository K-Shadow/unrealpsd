from misc import Misc

### Class to handle the various commands of the protocol for UnrealIRCd ###

class IRCDProtocol:

	def __init__(self, client, config):
		self.client = client
		self.misc = Misc()
		self.protover = 2311
		self.config = config

	### Initial protocol messages ###
	def sendInitial(self):
		self.client.transport.write('PROTOCTL NICKv2\r\n')
		self.client.transport.write('PASS :%s\r\n' % (self.config['connectpass']))
		self.client.transport.write('SERVER %s 1 :%s\r\n' % (self.config['servername'], self.config['serverdesc']))
		self.client.transport.write('NETINFO 0 %s %s * 0 0 0 :%s\r\n' % (self.misc.getUTCTime(), self.protover, self.config['netname']))
		self.client.transport.write('EOS\r\n')

	### Responds to PING messages from other servers ###
	def sendPong(self, destination):
		self.client.transport.write('PONG %s %s\r\n' % (self.config['servername'], destination))

	### Sends information about a user on the server (or pseudo client in this case) ###
	def sendNickCreate(self, nick, username, hostname, usermodes, realname):
		self.client.transport.write('NICK %s 1 %s %s %s %s 0 %s * :%s \r\n' % (nick, self.misc.getUTCTime(), 
			username, hostname, self.config['servername'], usermodes, realname))

	### Used for sending notices to users through pseudo clients ###
	def sendNotice(self, nick, destination, message):
		self.client.transport.write(':%s NOTICE %s :%s\r\n' % (nick, destination, message))

	### Sends quit message to disconnect a pseudo client ###
	def sendUserQuit(self, nick, reason='Module unloaded.'):
		self.client.transport.write(':%s QUIT :%s\r\n' % (nick, reason))

	### Sends a join channel notification ###
	def sendJoin(self, user, channel):
		self.client.transport.write(':%s JOIN %s\r\n' % (user, channel))

	### Sends a message to a user/channel ###
	def sendMsg(self, user, destination, message):
		self.client.transport.write(':%s PRIVMSG %s :%s\r\n' % (user, destination, message))

	### Sends channel kick message ###
	def sendKick(self, kickuser, channel, user, reason):
		self.client.transport.write(':%s KICK %s %s :%s\r\n' % (kickuser, channel, user, reason))

	### Changes a user's host ###
	def chgUserHost(self, user, targetuser, host):
		self.client.transport.write(':%s CHGHOST %s %s\r\n' % (user, targetuser, host))

	### Handles PRIVMSG commands ###
	def irc_PRIVMSG(self, cmd):
		dest = cmd[2]
		command = cmd[3].split(':')[1]
		
		if len(cmd) > 4:
			args = cmd[4].split(' ')
		else:
			args = None

		### Handles PRIVMSGs that aren't in channels or CTCP requests ###
		if dest.startswith('#') != True and command.startswith('\x01') != True:
			command = cmd[2].lower() + '.' + command.lower()
			dest = cmd[0].split(':')[1]

			if (command in self.client.modhandler.cmds):
				hook = self.client.modhandler.cmds[command]
							
				try:
					hook['function'](dest, args)
				except:
					self.sendNotice(cmd[2], dest, hook['usage'])

			else:
				self.sendNotice(cmd[2], dest, 'Unknown command: %s' % (command.split('.')[1]))

		### CTCP request hooking ###
		elif command.startswith('\x01'):
			dest = cmd[0].split(':')[1]
			self.client.modhandler.callHook('privmsg', dest, command, cmd)

		### Channel message hooking ###
		elif dest.startswith('#') & command.startswith('\x01') != True:
			self.client.modhandler.callHook('privmsg', dest, command, cmd)

	### Handles PING commands ###
	def irc_PING(self, cmd):
		self.sendPong(cmd[1])


