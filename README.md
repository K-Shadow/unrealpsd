UnrealPSD
=========

UnrealPSD aims to be a modular pseudo server for UnrealIRCD based networks, as implementing bots 
in a pseudo server that links to the IRCd rather than connecting as a regular client allows for more
control and power for the bots/modules to take advantage of.

How to use:
==========
UnrealPSD so far only depends on Twisted, which is a networking library for Python.
After you acquire Twisted, follow these steps to get the pseudo server up and running:

1) Add a link block to your IRC server's unrealircd.conf to allow the pseudo server to link.

2) Edit unrealpsd.conf to match your network's configuration/settings you would like.

3) Now all you have to do is run unrealpsd.py and you're done!
