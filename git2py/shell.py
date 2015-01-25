#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ipshellapi
from tabulate import tabulate
import sys

sys.path.extend("/home/tux/PycharmProjects/git2py/git2py")

from git import Repo, GIT


IP = ipshellapi.Ipshell()


@IP.magic("projs")
def _projects(self, arg):
    print(tabulate(Repo.list()))

@IP.magic("go")
def _go(self, project):
    print(project)
    repo = Repo.go(str(project))
    IP.user_ns["repo"] = repo


IP.ipsh.user_ns["Repo"] = Repo
IP.ipsh.user_ns["GIT"] = GIT

if __name__ ==  "__main__":

    print("IPython GIT MODULE")
    print(tabulate(Repo.list()))

    print("""
Usage:
    %go     <project_nam>  # Go to a project
    %projs                 # List projects

    """.strip("\n"))


    repo = GIT(".")

    IP.run()