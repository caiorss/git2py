#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

$ git show-branch
* [dev] dtime library updated
 ! [master] saturated_steam.txt
--
*  [dev] dtime library updated
*  [dev^] added date parser
*  [dev~2] files added
*  [dev~3] added files
*  [dev~4] shell improved project hirarchy improved
*  [dev~5] added prefnum
*+ [master] saturated_steam.txt

"""
from __future__ import print_function

import os
from pathlib import Path

import sys
from subprocess import Popen, PIPE
import re
from pprint import pprint
import utils
from tabulate import tabulate


def zipdir(path, filename):
    import zipfile
    zip = zipfile.ZipFile(filename, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

    zip.close()


def execute(cmd):

    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out+err


def is_git(path):
    return os.path.isdir(os.path.join(path, ".git"))


class GIT:

    git = "/usr/bin/git"

    def __init__(self, directory="."):
        self.directory = os.path.abspath(directory)

    @property
    def name(self):
        return os.path.basename(self.directory)

    def gitrun(self, command):
        pwd = os.getcwd()
        os.chdir(self.directory)
        out = self.run("{} {} ".format(GIT.git, command))
        os.chdir(pwd)
        return out

    def is_git(self):
        return is_git(self.directory)

    def config_global(self, username, email):
        execute('git config --global user.name {}'.format(username))
        execute('git config --global user.email "{}"'.format(email))

    def config_local(self, username, email):
        self.run('git config --local user.name {}'.format(username))
        self.run('git config --local user.email "{}"'.format(email))

    def get_user_global(self):
        user= execute("git config --get user.name").strip()
        email= execute("git config --get user.email").strip()
        return "{} <{}>".format(user, email)

    def get_user_local(self):
        user = self.run("git config --get --local user.name").strip()
        email = self.run("git config --get --local user.email").strip()
        return "{} <{}>".format(user, email)

    def show_config(self):
        """
        Show all global config
        :return:
        """
        print(execute("git config --list"))

    def run(self, command):
        pwd = os.getcwd()
        os.chdir(self.directory)
        out = execute(command)
        os.chdir(pwd)
        return out

    def authors(self):
        out = self.run("git log")
        authors =  re.findall(r"Author:\s*(\S+)\s<(.*)>", out)

        authors = map(lambda x: "{} <{}>".format(x[0], x[1]), authors)
        authors = sorted(set(authors))
        #print(authors)
        return authors

    def branches(self, type=""):
        """
        :param type: '-r' : Show remote branches only, '-a', all branches
        :return:
        """
        out = self.run("git branch {}".format(type))
        return list(map(lambda x: x.strip(), out.splitlines()))

    def remote_branches(self):
        return self.run("git remote").split()

    def add_remote(self, name, url):
        """
        Add Remote Branch

        :param name: Name of remote branch
        :param url:  URL of remote branch
        :return:

        Example:
        git remote add beanstalk git@accountname.beanstalkapp.com:/gitreponame.git

        add_remote("beanstalk", "git@accountname.beanstalkapp.com:/gitreponame.git")

        """
        #git remote add beanstalk git@accountname.beanstalkapp.com:/gitreponame.git
        self.gitrun("remote add {} {}".format(name, url))


    def all_branches(self):
        return self.branches('-a')

    def current_branch(self):
        return self.gitrun("rev-parse --abbrev-ref HEAD").strip()

    def remote_url(self):
        """
        List all remote URLS
        :return: Remote branch URLS
        """
        return self.run("git remote -v")

    def status(self):
        out= self.gitrun("status")
        modified = re.findall("modified:\s+(.*)", out)

        pprint(modified)

        o1 = re.findall("Untracked files:(.*)", out, re.DOTALL)
        if o1:

            print(o1[0])

            untracked = re.findall("^\s+(.*)", o1[0], re.M)
            untracked = untracked[1:-1]
        else:
            untracked = []

        return modified, untracked


    def push(self, local="master", remote="origin"):
        out = self.gitrun("push {} {}".format(remote, local))
        return out

    def untracked_files(self):
        out= self.gitrun("status")
        o1 = re.findall("Untracked files:(.*)", out, re.DOTALL)
        if o1:
            untracked = re.findall("^\s+(.*)", o1[0], re.M)
            untracked = untracked[1:-1]
        else:
            untracked = []

        return untracked


    def modified_files(self):
        out= self.gitrun("status")
        modified = re.findall("modified:\s+(.*)", out)
        return modified

        #print(out)

    def list_files(self, branch=""):

        if not branch:
            out = self.gitrun("ls-files")
        else:
            out = self.gitrun("ls-tree -r {} --name-only".format(branch))
        return out.splitlines()

    def replace_author(self, oldname, newname, newemail):
        """
        Reference: http://www.michaelwnelson.com/2013/12/08/rewriting-history-in-git/

        git push origin master --force
        """

        cmd = """
        git filter-branch --commit-filter 'if [ "$GIT_AUTHOR_NAME" = "{OLDNAME}" ];
        then export GIT_AUTHOR_NAME="{NEWNAME}";
        export GIT_AUTHOR_EMAIL={NEWEMAIL;
        fi; git commit-tree "$@"' -f"""

        cmd = cmd.format(OLDNAME=oldname, NEWNAME=newname, NEWEMAIL=newemail)
        self.run(cmd)

    def replace_committer(self, oldname, newname, newemail):
        """
        Reference: http://www.michaelwnelson.com/2013/12/08/rewriting-history-in-git/

        git push origin master --force
        """

        cmd = """
        git filter-branch --commit-filter 'if [ "$GIT_AUTHOR_NAME" = "{OLDNAME}" ];
        then export GIT_COMMITER_NAME="{NEWNAME}";
        export GIT_COMMITER_EMAIL={NEWEMAIL;
        fi; git commit-tree "$@"' -f"""

        cmd = cmd.format(OLDNAME=oldname, NEWNAME=newname, NEWEMAIL=newemail)
        self.run(cmd)


    def fix_name_email(self, old_email, correct_name, correct_email):
        """
        :param oldname: 
        :return:

        https://help.github.com/articles/changing-author-info/
        git push --force --tags origin 'refs/heads/*'
        """
        
        script = """
        git  filter-branch --env-filter '
        OLD_EMAIL="{OLD_EMAIL}"
        CORRECT_NAME="{CORRECT_NAME}"
        CORRECT_EMAIL="{CORRECT_EMAIL}"

        if [ "$GIT_COMMITTER_EMAIL" = "{OLD_EMAIL}" ]
        then
        export GIT_COMMITTER_NAME="{CORRECT_NAME}"
        export GIT_COMMITTER_EMAIL="{CORRECT_EMAIL}"
        fi
        if [ "$GIT_AUTHOR_EMAIL" = "{OLD_EMAIL}" ]
        then
        export GIT_AUTHOR_NAME="{CORRECT_NAME}"
        export GIT_AUTHOR_EMAIL="{CORRECT_EMAIL}"
        fi
        ' -f --tag-name-filter cat -- --branches
        """

        script = script.format(OLD_EMAIL=old_email, CORRECT_NAME=correct_name, CORRECT_EMAIL=correct_email)

        print(script)

        out = self.run(script)

        print(out)

    def log_all(self):
        print(self.run("git log --all"))

    def log_diff(self):
        print(self.run("git log -p "))

    def log_oneline(self):
        print(self.run("git log --oneline"))

    def log_relative(self):
        os.system("git log --relative-date")

    def log_author(self, author):
        print(self.run("git log --author {}".format(author)))

    def log_commiter(self, author):
        print(self.run("git log --commiter {}".format(author)))


    def log_graph(self):
        print(self.run(" git log --graph"))

    def ls(self):
        print(self.run('git log --pretty=format:"%C(yellow)%h%Cred%d %Creset%s%Cblue [%cn]" --decorate'))

    def ll(self):
        print(self.run("""git log --pretty=format:"%C(yellow)%h%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --numstat"""))

    def lds(self):
        print(self.run("""git log --pretty=format:"%C(yellow)%h\\ %ad%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --date=short"""))

    def archive(self, branch="master"):
        name = os.path.basename(self.directory)
        self.run(" git archive --format=zip {branch}^ > {name}_{branch}.zip".format(name=name, branch=branch))

    def change_branch(self, name):
        self.run("git checkout -b {}".format(name))

    def init(self, files):
        self.run("git init")
        self.run("git add {}".format(" ".join(files)))
        self.run("git commit -a -m 'started'")


    def commit_all(self, meassage):
        self.run("git commit -a -m '{}'".format(meassage))

    def get_summary(self):
        return self.run("git show --summary")

    def summary(self):
        print(self.get_summary())

    def last_commit(self):
        hash = self.run("git show-ref -h HEAD").strip()
        time = self.run('git log -1 --format="%cd"').strip()
        message = self.run("git log -1 --pretty=%B").strip()

        return (message, time, hash)

    def reset_hard(self):
        print(self.run("git reset --hard"))

    def backup(self):
        """
        Backup the project directory
        :return:
        """
        from datetime import datetime
        name = os.path.basename(self.directory)
        date = datetime.today().strftime("%Y-%m-%d")
        filename = "{}-backup-{}.zip".format(name, date)
        zipdir(".", filename)
        pwd = os.getcwd()
        os.chdir(self.directory)
        os.chdir(pwd)


    def ammend(self):
        """
        Which will take all uncommitted and un-staged changes currently
        in the working directory         and add them to the previous
        commit, amending it before pushing the change up. I use this
        all the time.

        http://blogs.atlassian.com/2014/10/advanced-git-aliases/
        :return:
        """
        self.gitrun("commit -a --amend -C HEAD")


    def __repr__(self):
        text = """
        Directory        : {directory}
        Current Branch   : {current}



        Branches:        : {branches}
        Remote Branches  : {remotes}

        Global User      : {globaluser}
        Local  User-Email: {localuser}

        Last Commit:
        {lastcommit}
        """.strip('\n')

        text= text.format(
            directory=self.directory,
            current=self.current_branch(),
            branches=self.branches(),
            globaluser = self.get_user_global(),
            localuser = self.get_user_local(),
            remotes = self.remote_branches(),
            lastcommit = "\n\t".join(self.last_commit())
        )

        return text




    #import IPython
    #IPython.embed()