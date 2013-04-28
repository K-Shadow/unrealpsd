import sys

class ModuleHandler:

	def __init__(self, client):
		self.client = client
		self.log = self.client.log
		self.modules = {}
		self.hooks = {}
		self.cmds = {}

	def loadModule(self, module):
		if module in self.modules:
			self.log.output('Module %s is already loaded!' % (module))
			return False

		try:
			modname = 'upsdm_' + module
			mod = __import__("modules." + modname)
			mod = eval("mod." + modname)
			modinstance = getattr(mod, 'UPSDModule_' + module) (self.client.proto, self.client)

		except Exception, err:
			self.log.output('Error loading %s module: %s' % (module, err))
			return False

		self.modules[module] = modinstance

		try:
			for cmd, cmd_dict in modinstance.getModCommands():
				self.addCommand(module, cmd, cmd_dict)

			for hook, function in modinstance.getModHooks():
				self.addHook(hook, function)

			modinstance.start()
			self.log.output('Loaded %s module.' % (module))
			return True

		except Exception, err:
			self.log.output('Error starting %s module: %s' % (module, err))
			self.unloadModule(module)

	def unloadModule(self, module):
		if module not in self.modules:
			self.log.output('Module %s is not loaded!' % (module))
			return False

		modinstance = self.modules[module]

		try:
			for hook, function in modinstance.getModHooks():
				self.hooks[hook].remove(function)

			for cmd, cmd_dict in modinstance.getModCommands():
				cmd = module + "." + cmd
				del self.cmds[cmd]
				
			modinstance.stop()
			sys.modules.pop("modules.upsdm_" + module)
			self.log.output('Module %s has been unloaded.' % (module))

		except Exception, err:
			self.log.output('Error shutting down and unloading module %s: %s' % (module, err))
			return False

		del self.modules[module]
		return True

	def reloadModule(self, module):
		self.unloadModule(module)
		self.loadModule(module)

	def addCommand(self, cmd_module, cmd_name, cmd_dict):
		cmd_name = cmd_module + "." + cmd_name
		self.cmds.update({cmd_name:cmd_dict})

	def addHook(self, hook, function):
		if not self.hooks.has_key(hook):
			self.hooks.update({hook:[]})

		self.hooks[hook].append(function)

	def callHook(self, hook, prefix, command, params):
		if not hook in self.hooks:
			return

		for func in self.hooks[hook]:
			try:
				func(prefix, command, params)
			except:
				return