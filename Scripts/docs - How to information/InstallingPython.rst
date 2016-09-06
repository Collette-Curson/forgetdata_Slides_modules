
Documentation of Slides - Installation of Python/Sphinx and Documenting modules
===============================================================================

Installing Python:
==================
The latest version is currently version 2.7.8.

The latest version of Python can be downloaded and installed from https:/www.python.org/downloads/windows/


Link to media.readthedocs which is a useful guide for using python:  https://media.readthedocs.org/pdf/python-guide/latest/python-guide.pdf



Installation Help: 
------------------
Help is available on the same link – see latest version link.  

* The HELP chm files cannot be viewed by default – see http:/stackoverflow.com/questions/11438634/opening-a-chm-file-produces-navigation-to-the-webpage-was-canceled for more information.  
* The short cut is to save chm to local folder, right-click and select Properties, and select Unblock on the General tab.

Installation Path:
------------------
The default installation path is C:/Python27/, and this can be optionally added to the Path during the installation. 

Documentation:
--------------
Latest Documentation is available here: http:/docs.python.org.

Checking that Python is installed correctly:
--------------------------------------------

#. Open a command prompt:
#. Check that Python is on your path, type:

| C:>Python

If this is not recognised, type:

| set path=%path%;C:/python27

Running Python should return the following:

| C:>python
| Python 2.7.8 (default, Jun 30 2014, 16:03:49) [MSC v.1500 32 bit (Intel)] on win32
| Type "help", "copyright", "credits" or "license" for more information.
| >>>

Python is now installed correctly

Modules:
--------

The default Python library would be installed to C:/Python27/Lib/.
Third-party modules should be stored in C:/Python27/Lib/site-packages/.

(Other modules are installed to C:/Python27/Scripts)

PYTHONPATH environment variable:
--------------------------------
PYTHONPATH can be used to define an alternative module path. See environment variables here https:/docs.python.org/2.7/using/cmdline.html#envvar-PYTHONPATH

sys.path uses this PYTHONPATH to define where the default modules and site-packages are found.



Installing multiple versions or copies of Python:
=================================================


Making a Python virtual environment. (virtualenv)
-------------------------------------------------

For full details on installation and uses for virtualenv, see: http:/virtualenv.readthedocs.org/en/latest/virtualenv.html

Virtualenv
^^^^^^^^^^
virtualenv is a tool to create isolated Python environments.
The basic problem being addressed is one of dependencies and versions, and indirectly permissions. Imagine you have an application that needs different versions of Python or it’s modules. How can you use both these applications? It’s easy to end up in a situation where you unintentionally upgrade an application.
virtualenv creates an environment that has its own installation directories, that doesn’t share libraries with other virtualenv environments.

PIP
^^^
"pip" is a package management system used to install and manage software packages written in Python. Many packages can be found in the Python Package Index (PyPI).
pip.exe is installed with Python.
pip install options can be found here: https:/pip.pypa.io/en/latest/reference/pip_install.html#cmdoption-t

Note: if pip is not installed for some reason, see here: http:/pip.readthedocs.org/en/latest/installing.html - download get-pip.py, and run python get-pip.py
When running pip install manually, you might find that pip goes into the Python27/Scripts folder, rather than the Python27/Tools/Scripts folder.  You will probably need to also run:
PATH=%PATH%;C:/Python27/Scripts for it to be recognised.

To install virtualenv, from a command prompt:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Run the following 

| c:/pip install virtualenv

This will install virtualenv into the C:/pythonXY/Scripts and C:/pythonXY/Lib/site-packages folder.

* Then run the following:

| c:/virtualenv ENV

This will create an ENV folder at the top level c:/ENV/ containing Include, Lib and Scripts folder.
Python.exe is installed into the Scripts folder.


If you run python from the default location the paths used will be as follows:

| C:/>python
| Python 2.7.8 (default, Jun 30 2014, 16:03:49) [MSC v.1500 32 bit (Intel)] on win32
| Type "help", "copyright", "credits" or "license" for more information.
| >>> import sys
| >>> sys.path
| ['', 'C:/Windows/system32/python27.zip', 'C:/Python27/DLLs', 'C:/Python27/
| /lib', 'C:/Python27/lib/plat-win', 'C:/Python27/lib/lib-tk', 'C:/Python27
| ', 'C:/Python27/lib/site-packages', 'C:/Python27/lib/site-packages/win32'
| , 'C:/Python27/lib/site-packages/win32/lib', 'C:/Python27/lib/site-packages/Pythonwin']
| 


If you do the same, using the ENV version, the paths used for your modules/site-packages will be altered:

