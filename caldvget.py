import configparser
import getpass
import argparse, sys
import caldav


class CalInfo:
    def __init__(self):
        self.url = None
        self.usrname = None
        self.passwd = None

    def readconfig(self, confname):
        cp = configparser.ConfigParser()
        try:
            cp.read(confname)
        except configparser.Error:
            raise "parse error config file"

        for (sectname, proxy) in cp.items():
            if sectname=='server':
                self.url = proxy.get('url')
                self.usrname = proxy.get('username')
                self.passwd = proxy.get('password')


class CalDVGetState:
    def __init__(self, read_config=True):
        self.calinfo = CalInfo()
        if read_config:
            self.calinfo.readconfig('caldvrc')

    def connect(self):
        if not self.calinfo.url or not self.calinfo.usrname:
            raise "caldav server info missing"
        if not self.calinfo.passwd:
            self.calinfo.passwd = getpass.getpass()

        self.davclient = caldav.DAVClient(url=self.calinfo.url,
                                          username=self.calinfo.usrname,
                                          password=self.calinfo.passwd)
        self.principal = self.davclient.principal()
        self.fetch_calendars()

    def fetch_calendars(self):
        self.calendars = {}
        for c in self.principal.calendars():
            self.calendars[c.name] = c



if __name__ == "__main__":
    pass
