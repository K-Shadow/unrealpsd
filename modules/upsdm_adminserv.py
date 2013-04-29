from upsdmodule import *
from core.config import Config
from twisted.internet import reactor
import string

class UPSDModule_adminserv(UPSDModule):

	modname = 'adminserv'
	modperm = 'master'

	def start(self):
		if not UPSDModule.start(self):
			return False

		self.conf = Config()
		self.userconf = {}

		### Load info for pseudo client from config ###
		self.userconf['nick'] = self.conf.getOption(self.modname, 'nick')
		self.userconf['ident'] = self.conf.getOption(self.modname, 'ident')
		self.userconf['host'] = self.conf.getOption(self.modname, 'host')
		self.userconf['modes'] = self.conf.getOption(self.modname, 'modes')
		self.userconf['realname'] = self.conf.getOption(self.modname, 'realname')
		self.userconf['mainchan'] = self.conf.getOption(self.modname, 'mainchan')

		self.proto.sendNickCreate(self.userconf['nick'], self.userconf['ident'], self.userconf['host'], self.userconf['modes'], self.userconf['realname'])
		self.proto.sendJoin(self.userconf['nick'], self.userconf['mainchan'])

		return True

	def stop(self):
		UPSDModule.stop(self)
		self.proto.sendUserQuit(self.userconf['nick'])

	def loadMod(self, destination, params):
		if (self.perm.checkPerm(destination, self.modperm)):
			if self.main.modhandler.loadModule(params[0]):
				self.proto.sendNotice(self.userconf['nick'], destination, 'Loaded module %s!' % (params[0]))

			else:
				self.proto.sendNotice(self.userconf['nick'], destination, 'Unable to load module %s.' % (params[0])) 

		return True

	def unloadMod(self, destination, params):
		if (self.perm.checkPerm(destination, self.modperm)) & (params[0] != self.modname):
			if self.main.modhandler.unloadModule(params[0]):
				self.proto.sendNotice(self.userconf['nick'], destination, 'Unloaded module %s!' % (params[0]))

			else:
				self.proto.sendNotice(self.userconf['nick'], destination, 'Unable to unload module %s.' % (params[0])) 
		else:
			self.proto.sendNotice(self.userconf['nick'], destination, 'You aren\'t allowed to use this command!')
			return False

		return True

	def reload(self, destination, params=None):
		if (self.perm.checkPerm(destination, self.modperm)):
			self.proto.sendNotice(self.userconf['nick'], destination, 'Reloading %s module!' % (self.modname))
			self.main.modhandler.reloadModule(self.modname)

		else:
			self.proto.sendNotice(self.userconf['nick'], destination, 'You aren\'t allowed to use this command!')
			return False

		return True

	def sendHelp(self, destination, params=None):
		if (self.perm.checkPerm(destination, self.modperm)):
			self.proto.sendNotice(self.userconf['nick'], destination, '\x02AdminServ Commands\x02:')
			self.proto.sendNotice(self.userconf['nick'], destination, '\x02LOADMOD <module>\x02 - Loads the specified module.')
			self.proto.sendNotice(self.userconf['nick'], destination, '\x02UNLOADMOD <module>\x02 - Unloads the specified module.')
			self.proto.sendNotice(self.userconf['nick'], destination, '\x02RELOAD\x02 - Reloads the AdminServ module.')

		else:
			self.proto.sendNotice(self.userconf['nick'], destination, 'You aren\'t allowed to use this command!')
			return False
			
		return True

	def adminserv_ctcp(self, user, command, params):
		if command.lower() == "\x01version\x01":
			self.proto.sendNotice(self.userconf['nick'], user, '\x01VERSION %s\x01' % (self.getVersion()))

		return True

	def adminserv_quit(self, user, command, params):
		print 'QUIT Detected!'
		return True

	def adminserv_channel(self, user, command, params):
		nick = params[0].split(':')[1]

		if (command == '.help'):
			if (self.perm.checkPerm(nick, self.modperm)):
				self.proto.sendMsg(self.userconf['nick'], user, 'Okay I\'ll help you ' + nick + '.')
				self.sendHelp(nick)

		elif (command == '.reload'):
			if (self.perm.checkPerm(nick, self.modperm)):
				self.proto.sendMsg(self.userconf['nick'], user, 'Okay, I\'ll only reload because I love you ' + nick + ".")
				self.reload(nick)

		return True

	def getModCommands(self):
		return ( 
				('loadmod', {
							'function': self.loadMod,
							'usage': '\x02Syntax\x02: LOADMOD <module>'
							}),
				('unloadmod', {
							'function': self.unloadMod,
							'usage': '\x02Syntax\x02: UNLOADMOD <module>'
							}),
				('reload', {
							'function': self.reload,
							'usage': '\x02Syntax\x02: RELOAD'
							}),
				('help', {
							'function': self.sendHelp,
							'usage': '\x02Syntax\x02: HELP'
							})
				)

	def getModHooks(self):
		return (('quit', self.adminserv_quit),
				('privmsg', self.adminserv_ctcp),
				('privmsg', self.adminserv_channel))

	def getVersion(self):
		return 'UnrealPSD AdminServ Module'