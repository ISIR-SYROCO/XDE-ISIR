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

To update everything:
---------------------

	git pull
	git submodule update

To commit change:
-----------------

To update the global XDE-ISIR, you have to update the submodule first,
then tell XDE-ISIR to use the new version of the submodule by adding it.

Example:

In a submodule directory (for example XDE-WorldManager):

    git add something
    git commit -m "Fix something"
    git push
    cd ..
    git add XDE-WorldManager
    git commit -m "Update XDE-WorldManager"
    git push
