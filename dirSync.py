#!/usr/bin/python
# dirSync.py

import os
import sys
from os.path import *
from filecmp import *
from time import strftime
import shutil

fileCount = 0
dirCount = 0
verbose = False

def dirCompare(dir1, dir2):
	"""Compare dir1 to dir2."""
	if not exists(dir1):
		print("Path does not exist:", dir1)
		return
	if not exists(dir2):
		print("Path does not exist:", dir2)
		return

	dc = dircmp(dir1,dir2,[],[])
	if verbose:
		dc.report()
		print dc.left_only
	
	# Iterate through the files and directories only in dir1.
	for node in dc.left_only:
		if isdir(join(dir1,node)):
			copyDir(join(dir1,node), join(dir2,node))
		else:
			# Assume node is a file.
			copyFile(join(dir1,node), dir2)
	
	# Iterate through the common files making sure they are up to date.
	for node in dc.common_files:
		# Do a shallow comparison (stat vs. bit by bit) of files.
		if not cmp(join(dir1,node), join(dir2,node)):
			# Determine if node is older in dir2.
			dir1stat = os.stat(join(dir1,node))
			dir2stat = os.stat(join(dir2,node))
			if dir1stat.st_mtime > dir2stat.st_mtime:
				# The file is old, copy over the new version.
				copyFile(join(dir1,node), dir2)
		
	# Recurse through the directories to make sure they are up to date.
	for node in dc.common_dirs:
		dirCompare(join(dir1,node), join(dir2,node))
	
def copyDir(dir1, dir2):
	"""Copy dir1 to dir2."""
	global dirCount
	if verbose:
		print("Copying directory \"%s\" to \"%s\"..." % (dir1, dir2))
		sys.stdout.flush()
	
	shutil.copytree(dir1, dir2)

	if verbose:
		print("Done.")
		sys.stdout.flush()
	
	dirCount = dirCount + 1
	return
	
def copyFile(file1, dir2):
	"""Copy file1 to dir2."""
	global fileCount
	if verbose:
		print("Copying file \"%s\" to \"%s\"..." % (file1, dir2))
		sys.stdout.flush()
	
	shutil.copy2(file1, dir2)

	if verbose:
		print("Done.")
		sys.stdout.flush()
	
	fileCount = fileCount + 1
	return

if __name__ == '__main__':
	# Being run stand alone.
	startTime = strftime("%H:%M:%S")
	print("Starting at: %s" % startTime)
	sys.stdout.flush()
	
	# Note: Paths using "\" need to be written with "\\" instead.
	dir1 = "/Volumes/MacTB1/Photos"
	dir2 = "/Volumes/MacTB2/Photos"
	print("Comparing \"%s\" with \"%s\"..." % (dir1, dir2))
	sys.stdout.flush()
	dirCompare(dir1,dir2)
	sys.stdout.flush()

	print("Copied %d directories and %d individual files." % (dirCount, fileCount))
	endTime = strftime("%H:%M:%S")
	print("Started at: %s" % startTime)
	print("Ended at: %s" % endTime)
	