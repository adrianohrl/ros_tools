#!/usr/bin/python
__author__ = 'Adriano Henrique Rossette Leite'

import argparse
import sys
import os
from os.path import join, exists
from subprocess import check_output

class Package:
	def __init__(self, name):
		self.name = name
		self.path = check_output(["rospack", "find", name])[:-1]
		self.extensions = {}
		self.folders = list()
		self.files_to_be_moved = list()
		self.duplicated_files = list()
		pass
	def __repr__(self):
		s = "{\n\tname: '%s',\n\tpath: '%s',\n\tfolders:" % (self.name, self.path)
		for folder in self.folders:
			s += "\n\t\t%s" % folder
		return s
	def __str__(self):
		s = "\tname: '%s',\n\tpath: '%s',\n\tfolders:" % (self.name, self.path)
		self.folders.sort(key=lambda x: x.name)
		for folder in self.folders:
			s += "\n%s" % folder
		if not self.isOrganized():
			self.duplicated_files.sort(key=lambda x: x.name)
			s += "\n\tduplicated files:"
			for file in self.duplicated_files:
				s += "\n\t\t%s" % file
		s += "\n\torganized: %s" % self.isOrganized()
		return s
	def appendFolder(self, folder):
		folder.package = self
		self.folders.append(folder)
	def appendFile(self, file, file_folder):
		if self.extensions[file.extension] != file_folder.name:
			self.files_to_be_moved.append(file)
		for folder in self.folders:
			if folder.path == file_folder.path:
				folder.appendFile(file)
				return
		file_folder.appendFile(file)
		self.folders.append(file_folder)
	def getFolder(self, folder_name):
		for folder in self.folders:
			if folder.name == folder_name:
				return folder
		return None
	def move(self, file, origin, destiny):
		if self.isDuplicated(file):
			self.duplicated_files.append(file)
		else:
			os.rename(file.path, os.path.join(destiny.path, file.name))
			package.appendFile(file, destiny)
		folder = self.getFolder(origin.name);
		if folder:
			folder.remove(file.name)
	def remove(self, folder_name):
		for i in range(len(self.folders)):
			if self.folders[i].name == folder_name:
				del self.folders[i]
				return
	def clear(self):
		self.files_to_be_moved = list()
	def isDuplicated(self, file):
		folder = self.getFolder(self.extensions[file.extension])
		return folder and folder.isDuplicated(file.name)
	def isOrganized(self):
		return len(self.files_to_be_moved) == 0 and len(self.duplicated_files) == 0

class Folder:
	def __init__(self, name, path):
		self.name = name
		self.path = path
		self.package = None
		self.files = list()
	def __repr__(self):
		try:
			path = self.package.name + '/' + self.name
		except:
			path = self.path
		return "%s @ %s: %s" % (self.name, path, self.files)
	def __str__(self):
		s = "\t\tname: '%s',\n\t\tpath: '%s',\n\t\tfiles:" % (self.name, self.path)
		self.files.sort(key=lambda x: x.name)
		for file in self.files:
			s += "\n\t\t\t%s" % file
		return s
	def appendFile(self, file):
		file.folder = self
		file.package = self.package
		self.files.append(file)
	def remove(self, file_name):
		for i in range(len(self.files)):
			if self.files[i].name == file_name:
				del self.files[i]
				return
	def isDuplicated(self, file_name):
		for file in self.files:
			if file.name == file_name:
				return True
		return False
	def isEmpty(self):
		return len(self.files) == 0
        
class File:
	def __init__(self, name, extension, folder):
		self.name = name
		if not extension.startswith("."):
			extension = "." + extension
		self.extension = extension
		self.path = os.path.join(folder.path, name)
		self.folder = None
		self.package = None
	def __repr__(self):
		try:
			path = self.package.name + '/' + self.folder.name + '/' + self.name
		except:
			path = self.path
		return "%s @ %s" % (self.name, path)
	def __str__(self):
		return "name: %s, path: %s" % (self.name, self.path)
	def needToBeMovedTo(self, folder):
		return folder and self.folder.path != folder.path

def move(file, folder, package, report):
	if file.needToBeMovedTo(folder):
		if package.isDuplicated(file):
			if report:
				print "[WARN] The %s file is duplicated in the %s package." % (file.name, package.name)
		package.move(file, file.folder, folder)
		if report:
			print "[INFO] The %s file was moved to %s directory." % (file.name, folder.path)

def create(folder_name, package, report):
	folder = package.getFolder(folder_name)
	if not folder:
		folder_path = os.path.join(package.path, folder_name)
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
			if report:
				if os.path.exists(folder_path):
					print "[INFO] The %s folder was created at %s." % (folder_name, folder_path)
				else:
					print "[ERROR] The %s folder could not be created at %s." % (folder_name, folder_path)
					sys.exit(2)
			folder = Folder(folder_name, os.path.join(package.path, folder_name))
			package.appendFolder(folder)
	return folder

