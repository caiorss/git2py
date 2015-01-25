#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import ipshellapi
from tabulate import tabulate
import sys
from shutil import copy

sys.path.extend("/home/tux/PycharmProjects/git2py/git2py")

from git2py.git import GIT

import os
import json
from collections import OrderedDict

def expand_path(path): return os.path.join(*list(map(os.path.expanduser, path.split(os.path.sep))))

USERFILE = expand_path("~/.git2py.json")


if not os.path.exists(USERFILE):
    model = os.path.join(os.path.dirname(os.path.abspath(__file__)), "git2py.json")
    copy(model, USERFILE)
    print("Created: ", USERFILE)
    print("Edit this file and add your settings")
    sys.exit(0)



with open(USERFILE) as fp:
    data = json.load(fp, object_pairs_hook=OrderedDict)

projects = data["projects"]



def get(key, dict_list):
    return list(map(lambda obj: obj[key], dict_list))

def select(key, value, dict_list):
    try:
        return list(filter(lambda obj: obj[key] == value, dict_list))[0]
    except:
        return False

def list_projects():
    return get("name", projects)

def get_project(name):
    try:
        proj =  select("name", name, projects)
        return GIT(path= expand_path(proj["path"]), name=proj["name"], desc=proj["desc"], tags=proj["tags"])
    except:
        return False

def show_projects():
    print(json.dumps(projects, indent=2))


def usage():
    print("IPython GIT MODULE")

    print("""
    Enter:

    > usage()               - Show this help text

    > who                   - To see the user variables
    > show_projects()       - To show all the User projects
    > list_projects()       - List all project names
    > get_project(project)  - Returns a GIT object of the project
    > settings              - This Variable contains the User Settings Location

    Git class:                                  GIT
    Create a New GIT object:                    g = GIT("/repository")
    Create a GIT object in current directory:   g = GIT()

    Example:
        >>> p = get_project("myproject")

    """.strip("\n"))


def command_line_usage():
    print("git2py  [--help/-h | --show/-s | --list/-l | --proj/-p] [project]")
    print("")
    print("Options:")
    print("     --help -h           : Print help text")
    print("     --list -l           : List all projects names")
    print("     --show -s           : Show all projects details")
    print("     --proj -p <project> : Starts loading a project")


IP = ipshellapi.Ipshell()

IP.ipsh.user_ns["GIT"] = GIT
IP.ipsh.user_ns["projects"] = projects
IP.ipsh.user_ns["get"] = get
IP.ipsh.user_ns["select"] = select
IP.ipsh.user_ns["list_projects"] = list_projects
IP.ipsh.user_ns["get_project"] = get_project
IP.ipsh.user_ns["show_projects"] = show_projects
IP.ipsh.user_ns["settings"] = USERFILE
IP.ipsh.user_ns["usage"] = usage


argvs = sys.argv
nargv = len(sys.argv)

#print(argvs)

if __name__ == "__main__":

    if nargv >= 2:

        if argvs[1] == "--help" or argvs[1] == "-h" :
            command_line_usage()
            sys.exit(0)

        elif argvs[1] == "--show" or argvs[1] == '-s':
            print(show_projects())
            sys.exit(0)

        elif argvs[1] == "--list" or argvs[1] == '-l':
            print(list_projects())
            sys.exit(0)


        elif argvs[1] == "-proj" or argvs[1] == '-p':

            proj = get_project(argvs[2])
            proj.cd()
            IP.ipsh.user_ns["proj"] = proj
            IP.run()

            if proj:
                print("Loaded Project : %s" % argvs[2])
                print(proj)
            else:
                print("Project not found")
                sys.exit(1)

        elif argvs[1] == "-int" or argvs[1] == "-i":
                usage()
                IP.run()

    else:
        command_line_usage()
        sys.exit(0)


    #repo = GIT(".")


    sys.exit(0)