XDE-ISIR:
=========

Install:
--------
This repository contains all XDE-ISIR tools available

    git clone https://github.com/XDE-ISIR/XDE-ISIR.git
	git submodule init
	git submodule update
	mkdir _build
	cd _build
	cmake [-DCMAKE_INSTALL_PREFIX=path] [-DINSTALL_MODE=develop] ..
	make install

To update everything:
---------------------

	git pull
	git submodule update

XDE-ISIR EXPERIMENTAL:
======================

Cloning the repository:
-----------------------

In order to clone this repository do:

    git clone --recursive --branch experimental https://github.com/XDE-ISIR/XDE-ISIR.git

Install in python:
------------------

Run setup script:

    python setup.py install --prefix=path
or 

    python setup.py develop --prefix=path

