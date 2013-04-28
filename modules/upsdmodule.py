class UPSDModule(object):

	def __init__(self, proto, main):
		self.proto = proto
		self.main = main
		self.log = self.main.log
		self.config = self.main.config
		self.modstarted = False

	def start(self):
		if self.modstarted:
			return False

		self.modstarted = True
		return True

	def stop(self):
		if not self.modstarted:
			return

	def getModCommands(self):
		return ()

	def getModHooks(self):
		return ()

	def getVersion(self):
		return None