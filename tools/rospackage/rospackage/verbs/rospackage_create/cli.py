from __future__ import print_function

import os
from os.path import exists, join

from osrf_pycommon.terminal_color import print_color

from catkin_pkg.package_templates import create_package_files, PackageTemplate
from catkin_pkg.package import package_exists_at

def prepare_arguments(parser):
    parser.description="This verb is used to create an organized ROS packages."
    parser.add_argument('name', nargs=1, help='The name for the package')
    parser.add_argument('--meta', action='store_true', help='Creates meta-package files')
    parser.add_argument('dependencies', nargs='*', help='Catkin package Dependencies')
    parser.add_argument('-s', '--sys-deps', nargs='*', help='System Dependencies')
    parser.add_argument('-b', '--boost-comps', nargs='*', help='Boost Components')
    parser.add_argument('-V', '--pkg_version', action='store', help='Initial Package version')
    parser.add_argument('-D', '--description', action='store', help='Description')
    parser.add_argument('-l', '--license', action='append', help='Name for License, (e.g. BSD, MIT, GPLv3...)')
    parser.add_argument('-a', '--author', action='append', help='A single author, may be used multiple times')
    parser.add_argument('-m', '--maintainer', action='append', help='A single maintainer, may be used multiple times')
    rosdistro_name = os.environ['ROS_DISTRO'] if 'ROS_DISTRO' in os.environ else None
    parser.add_argument('--rosdistro', required=rosdistro_name is None, default=rosdistro_name, help='The ROS distro (default: environment variable ROS_DISTRO if defined)')
    return parser


def main(options):

	parent_path = os.getcwd()
	print("parent path: %s" % parent_path)
	package_name = options.name[0]
	print("package name: %s" % package_name)
	package_path = os.path.join(parent_path, package_name)
	print("package path: %s" % package_path)
	print_color("@!@{green}==>@|@! Creating %s package..." % package_name)
	try:
		package_template = PackageTemplate._create_package_template(
			package_name=package_name,
			description=options.description,
			licenses=options.license or [],
			maintainer_names=options.maintainer,
			author_names=options.author,
			version=options.pkg_version,
			catkin_deps=options.dependencies,
			system_deps=options.sys_deps,
			boost_comps=options.boost_comps
		)
		create_package_files(target_path=package_path,
			package_template=package_template,
			rosdistro=options.rosdistro,
			newfiles={},
			meta=options.meta
		)
		print('Successfully created files in %s. Please adjust the values in package.xml.' % package_path)
	except ValueError as vae:
		print_color("@{red}[ERROR] %s" % vae)

	if not package_exists_at(package_path):
		print_color("@{red}[ERROR] The %s package was not created." % package_name)
		return 1
	print_color("[INFO] The %s package was created." % package_name)

	folders = ['include', 'include/%s' % package_name, 'src', 'src/%s' % package_name,
		'action', 'config', 'launch', 'msg', 'mmsg', 'srv']
	print_color("@!@{green}==>@|@! Organizing package...")
	for folder_name in folders:
		folder_path = os.path.join(package_path, folder_name)
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
			print_color("[INFO] The %s folder was created in the %s package." % (folder_name, package_name))

	return 0