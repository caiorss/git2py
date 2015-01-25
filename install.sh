#!/usr/bin/env bash

# Get the directory where this script is
THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

ln -s $THISDIR/git2py  ~/lib/git2py

# Install Launcher
cp git2py.sh ~/bin/git2py
chmod +x ~/bin/git2py