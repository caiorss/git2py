#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import ipshellapi
from tabulate import tabulate
import sys

sys.path.extend("/home/tux/PycharmProjects/git2py/git2py")

from git2py.git import GIT


IP = ipshellapi.Ipshell()



IP.ipsh.user_ns["GIT"] = GIT

if __name__ ==  "__main__":

    print("IPython GIT MODULE")
    #print(tabulate(Repo.list()))

    print("""
Usage:
    %go     <project_nam>  # Go to a project
    %projs                 # List projects

    """.strip("\n"))


    repo = GIT(".")

    IP.run()