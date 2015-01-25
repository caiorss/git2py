#!/bin/bash

#export MODULE_PATH=$(pwd)/git2py
export MODULE_PATH=$(pwd)

export PYTHONPATH=$PYTHONPATH:MODULE_PATH
echo $MODULE_PATH

python -m git2py

