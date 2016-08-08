#!/usr/bin/python

import sys
import os
from os.path import join, exists
from subprocess import check_output

class Package:
	def __init__(self, name = "", path = ""):
		self.name = name
		self.path = path
	def __repr__(self):
		return "{name: '%s', path: '%s'}" % (self.name, self.path)
	def __str__(self):
		return "name: '%s', path: '%s'" % (self.name, self.path)
		
class Folder:
	def __init__(self, name, extension, path):
		self.name = name
		if not extension.startswith("."):
		  extension = "." + extension
		self.extension = extension
		self.path = path
	def __repr__(self):
		return "{name: '%s', extension: '%s', path: '%s'}" % (self.name, self.extension, self.path)
	def __str__(self):
		return "name: '%s', extension: '%s', path: '%s'" % (self.name, self.extension, self.path)
        
class File:
	def __init__(self, name, extension, path, folder, package):
		self.name = name
		if not extension.startswith("."):
		  extension = "." + extension
		self.extension = extension
		self.path = path
		self.folder = folder
		self.package = package
	def needToBeMovedTo(self, folder):
		return self.folder.path != folder.path
	def __repr__(self):
		return "{name: '%s', extension: '%s', path: '%s', folder: {%s}, package: {%s}} " % (self.name, self.extension, self.path, self.folder, self.package)
	def __str__(self):
		return "name: '%s', extension: '%s', path: '%s', folder: {%s}, package: {%s}" % (self.name, self.extension, self.path, self.folder, self.package)

package = Package()

def move(file, folder):
	 if file.needToBeMovedTo(folder):
		  print "\t%s will be moved to %s directory!!" % (file.name, folder.path)
		  os.rename(file.path, folder.path + "/" + file.name)

def locate(extension, root = os.curdir, files = list()):
	global package
	for c in os.listdir(root):
		if c.startswith("."):
			continue;
		candidate = os.path.join(root, c)
		if not os.path.isfile(candidate):
			files = locate(extension, candidate, files)
		elif c.endswith(extension):
			folder = Folder(os.path.basename(root), extension, root)
			file = File(c, extension, os.path.join(root, c), folder, package)
			files.append(file)
	return files

def create(folder):
	if not os.path.exists(folder.path):
		 print "\tCreating inexistent folder %s" % folder.name
		 os.makedirs(folder.path)
	
def main(argv):
	global package
	if len(argv) < 3:
		sys.exit()
	package.name = sys.argv[1]
	package.path = check_output(["rospack", "find", package.name])[:-1]
	folders = list()
	i = 2
	j = 0
	while i < len(argv):
		name = argv[i]
		if name == "-e" and len(argv) > i + 1:
			folders[j - 1].extension = argv[i + 1]
			i += 1
		elif name == "-f" and len(argv) > i + 1:	
			name = argv[i + 1]
			folders[j - 1].name = name
			folders[j - 1].path = package.path + "/" + name
			i += 1
		elif not name.startswith("-"):
			folder = Folder(name, name, package.path + "/" + name)
			folders.append(folder)
			j += 1
		else:
			print "Input error!! There isn't a folder name(or an extension file) input argument after last '-f' (or '-e') input argument."
			sys.exit()
		i += 1
	print "Starting verifications in %s package" % package.name
	for folder in folders:
		create(folder)
		print "\nVerifying %s files" % folder.extension
		files = locate(folder.extension, package.path)
		# duplicated files must be verified yet
		for file in files:
			 print "\t%s @ %s" % (file.name, file.folder.path)
			 move(file, folder)
		del files[:]
	pass
	
if __name__ == "__main__":
	main(sys.argv)	
		
