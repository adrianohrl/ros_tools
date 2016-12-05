from __future__ import print_function

import os
from os.path import exists, join

from rospkg import RosPack

from osrf_pycommon.terminal_color import print_color

class Package:

	def __init__(self, name):
		self.name = name
		rospack = RosPack()
		self.path = rospack.get_path(name)
		self.extensions = {}
		self.folders = list()
		self.files_to_be_moved = list()
		self.duplicated_files = list()
		pass

	def __repr__(self):
		s = "\n\tname: %s,\n\tpath: %s,\n\tfolders:" % (self.name, self.path)
		for folder in self.folders:
			s += "\n\t\t%s" % folder
		return s

	def __str__(self):
		return "name: %s, path: %s" % (self.name, self.path)

	def pretty(self):
		s = "\tname: %s,\n\tpath: %s,\n\tfolders:" % (self.name, self.path)
		self.folders.sort(key=lambda x: x.name)
		for folder in self.folders:
			s += "\n%s" % folder.pretty()
		if not self.is_organized():
			self.duplicated_files.sort(key=lambda x: x.name)
			s += "\n\tduplicated files:"
			for file in self.duplicated_files:
				s += "\n\t\t%s" % file.pretty()
		s += "\n\torganized: %s" % self.is_organized()
		return s

	def append_folder(self, folder):
		folder.package = self
		self.folders.append(folder)

	def append_file(self, file, file_folder):
		if self.extensions[file.extension] != file_folder.name:
			self.files_to_be_moved.append(file)
		for folder in self.folders:
			if folder.path == file_folder.path:
				folder.append_file(file)
				return
		file_folder.append_file(file)
		self.folders.append(file_folder)

	def get_folder(self, folder_name):
		for folder in self.folders:
			if folder.name == folder_name:
				return folder
		return None

	def move(self, file, origin, destiny):
		if self.is_duplicated(file):
			self.duplicated_files.append(file)
		else:
			os.rename(file.path, os.path.join(destiny.path, file.name))
			self.append_file(file, destiny)
		folder = self.get_folder(origin.name);
		if folder:
			folder.remove(file.name)

	def remove(self, folder_name):
		for i in range(len(self.folders)):
			if self.folders[i].name == folder_name:
				del self.folders[i]
				return

	def clear(self):
		self.files_to_be_moved = list()

	def is_duplicated(self, file):
		folder = self.get_folder(self.extensions[file.extension])
		return folder and folder.is_duplicated(file.name)

	def is_organized(self):
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
		try:
			path = self.package.name + '/' + self.name
		except:
			path = self.path
		return "name: %s, path: %s" % (self.name, path)

	def pretty(self):
		s = "\t\tname: '%s',\n\t\tpath: '%s',\n\t\tfiles:" % (self.name, self.path)
		self.files.sort(key=lambda x: x.name)
		for file in self.files:
			s += "\n\t\t\t%s" % file.pretty()
		return s

	def append_file(self, file):
		file.folder = self
		file.package = self.package
		self.files.append(file)

	def remove(self, file_name):
		for i in range(len(self.files)):
			if self.files[i].name == file_name:
				del self.files[i]
				return

	def is_duplicated(self, file_name):
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
		try:
			path = self.package.name + '/' + self.folder.name + '/' + self.name
		except:
			path = self.path
		return "name: %s, path: %s" % (self.name, self.path)

	def pretty(self):
		return "name: %s, path: %s" % (self.name, self.path)

	def need_to_be_moved_to(self, folder):
		return folder and self.folder.path != folder.path


def move(file, folder, package, report):
	if file.need_to_be_moved_to(folder):
		if package.is_duplicated(file):
			if report:
				print_color("@{yellow}[WARN] The %s file is duplicated in the %s package." % (file.name, package.name))
		package.move(file, file.folder, folder)
		if report:
			print_color("[INFO] The %s file was moved to %s directory." % (file.name, folder.path))


def create(folder_name, package, report):
	folder = package.get_folder(folder_name)
	if not folder:
		folder_path = os.path.join(package.path, folder_name)
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
			if report:
				print_color("[INFO] The %s folder was created at %s." % (folder_name, folder_path))
			folder = Folder(folder_name, os.path.join(package.path, folder_name))
			package.append_folder(folder)
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
			package.append_file(file, folder)
			files.append(file)
	return files