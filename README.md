![ECCW title image](/home/bmary/Programmation/eccw/eccw/images/eccw_title.png  "ECCW")

    
# Exact Critical Coulomb Wedge

**ECCW** allows to compute the exact solution of any parameter of critical Coulomb wedge (as Dahlen 1984 and Yuan et al. 2015). It allows to draw any of these solutions in the β vs α domain (basal slope against surface slope). Are availables compressive or extensive geological context and fluid pore pressure.
  
**ECCW** is under GNU GPL-v3  licence.

------------------------------------

# Installation


## Dependancies

The folowing dependancies are needed for manual installation from sources.
All are availables on *ubuntu* and *debian* repositories.

	numpy
	matplotlib
	python3-pyqt5
	python3-xmltodict
	canberra-gtk-module (?)

## Steps for installation

### Installation from pypi

Simply type in a shell

	$ pip install eccw

or 

	$ pip3 install eccw

according to your system defaults.
Eccw is written in python3, so the pypi version should be so.

### Installations from sources

Unzip eccw.zip somewhere in your home.

Add the location of *eccw* folder to the environment variable `$PYTHONPATH`

    $ export PYTHONPATH=${PYTHONPATH}:${HOME}/path/to/eccw/

Adding this line (correctly setted to suit your system) in your `.bashrc` file will permanently set  available the access to eccw module to your local python.

Before to try to launch *eccw*, make sure that the file `eccw/eccw/bin/eccw` is executable

    $ chmod +x ${HOME}/path/to/eccw/eccw/bin/eccw

with `${HOME}/path/to/` replaced by your path to the *eccw* folder on your system.



------------------------------------

# Usage

## GUI usage

### From pypi install

Simply type `eccw` in a shell to launch *eccw*.

### From sources install

To launch eccw, run `./eccw` in a shell which current working directory is setted to `${HOME}/path/to/eccw/eccw/bin` (with `${HOME}/path/to/` replaced by your path to the *eccw* folder on your system)


## Python library usage

You can import and use the core objects for computing and plotting Critical Coulomb Wedge from python as discribe in what follows.

### EccwCompute

```python
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
(3.4365319302835018, 23.946319406533199)
```

The result is always a tuple of two elements.
First result is for inverse fault mechanism context, second result is for normal fault mechanism context.

The `beta` parameter gets a specificity : 0, 1 or 2 results could be obtained in both the normal of inverse context.
This is the reason `beta` results are tuples of tuples.

```python
>>> foo.alpha = 3.436532
>>> foo.compute("beta") 
((-1.0516746372768912e-07,), (69.6779628783264,))
>>> foo.alpha = 20
>>> foo.compute("beta") 
((), (-3.580929608343892, 43.25889259183777))
>>> foo.alpha = -20
>>> foo.compute("beta") 
((36.74110740816224, 83.58092960834391), ())
```

Have a look on the plot obtained in next section to understand the previous results.

### EccwPlot

```python
>>> from eccw import EccwPlot
>>> foo = EccwEccwPlot(phiB=30, phiD=10)
>>> foo.add_curve()
>>> foo.add_point(alpha=3.436532)
>>> foo.add_point(alpha=20, style='*', size=10)
>>> foo.add_point(alpha=-20, style='s')
>>> foo.show()
```

----------------------------------

# Contributing

## Dependancies

	pyqt5-dev-tools (pyuic5, pyrcc5)

## Informations for developpers

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
