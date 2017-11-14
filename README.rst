|ECCW|
######
    
Exact Critical Coulomb Wedge
============================

**ECCW** allows to compute the exact solution of any parameter of critical Coulomb wedge (as Dahlen 1984 and Yuan et al. 2015). It allows to draw any of these solutions in the β vs α domain (basal slope against surface slope). Are availables compressive or extensive geological context and fluid pore pressure.
  
=========  =======  =============
  Date     Version     Authors
=========  =======  =============
2017-11-8     1     BCL Mary
=========  =======  =============

-------------------------------------

Installation
============

Dependeancies
+++++++++++++

    | python3-pyqt4
    | canberra-gtk-module
    | python3-xmltodict
    | numpy
    | pyqt4-dev-tools (pyuic4)

Steps for installation
++++++++++++++++++++++


Usage
=====

.. TODO Need a brief tuto here

Contributing
============

Informations for developpers
++++++++++++++++++++++++++++
Convert xml .ui files created using *Qt-Designer* into python files::
    
    $ pyuic4 -x xxx.ui -o xxx_Viewer.py

**Warning**: in files using KColorButton, conversion from xml to python3 is buggy. One need too add 
``from PyKDE4.kdeui import KColorButton`` 
and remove
``from kcolorbutton import KColorButton``

All graphical object (Qt-derived) get the following methods:

* getParams:   return an OrderedDict that describe the state of the object.
* setParams:   set the object with a dict obtained from getParams.
* getSelect:   return an OrderedDict that describe the selected parameters to treat (equal to getParams if the paramters gets single state).


.. |ECCW| image:: ./eccw/images/eccw_title.png
    :alt: ECCW
    :height: 200
