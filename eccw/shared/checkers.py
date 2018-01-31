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

