from config import Config

class UserPerm:

	def __init__(self, client):
		self.client = client
		self.config = Config()
		self.log = self.client.log

	def checkPerm(self, user, level):
		try:
			configuser = 'user_' + user.lower()
			userlevel = self.config.getOption(configuser, 'level')
			if (userlevel == level):
				return True
			else:
				return False

		except Exception, err:
			print err
			return False