from upsdmodule import *
from core.config import Config

class UPSDModule_testserv(UPSDModule):

	modname = 'testserv'

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

		self.proto.sendNickCreate(self.userconf['nick'], self.userconf['ident'], self.userconf['host'], self.userconf['modes'], self.userconf['realname'])
		self.proto.sendJoin(self.userconf['nick'], '#services')
		self.proto.sendMsg(self.userconf['nick'], '#services', 'Hello I am TestServ, a test module written for UnrealPSD!')

		return True

	def stop(self):
		UPSDModule.stop(self)
		self.proto.sendUserQuit(self.userconf['nick'])

	def testserv_ctcp(self, user, command, params):
		if command == "\x01VERSION\x01":
			self.proto.sendNotice(self.userconf['nick'], user, '\x01VERSION %s\x01' % (self.getVersion()))

		return True

	def testserv_channel(self, user, command, params):
		nick = params[0].split(':')[1]

		if (len(params) > 4):
			args = params[4].split(' ')
		else:
			args = None

		if (command == ".kick"):
			self.proto.sendKick(self.userconf['nick'], user, args[0], args[1])

	def getModHooks(self):
		return (('privmsg', self.testserv_ctcp),
				('privmsg', self.testserv_channel))

	def getVersion(self):
		return 'UnrealPSD TestServ Module'