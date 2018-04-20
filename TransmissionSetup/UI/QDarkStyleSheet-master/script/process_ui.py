# -*- coding: utf-8 -*-
"""Script to process UI files (convert .ui to .py).

It compiles .ui files to be used with PyQt4, PyQt5, PySide, QtPy, PyQtGraph.
You just need to run (it has default values) from script folder.

To run this script you need to have these tools available on system:

    - pyuic4 for PyQt4 and PyQtGraph
    - pyuic5 for PyQt5 and QtPy
    - pyside-uic for Pyside

Links to understand those tools:

    - pyuic4: http://pyqt.sourceforge.net/Docs/PyQt4/designer.html#pyuic4
    - pyuic5: http://pyqt.sourceforge.net/Docs/PyQt5/designer.html#pyuic5
    - pyside-uic: https://www.mankier.com/1/pyside-uic

"""

from __future__ import absolute_import, print_function

import argparse
import glob
import os
import sys
from subprocess import call


def main(arguments):
    """Process UI files."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--ui_dir',
                        default='../example/ui',
                        type=str,
                        help="UI files directory, relative to current directory.",)
    parser.add_argument('--create',
                        default='all',
                        choices=['pyqt', 'pyqt5', 'pyside', 'qtpy', 'pyqtgraph', 'all'],
                        type=str,
                        help="Choose which one would be generated.")

    args = parser.parse_args(arguments)

    print('Changing directory to: ', args.ui_dir)
    os.chdir(args.ui_dir)

    print('Converting .ui to .py ...')

    for ui_file in glob.glob('*.ui'):
        # get name without extension
        filename = os.path.splitext(ui_file)[0]
        print(filename, '...')
        ext = '.py'

        # creating names
        py_file_pyqt5 = filename + '_pyqt5_ui' + ext
        py_file_pyqt = filename + '_pyqt_ui' + ext
        py_file_pyside = filename + '_pyside_ui' + ext
        py_file_qtpy = filename + '_qtpy_ui' + ext
        py_file_pyqtgraph = filename + '_pyqtgraph_ui' + ext

        # calling external commands
        if args.create in ['pyqt', 'pyqtgraph', 'all']:
            call(['pyuic4', '--from-imports', ui_file, '-o', py_file_pyqt])

        if args.create in ['pyqt5', 'qtpy', 'all']:
            call(['pyuic5', '--from-imports', ui_file, '-o', py_file_pyqt5])

        if args.create in ['pyside', 'all']:
            call(['pyside-uic', '--from-imports', ui_file, '-o', py_file_pyside])

        if args.create in ['qtpy', 'all']:
            print("Compiling for PySide ...")
            # special case - qtpy - syntax is PyQt5
            with open(py_file_pyqt5, 'r') as file:
                filedata = file.read()
            # replace the target string
            filedata = filedata.replace('from PyQt5', 'from qtpy')
            with open(py_file_qtpy, 'w+') as file:
                # write the file out again
                file.write(filedata)

        if args.create in ['pyqtgraph', 'all']:
            # special case - pyqtgraph - syntax is PyQt4
            with open(py_file_pyqt, 'r') as file:
                filedata = file.read()
            # replace the target string
            filedata = filedata.replace('from PyQt4', 'from pyqtgraph.Qt')
            with open(py_file_pyqtgraph, 'w+') as file:
                # write the file out again
                file.write(filedata)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
