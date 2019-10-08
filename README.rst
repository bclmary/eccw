ECCW
####

Exact Critical Coulomb Wedge
============================

**ECCW** allows to compute the exact solution of any parameter of critical Coulomb wedge (as Dahlen 1984 and Yuan et al. 2015). It allows to draw any of these solutions in the β vs α domain (basal slope against surface slope). Are availables compressive or extensive geological context and fluid pore pressure.

**ECCW** is under GNU GPL-v3 license.


*******************************************************************

General informations
====================

*ECCW* is a *python3* library.

A graphical user interface (GUI), written in *python3* and using *Qt* is also available under the name *ECCW-GUI*.


*******************************************************************


Installation
============


Windows
+++++++

.. note :: Only tested on *Windows 7*.


1. Install python3 verson of **miniconda** python environment from https://conda.io/miniconda.html
    a. run downloaded .exe;
    b. at **Advanced Options** step, tick checkbox named *Add Anaconda to my PATH environment variable*.

2. Launch the windows **Command Prompt**:
    a. type ``conda`` to check that *conda* is correctly installed;
    b. type ``pip`` to check that *pip* is also correctly installed.

3. Install *ECCW* with the following command in the *Command Prompt*::

    $ pip install eccw

4. *ECCW* is then available from the *Command Prompt* by taping ``eccw`` or simply from the main *Windows* menu under the name *eccw*.


Linux
+++++

.. note :: Only tested on *Debian 9 (Gnome)* and *Ubuntu 16.04 (Unity)*.

Installation using pip
----------------------

1. Install **pip** and **tk** for *Python3*. 
   On *Debian* family distributions, you can install these packages using the following command::

      $ sudo apt-get install python3-pip python3-tk

2. Install *ECCW* with the following command::

      $ pip3 install eccw

3. *ECCW* is then available from a terminal by taping ``eccw``

Installation from sources_
--------------------------

1. Install the folowing dependancies for python3:

	| tk
	| pyqt5
	| numpy
	| matplotlib
	| xmltodict

   On *Debian* family distributions, you can install these packages using the following command::

      $ sudo apt-get install python3-tk python3-pyqt5 python3-numpy python3-matplotlib python3-xmltodict

2. Using a terminal with current working directory setted on *ECCW* sources folder, you can install *ECCW* with the following command::

      $ python3 setup.py install

3. *ECCW* is then available from a Terminal by taping ``eccw``


.. note:: You can also launch *ECCW* without installation (but with dependancies installed) if you add the path to the *ECCW* sources folder to the environment variable ``$PYTHONPATH``::

    $ export PYTHONPATH=${PYTHONPATH}:path/to/eccw/sources/

    This command can be added to your ``.bashrc`` file (hidden file located at the root of your home).
    Once the PYTHONPATH is seted, you can launch *ECCW* by running ``eccw/main.py`` file in the sources folder.



*******************************************************************

Usage
=====

The following describe usage of *ECCW* class objects, callable from a python3 shell.

EccwCompute
+++++++++++

This the core object that compute the solutions of the *CCW* problem.
::

    >>> from eccw import EccwCompute
    >>> foo = EccwCompute(phiB=30, phiD=10, beta=0)
    >>> foo.show_params()
    { context       : 'Compression'
      beta          : 0.0
      alpha         : nan
      phiB          : 30.0
      phiD          : 10.0
      rho_f         : 0.0
      rho_sr        : 0.0
      delta_lambdaB : 0.0
      delta_lambdaD : 0.0
    }
    >>> foo.compute("alpha")
    ((3.4365319302835018,), (23.946319406533199,))
    

The result obtained with the ``compute`` method is always a tuple of two tuples.
The first tuple contains results in **inverse** fault mechanism, while the second tuple contains results in **normal** fault mechanism.
These tuples can each contain 0, 1 or 2 values, with a total always equal to 0 or 2.
Here some more examples with computation of beta ``parameter``::
::

    >>> foo.alpha = 3.436532
    >>> foo.compute("beta") 
    ((-1.0516746372768912e-07,), (69.6779628783264,))
    >>> foo.alpha = 20
    >>> foo.compute("beta") 
    ((), (-3.580929608343892, 43.25889259183777))
    >>> foo.alpha = -20
    >>> foo.compute("beta") 
    ((36.74110740816224, 83.58092960834391), ())
    >>> foo.alpha = -35
    >>> foo.compute("beta") 
    ((), ())

Have a look on the plot obtained in next section to understand these results.

EccwPlot
++++++++

This the core object that plot the solutions of the *CCW* problem. This object inherits from ``EccwCompute``.
::

    >>> from eccw import EccwPlot
    >>> foo = EccwPlot(phiB=30, phiD=10)
    >>> foo.add_curve(inverse={'color':(1,0,0,1), 'label':'inverse'}, 
                      normal={'color':(0,0,1,1), 'label':'normal'})
    >>> foo.add_point(alpha=3.436532)
    >>> foo.add_point(alpha=20, style='*', size=10)
    >>> foo.add_point(alpha=-20, style='s')
    >>> foo.add_legend()
    >>> foo.show()

|Screen copy of EccwPlot's plot|





.. _sources: https://github.com/bclmary/eccw.git

.. |Screen copy of EccwPlot's plot| image:: ./images/EccwPlot_example.png
    :alt: screen copy of matplotlib window containing ECCW plot
    :width: 400


