.PHONY: all setup clean_dist distro clean install install_user

NAME=rospackage
VERSION=`./setup.py --version`

all:
	echo "noop for debbuild"

setup:
	echo "building version ${VERSION}"

clean_dist:
	rm -rf dist
	rm -rf ${NAME}.egg-info

distro: setup clean_dist
	python setup.py sdist

clean: clean_dist
	echo "clean"

install: distro
	sudo checkinstall python setup.py install

install_user: distro
	sudo checkinstall --install=no python setup.py install --user
