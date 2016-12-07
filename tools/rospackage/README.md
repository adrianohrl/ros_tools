# rospackage

Command line tools for working with ROS packages.

## Installation

for users:

	sudo python setup.py install

for developers:

	sudo python setup.py develop

## Usage

	rospackage build ...
	rospackage config ...
	rospackage create ...
	rospackage list ...
	rospackage organize -p test_pkg --all
	rospackage organize -p test_pkg -e yaml rviz -f config -e action launch msg srv