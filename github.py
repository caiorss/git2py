#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import request
from requests.auth import HTTPBasicAuth
import json


def mapl(func, lst):
    return list(map(func, lst))

def pluck(key, ListOfDict):
    return list(map(lambda obj: obj[key], ListOfDict))

def select(keys, ListOfDict):
    return mapl( lambda obj: mapl(lambda key: obj[key], keys), ListOfDict)

    #return list(map(lambda key: data[0].get(key), ["name", "url", "description", "fork"]))


def list2dict(keys, List):
    """
    Returns a list of dictionaries given a list of list

    f [k] [[x]] --> [{k:x1}, {k:x2} ... {k:xn}]

    :param keys:
    :param List:
    :return:
    """
    return mapl(lambda obj: dict(zip(keys, obj)), List)


def __print_show_repository(data):

    print("\n\n")
    print ("Name:\t\t", data["name"])
    print ("Description:\t\t\n", data["description"], "\n")
    print ("Language:\t\t", data["language"])
    print ("Url:\t\t", data["html_url"])
    print ("SSH Url:\t\t", data["ssh_url"])
    print ("Created:\t\t", data["created_at"])
    print ("Updated:\t\t", data["updated_at"])
    print ("Fork:\t\t", data["fork"])
    #print ("Language:\t", repo_data[])


def show_repository(username, auth=None):

    apiturl = "https://api.github.com/users/{}/repos".format(username)
    r = request("GET", apiturl, auth=auth)
    reamaining_requests = int(r.headers['X-RateLimit-Remaining'])

    print("Remaining Requests :", reamaining_requests)

    #print("Remain")

    data = r.json()

    keys = ["name", "description", "url", "ssh_url", "html_url", "created_at", "updated_at", "language", "fork"]
    selected = list2dict(keys, select(keys, data))
    mapl(__print_show_repository, selected)



def create_repository(user, passw, repository_data):
    """
    Example:
    {
      "name": "Hello-World",
      "description": "This is your first repository",
      "homepage": "https://github.com",
      "private": false,
      "has_issues": true,
      "has_wiki": true,
      "has_downloads": true
    }

    :param username:
    :param auth:                Tuple username, password
    :param repository_data:
    :return:
    """
    apiturl = "https://api.github.com/user/repos"
    r = request("POST", apiturl, auth=HTTPBasicAuth(user, passw), data= repository_data)

    reamaining_requests = int(r.headers['X-RateLimit-Remaining'])
    print("Remaining Requests :", reamaining_requests)

    #response=  r.json()
    #return response["ssh_url"], response["html_url"]

    return r.text





