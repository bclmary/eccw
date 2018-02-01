#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manage command line interface.
"""

import argparse


from eccw import __version__, __authors__
from eccw.shared.file_management import open_pdf


def options_parser() :
    """Parse options given with the execute command line."""

    #create a parser object
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        description=
            "    ECCW - Exact Critical Coulomb Wedge, Version {0}\n"
            "\n"
            "ECCW Copyright (c) 2016-2018 {1}\n"
            "This program comes with ABSOLUTELY NO WARRANTY.\n"
            "This is free software, and you are welcome to redistribute it"
            "under certain conditions.\n"
            "\n"
            "ECCW is a Qt interface using python package 'eccw' to"
            " compute and draw the exact solution of critical Coulomb"
            " wedge (as Dahlen 1984 and Yuan et al. 2015)\n".format(
                __version__, 
                ", ".join(__authors__)
                ),
        usage="eccw [-h|--help] [-d|--doc] [-V|--version]",
        )

#    # Positional arguments
#    posarg = parser.add_argument_group(title="-"*30+"\nPOSITIONAL ARGUMENTS", description="") 
#    
#    posarg.add_argument('FILE', # phi_D [delta_lambda_B delta_lambda_D density_ratio] [beta]',
#                        type=(float),                        
#                        nargs="*",
#                        #action=EmptyIsTrue,
#                        help=("parameters can be :\n"
#                              "- phi_B : bulk friction angle of material [deg]\n"
#                              "- phi_D : friction angle on detachment [deg]\n"
#                              "          negative value for tectonic extension\n"
#                              "- delta_lambda_B : bulk fluid overpressure gradient\n"
#                              "- delta_lambda_D : décollement fluid overpressure gradient\n"
#                              "- density_ratio : ratio of fluid density and saturated rock density\n"
#                              "- beta : slope of detachment [deg]\n\n"
#                              "different combinations of these parameters are expected:\n"
#                              "  phi_B phi_D\n"
#                              "  phi_B phi_D beta\n"
#                              "  phi_B phi_D delta_lambda_B delta_lambda_D density_ratio\n"
#                              "  phi_B phi_D delta_lambda_B delta_lambda_D density_ratio beta\n\n"))

    # Optional arguments.
    optarg = parser.add_argument_group(title="-"*30+"\nOPTIONAL ARGUMENT", description="")

    optarg.add_argument(
        '-h', '--help',
        action='help',
        help="show this help message and exit\n\n"
        )

    optarg.add_argument(
        '-V', '--version',
        action='version',
        version=__version__,
        help="show program's version number and exit\n\n"
        )

    optarg.add_argument(
        '-d', '--doc',
        dest="doc",
        action='store_true',
        help="show complete documentation and exit\n\n"
        )

    optarg.add_argument('-f', '--file',
                        dest="file",
                        metavar=("FILE"),
#                        type=argparse.FileType('r'),
                        type=(str),
                        help="re-start session saved in FILE (*.eccw)\n\n")

    inputoptions = parser.parse_args() #parse the command line from the shell using arguments defined in the parser object

    if inputoptions.doc is True :
        open_pdf("/eccw/documentation/ECCW.pdf")
        exit()

    return inputoptions.file



if __name__ == "__main__":

    out = options_parser()
    print("run can start", out)

