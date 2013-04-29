from upsdmodule import *
from core.config import Config

class UPSDModule_vhostserv(UPSDModule):

	modname = 'vhostserv'

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

	def vhostserv_ctcp(self, user, command, params):
		if command.lower() == "\x01version\x01":
			self.proto.sendNotice(self.userconf['nick'], user, '\x01VERSION %s\x01' % (self.getVersion()))

		return True

	def vhostserv_channel(self, user, command, params):
		nick = params[0].split(':')[1]

		if (len(params) > 4):
			args = params[4].split(' ')
		else:
			args = None

		if (command == ".request"):
			if (args == None) or (args[0] == ''):
				self.proto.sendMsg(self.userconf['nick'], user, 'No vHost was specified.')
			else:
				self.proto.chgUserHost(self.userconf['nick'], nick, args[0])
				self.proto.sendMsg(self.userconf['nick'], user, 'vHost for %s has been set.' % (nick))

	def getModHooks(self):
		return (('privmsg', self.vhostserv_ctcp),
				('privmsg', self.vhostserv_channel))

	def getVersion(self):
		return 'UnrealPSD vHostServ Module'