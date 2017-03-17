#!/usr/bin/env python3.4

import sys
from distutils.core import setup

import py2exe

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 2}},
    windows=[{
        "script": 'LF2CRLF.py',
        "icon_resources": [(0, "Notepad.ico")]
    }],
    zipfile = None
)
