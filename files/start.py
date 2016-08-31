#!/usr/bin/env python

import requests
import os
import json
from time import sleep
from urlparse import urlunparse
from subprocess import Popen, PIPE


class Grafana(object):
    scheme = "http"
    api_path = "api/datasources"

    def __init__(self):
        '''
            Init params
        '''
        self.params = {
            "name": os.environ.get("DS_NAME"),
            "type": os.environ.get("DS_TYPE"),
            "access": os.environ.get("DS_ACCESS"),
            "url": os.environ.get("DS_URL"),
            "password": os.environ.get("DS_PASS"),
            "user": os.environ.get("DS_USER"),
            "database": os.environ.get("DS_DB"),
            "basicAuth": os.environ.get("DS_AUTH"),
            "basicAuthUser": os.environ.get("DS_AUTH_USER"),
            "basicAuthPassword": os.environ.get("AUTH_PASS"),
            "isDefault": os.environ.get("DS_IS_DEFAULT"),
            "jsonData": os.environ.get("DS_JSON_DATA")
        }
        # Create grafana api path
        self.gf_url = urlunparse(
            (
                self.scheme,
                ":".join((os.environ.get("GF_HOST", "localhost"), os.environ.get("GF_PORT", "3000"))),
                self.api_path, "", "", ""
            )
        )
        # Init requests session
        self.auth = os.environ.get("GF_USER", "admin"), os.environ.get("GF_PASS", "admin")
        self.sess = requests.Session()

        print "Parameters: "
        print json.dumps(self.params)

    def init_datasource(self):
        '''
            Upload a datasource
            :return bool
        '''

        try:
            print "Adding datasource"
            res = self.sess.post(self.gf_url, data=self.params, auth=self.auth)
            return True
        except Exception as message:
            print "CONNECTION! %s" % message
            return False

    def start(self):
        '''
            Start grafana and check api
            :return tuple - status, grafana process
        '''
        status = False
        # run grafana
        gf_proc = Popen([
            "/usr/sbin/grafana-server",
            "--homepath=/usr/share/grafana",
            "--config=/etc/grafana/grafana.ini",
            "cfg:default.paths.data=/var/lib/grafana",
            "cfg:default.paths.logs=/var/log/grafana"],
            stdout=PIPE
        )
        # wait, until gf api will be available
        # trying 10 times
        retry = 0
        while retry <= 10:
            if self._check_gf():
                status = True
                break
            retry += 1
            sleep(3)

        return status, gf_proc

    def _check_gf(self):
        '''
            Check gf api
            :return bool
        '''
        resp = False
        try:
            print "Connecting to %s" % self.gf_url
            res = self.sess.get(self.gf_url, auth=self.auth)
            resp = True if res and res.status_code == requests.codes.ok else False
            print "Success!"
        except Exception as message:
            print "CONNECTION! %s" % message

        return resp

if __name__ == "__main__":
    gf = Grafana()
    try:
        exit_code = 0
        retry = 0
        status, gf_proc = gf.start()
        if status:
            while retry <= 10:
                if gf.init_datasource():
                    print "*------------SUCCESS! Your datasource was added!------------*"
                    while True:
                        # read gf stdout until it terminated
                        output = gf_proc.stdout.readline()
                        if output == '' and gf_proc.poll() is not None:
                            break
                        if output:
                            print output.strip()
                        sleep(3)
                else:
                    print "*------------FAILURE! Failed adding datasource!-------------*"
                    retry += 1
                    sleep(3)

            exit_code = gf_proc.poll()
    except Exception as error:
        print "*------------ERROR! %s------------*" % error
        exit_code = 1
    finally:
        exit(exit_code)

