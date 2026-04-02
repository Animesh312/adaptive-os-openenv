animesh@Animesh:~/Projects/adaptive-os-openenv$ sudo add-apt-repository ppa:deadsnakes/ppa
 This PPA contains more recent Python versions packaged for Ubuntu.

Disclaimer: there's no guarantee of timely updates in case of security problems or other issues. If you want to use them in a security-or-otherwise-critical environment (say, on a production server), you do so at your own risk.

Update Note
===========
Please use this repository instead of ppa:fkrull/deadsnakes.

Reporting Issues
================

Issues can be reported in the master issue tracker at:
https://github.com/deadsnakes/issues/issues

Supported Ubuntu and Python Versions
====================================

- Ubuntu 22.04 (jammy) Python3.7 - Python3.9, Python3.11 - Python3.13
- Ubuntu 24.04 (noble) Python3.7 - Python3.11, Python3.13
- Note: Python 3.10 (jammy), Python3.12 (noble) are not provided by deadsnakes as upstream ubuntu provides those packages.

Why some packages aren't built:
- Note: for jammy and noble, older python versions requre libssl<3 so they are not currently built
- If you need these, reach out to asottile to set up a private ppa

The packages may also work on other versions of Ubuntu or Debian, but that is not tested or supported.

Packages
========

The packages provided here are loosely based on the debian upstream packages with some modifications to make them more usable as non-default pythons and on ubuntu.  As such, the packages follow debian's patterns and often do not include a full python distribution with just `apt install python#.#`.  Here is a list of packages that may be useful along with the default install:

- `python#.#-dev`: includes development headers for building C extensions
- `python#.#-venv`: provides the standard library `venv` module
- `python#.#-distutils`: provides the standard library `distutils` module
- `python#.#-lib2to3`: provides the `2to3-#.#` utility as well as the standard library `lib2to3` module
- `python#.#-gdbm`: provides the standard library `dbm.gnu` module
- `python#.#-tk`: provides the standard library `tkinter` module

Third-Party Python Modules
==========================

Python modules in the official Ubuntu repositories are packaged to work with the Python interpreters from the official repositories. Accordingly, they generally won't work with the Python interpreters from this PPA. As an exception, pure-Python modules for Python 3 will work, but any compiled extension modules won't.

To install 3rd-party Python modules, you should use the common Python packaging tools.  For an introduction into the Python packaging ecosystem and its tools, refer to the Python Packaging User Guide:
https://packaging.python.org/installing/

Sources
=======
The package sources are available at:
https://github.com/deadsnakes/

Nightly Builds
==============

For nightly builds, see ppa:deadsnakes/nightly https://launchpad.net/~deadsnakes/+archive/ubuntu/nightly
 More info: https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa
Press [ENTER] to continue or Ctrl-c to cancel adding it.

Hit:1 http://in.archive.ubuntu.com/ubuntu focal InRelease           
Get:2 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu focal InRelease [18.1 kB]
Hit:3 http://in.archive.ubuntu.com/ubuntu focal-updates InRelease              
Hit:4 http://security.ubuntu.com/ubuntu focal-security InRelease               
Hit:5 http://in.archive.ubuntu.com/ubuntu focal-backports InRelease            
Fetched 18.1 kB in 2s (10.9 kB/s)
Reading package lists... Done
Now do to start virtual enviornment of ->source venv/bin/activate

animesh@Animesh:~/Projects/adaptive-os-openenv$ 

pip list | grep openenv
Docker build invoking process
docker build -t adaptive-os .
docker run -p 7860:7860 adaptive-os
curl -X POST http://localhost:7860/reset
git remote set-url origin https://github.com/Animesh312/adaptive-os-openenv.git