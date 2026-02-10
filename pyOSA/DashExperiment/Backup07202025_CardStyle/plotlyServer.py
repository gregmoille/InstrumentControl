#! /Users/greg/miniforge3/bin/python

from paramiko import SSHClient
from scp import SCPClient
import sys, os
import tempfile
import secrets
import pathlib
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

class plotlyServer:
    def __init__(self, **kwargs):
        self._fig = kwargs.get("fig", None)
        self._figname = kwargs.get("figname", None)
        self._server = kwargs.get("server", "10.0.0.48")
        self._path = kwargs.get("path", "/usr/share/nginx/html/")
        self._username = kwargs.get("username", "greg")
        self._password = kwargs.get("password", "Gaia74200<3")
        self._url = kwargs.get("url", "https://nanophotonicsjqi.io/plots/")

        if not self._fig is None:
            self.createFileName()
            self.createTempHTML()
            self.transferHTML()
            self.figurl = self._url + self._filename
            print("URL to plot: ")
            print(self.figurl)
        else:
            try: 
                self.plot = self.retrieveHTMLdata(self._url)
            except Exception as e:
                print("Error retrieving HTML data: ", e)
            
        
    def retrieveHTMLdata(self, url):
        resp = requests.get(url, verify=False)
        soup = BeautifulSoup(resp.content, 'html.parser')
        plot = soup.findAll('script')[-1].text
        plot = re.findall(r'"x":\[(.*?)\],"y":\[(.*?)\]', plot)
        plot = [list(i) for i in plot]
        for pp in plot:
            pp[0] = [float(x) for x in pp[0].split(',')]
            pp[1] = [float(x) for x in pp[1].split(',')]
        output = [pd.DataFrame({'x': x, 'y': y}) for x, y in plot]
        return output

    def createFileName(self):
        secret = secrets.token_urlsafe(50)
        self._filename = secret + "&figname=" + self._figname + '.html'

    def createTempHTML(self):
        tmpdir = pathlib.Path(tempfile.gettempdir())
        self._tempFile = str(tmpdir.joinpath(self._figname + ".html"))
        self._fig.write_html(self._tempFile)
        os.chmod(self._tempFile, 0o666)

    def transferHTML(self):
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(self._server, username=self._username, password=self._password)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(self._tempFile, self._path + self._filename)
        os.remove(self._tempFile)

    def removeHTML(self):
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(self._server, username=self._username, password=self._password)
        sftp = ssh.open_sftp()
        sftp.remove(self._path + self._filename)


# secret = secrets.token_urlsafe(50)
# file = sys.argv[1]
# filename = file.split('/')[-1]
# filename = secret + "&figname=" + filename
# os.chmod(file, 0o444)
# server = '10.0.0.48'
# path = '/usr/share/nginx/html/'
# ssh = SSHClient()
# ssh.load_system_host_keys()
# ssh.connect(server, username='greg', password='Gaia74200<3')

# with SCPClient(ssh.get_transport()) as scp:
# scp.put(file, path + filename)
# scp.get('test2.txt')

# print("URL to plot: https://nanophotonicsjqi.io/plots/" + filename)