| C:/env/scripts/python
| Python 2.7.8 (default, Jun 30 2014, 16:03:49) [MSC v.1500 32 bit (Intel)] on win32
| Type "help", "copyright", "credits" or "license" for more information.
| >>> import sys
| >>> sys.path
| ['', 'C:/Windows/system32/python27.zip', 'c:/env/DLLs', 'c:/env/lib', 'c:
| /env/lib/plat-win', 'c:/env/lib/lib-tk', 'c:/env/scripts', 'C:/Python27
| /Lib', 'C:/Python27/DLLs', 'C:/Python27/Lib/lib-tk', 'c:/env', 'c:/env/lib/site-packages']
| 

To set the path to always use this virtualenv path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| C:/>env/scripts/activate
| (ENV) C:/
| 

and to undo these changes tun:

| (ENV) C:/env/scripts/deactivate
| C:/
| 

Using the default site-packages, those installed into the main Python location:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use this option when creating the virtualenv folder:

| C:/virtualenv --system-site-packages ENV
| 

For other information on settings paths, or config options, see the link at the top of this section.


Installing site-packages
------------------------

Info on installing Python modules and Python Distribution Utilities, can be found here: https://docs.python.org/2/install/

* To install a site-package module into default site-packages folder:

#. unzip the module zip into a folder, this should contain a setup.py file.
#. Then type:

| C:/>python setup.py install
| 

This will place the module into the site-package folder, eg C:/Python27/Lib/site-packages


* To install a site-package module into virtualenv site-packages folder:

#. Activate the virtualenv environment:

    | C:/env/scripts/activate
    | (ENV) C:/
    | 

#. Then unzip the module into a folder, this should contain a setup.py file.

#. Next type:

    | (ENV) C:/>python setup.py install
    | 

This will place the module into the site-package folder within the virtualenv environment, eg C:/ENV/Lib/site-packages

Making the re-distributable module, and setup file
==================================================

https://docs.python.org/2/distutils/introduction.html

Distributing modules
--------------------
If you have a module which is to be distributed within the Python, or virtualenv environment, then you must make a zip file containing the module and a setup.py file.

A basic setup.py file will look like this:

| from distutils.core import setup
| setup(name='my_module',
|       version='1.0',
|       py_modules=['my_module'],
|       )
| 

Use pip to install module packages into python.  
------------------------------------------------

Note: If pip isn't then download the windows binary from https://pypi.python.org/pypi

See here for information on Pip installing packages: https://docs.python.org/3.4/installing/index.html

* To install type:

    | (ENV) C:\>python -m pip install SomePackage, eg "python -m pip install Sphinx"
    | 
    
This will install Sphinx into the virualenv, eg C:\ENV\Lib\site-packages\Sphinx

Note: the "SomePackage" is taken from the Python Packaging Index, found here:   https://pypi.python.org/pypi, where it will download the latest version available, with all of its dependencies.
       
       
Install ipython, pandas, numpy using pip 
========================================

These modules are installed using https://pypi.python.org/pypi/
http://ipython.org/ - IPython is a command shell for interactive computing in multiple programming languages, originally developed for the Python programming language, that offers enhanced introspection, rich media, additional shell syntax, tab completion, and rich history. IPython currently provides the following features:

http://pandas.pydata.org/ - Pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.

http://www.numpy.org/ - NumPy is the fundamental package for scientific computing with Python. 

To Install
----------

| python -m pip install IPython or pip install IPython.
| pip install numpy
| pip install pandas

Note: some of these depend on MS Visual Studio v9.0 components and will not run without them.  
The C++ compiler that's needed can be installed from here: 
http://www.microsoft.com/en-gb/download/details.aspx?id=44266


IPython notebook
================

To install IPython notebook, you must first install the following dependencies:

| pip install jinja2
| pip install pyzmq
| pip install tornado
| 

The following will now start a browser session:

| C:\>IPython notebook  
| 

or alternatively, start it with the following to use network notebooks:

| C:\>IPython notebook --notebook-dir=u'\\FDNas01\\Media\\TestData\Notebooks'
|     Default: u'C:\\ENV\\Scripts'
|     The directory to use for notebooks and kernels.
| 

http://ipython.org/notebook.html - The IPython Notebook is a web-based interactive computational environment where you can combine code execution, text, mathematics, plots and rich media into a single document.

IronPython
==========

To Install
----------

IronPython can be installed from here:
http://ironpython.net/download/

IronPython is an open-source implementation of the Python programming language which is tightly integrated with the .NET Framework. 
IronPython can use the .NET Framework and Python libraries, and other .NET languages can use Python code just as easily.



Getting started guides
======================

numPy - http://wiki.scipy.org/Tentative_NumPy_Tutorial - see http://localhost:8888/notebooks/numPY%20tutorial.ipynb#
and http://wiki.scipy.org/Numpy_Example_List

SciPy - http://docs.scipy.org/doc/scipy/reference/tutorial/index.html
Pandas - http://pandas.pydata.org/pandas-docs/version/0.15.1/10min.html#min 


Using Python Decorators - http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
and http://www.artima.com/weblogs/viewpost.jsp?thread=240808
and http://www.brianholdefehr.com/decorators-and-functional-python
