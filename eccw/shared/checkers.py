#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
A collection of tools dedicated to check variables  and return a default value if value doesn't match targeted type.
"""

def float_check(value, default=None):
    """value must be a float or default."""
    try:
        return float(value)
    except ValueError:
        return default
        
def str_check(value, default=''):
    """value must be a string or default."""
    if value is None:
        return default
    else:
        return str(value)

#TODO : this function is deprecated : it is now found in WrapperDict class (where it is used).
def params_check(obj, parser, params):
    """Check integrity of eccw.gui.shared.wrappers structure."""
    name = obj.__class__.__name__
    if isinstance(params, dict):
        try:
            for key, value in params.items():
                if isinstance(value, dict):
                    parser[key](**value)
                else:
                    parser[key](value)
        except KeyError:
            raise TypeError(name+"() gets unknown keyword argument '" + str(key) + "'.")
    else:
        raise TypeError(name+"() awaits a dict as argument.")

