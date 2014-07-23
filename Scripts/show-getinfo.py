#!/usr/bin/env python

import sys, os
# Rather than mess around with subprocesses, we'll just use PyObjC
from Foundation import *

# Grab our list of files (linebreak delimited list)
input = sys.stdin.read()
files = input.splitlines(False)

# Configure out AppleScript to activate Finder and open the Get Info window for each file/folder
script = "tell application \"Finder\"\n\tactivate\n"
haveFile = False

for path in files:
	if not os.path.exists(path):
		print('No such path: ' + path)
		continue
	elif not haveFile:
		haveFile = True
	# Make sure that we have the right type of resource
	pathType = 'folder' if os.path.isdir(path) else 'file'
	sanePath = path.replace('"', '\\"')
	script = script + "\tset macpath to POSIX file \"%s\" as text\n\topen information window of %s macpath\n" % (sanePath, pathType)

script = script + "end tell"

# If we have at least one file/folder, run the AppleScript
if haveFile:
	s = NSAppleScript.alloc().initWithSource_(script)
	s.executeAndReturnError_(None)