def locate(package, extension, root = os.curdir, files = list()):
	for c in os.listdir(root):
		if c.startswith("."):
			continue
		candidate = os.path.join(root, c)
		if not os.path.isfile(candidate):
			files = locate(package, extension, candidate, files)
		elif c.endswith(extension):
			folder = Folder(os.path.basename(root), root)
			file = File(c, extension, folder)
			package.appendFile(file, folder)
			files.append(file)
	return files
	
def organize(package, report):
	if report:
		print "Processing %s package..." % package.name
	for extension, folder_name in package.extensions.items():
		files = locate(package, extension, package.path)
		if not files:
			if report:
				print "[WARN] None %s file was found in the %s package." % (extension.upper(), package.name)
		else:
			if not package.files_to_be_moved:
				if report:
					print "[INFO] All %s file is located at their proper folder (%s) in the %s package." % (extension.upper(), folder_name, package.name)
			else:
				folder = create(folder_name, package, report)	
				for file in package.files_to_be_moved:
				 	move(file, folder, package, report)
				package.clear()
		del files[:]
	for folder in package.folders:
		if folder.isEmpty():
			package.remove(folder.name)
	pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description='organize_pkg will locate PACKAGE and gather the EXTENSION(s) files into their'
			'respective FOLDER. If a EXTENSION file is found out of its proper FOLDER, it will be'
			'replaced to there.'
	)
	parser.add_argument(
		'-p',
		'--packages',
		type=str,
		nargs='+',
		dest='packages',
		metavar='PACKAGE',
		required=True,
		help='specify the ROS package in which this operation will be done.'
	)
	parser.add_argument(
		'-a', 
		'--all', 
		action='store_true', 
		help='gather all the .CONFIG, .MACHINE, .RVIZ, .URDF, .XACRO, and .YAML files of the'
			'PACKAGE into the CONFIG folder (if necessary, it is created); as well as, gather'
			'all the .ACTION, .BAG, .LAUNCH, .MAP, .MMSG, .MSG, and .SRV files into their'
			'respective folder (whose name is equal to their files extension).'
	)
	parser.add_argument(
		'-e', 
		'--extension', 
		action='append', 
		type=str, 
		nargs='+',
		#choices=['action','bag','config','launch','map','mmsg','msg','srv','rviz','urdf','xacro','yaml'], 
		dest='extensions',
		metavar='EXTENSION', 
		default=list(),
		help='specify the EXTENSION(s) files to be gathered into a FOLDER. If FOLDER is not'
			'given, the EXTENSION(s) files will be replaced to a folder whose name is equal'
			'to the EXTENSION of their inner files.'
	)
	parser.add_argument(
		'-f', 
		'--folder', 
		action='append', 
		type=str,  
		dest='folders',
		metavar='FOLDER',
		default=list(),
		help='specify the FOLDER in which the EXTENSION(s) files will to replaced to (if needed).'
	)
	parser.add_argument(
		'-q', 
		'--quiet', 
		action='store_true', 
		help='quiets error reports.'
	)
	args = parser.parse_args()
	if args.all or len(args.extensions) == 0:
		expression = list()
		expression.append('-p')
		expression.extend(args.packages)
		expression.extend(['-e', 'config', 'rviz', 'urdf', 'xacro', 'yaml', '-f', 'config'])
		expression.extend(['-e', 'action', 'bag', 'launch', 'map', 'mmsg', 'msg', 'srv'])
		if args.quiet:
			expression.append('-q')
		args = parser.parse_args(expression)
	report = not args.quiet
	packages = list()
	for package_name in args.packages:
		try:
			package = Package(package_name)
		except:
			if report: 
				print "[ERROR] %s is not a ROS package." % package_name
			continue
		for i in range(len(args.extensions)):
			if i < len(args.folders):
				folder_name = args.folders[i];
			for folder_extension in args.extensions[i]:
				if folder_extension.startswith("."):
					if report:
						print "[ERROR] The extension names must be entered with not dot."
					continue
					folder_extension = folder_extension
				if i >= len(args.folders):
					folder_name = folder_extension
				package.extensions["." + folder_extension] = folder_name
		if len(package.extensions) == 0:
			if report: 
				print "None folder."
			sys.exit(2)
		organize(package, report)
		packages.append(package)

	if not packages:
		if report: 
			print "[ERROR] None valid ROS package."
		sys.exit(2)

	if report:
		print "\nReporting..."
		print "packages:"
		for package in packages:
			print package
		print "End of report.\n"