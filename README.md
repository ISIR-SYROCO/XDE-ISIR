XDE-ISIR EXPERIMENTAL:
======================

This repository contains all XDE-ISIR tools available

	git submodule init
	git submodule update
	mkdir _build
	cd _build
	cmake [-DCMAKE_INSTALL_PREFIX=path] [-DINSTALL_MODE=develop] ..
	make install


To update modules:

	git pull
	git submodule update
