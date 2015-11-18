#!/usr/bin/env python

import requests
from os import environ
from time import sleep
from urlparse import urlunparse
from subprocess import call


class Grafana(object):
    env = environ.get
    scheme = "http"
    api_path = "api/datasources"

    def __init__(self):
        self.params = {
            "name": self.env("DS_NAME", "Test datasource"),
            "type": self.env("DS_TYPE", "graphite"),
            "access": self.env("DS_ACCESS", "proxy"),
            "url": self.env("DS_URL", ""),
            "password": self.env("DS_PASS", ""),
            "user": self.env("DS_USER", ""),
            "database": self.env("DS_DB", ""),
            "basicAuth": self.env("DS_AUTH", 'false'),
            "basicAuthUser": self.env("DS_AUTH_USER", ""),
            "basicAuthPassword": self.env("AUTH_PASS", ""),
            "isDefault": self.env("DS_IS_DEFAULT", 'false'),
            "jsonData": self.env("DS_JSON_DATA", 'null')
        }
        self.gf_url = urlunparse(
            (
                self.scheme,
                ":".join((self.env("GF_HOST", "localhost"), self.env("GF_PORT", "3000"))),
                self.api_path, "", "", ""
            )
        )
        self.auth = self.env("GF_USER", "admin"), self.env("GF_PASS", "admin")
        self.sess = requests.Session()

    def init_datasource(self):
        response = False
        res = self.sess.post(self.gf_url, data=self.params, auth=self.auth)
        if res.status_code == requests.codes.ok:
            response = True

        return response

    def start(self):
        status = False
        # run grafana
        call([
            "/usr/sbin/grafana-server",
            "--homepath=/usr/share/grafana",
            "--config=/etc/grafana/grafana.ini",
            "cfg:default.paths.data=/var/lib/grafana",
            "cfg:default.paths.logs=/var/log/grafana"]
        )
        # wait, until gf api will be available
        # trying 5 times
        repeat = 0
        while repeat <= 5:
            if self._check_gf():
                status = True
                break
            repeat += 1
            sleep(3)

        return status

    def _check_gf(self):
        res = self.sess.get(self.gf_url, auth=self.auth)

        return True if res.status_code == requests.codes.ok else False

if __name__ == "__main__":
    gf = Grafana()
    try:
        if gf.start():
            if gf.init_datasource():
                print "*------------SUCCESS! Your datasource was added!------------*"
    except Exception as error:
        print "*------------ERROR! %s------------*" % error


