import configparser
import getpass
import argparse, sys
import caldav


class CalInfo:
    def __init__(self):
        self.url = None
        self.usrname = None
        self.passwd = None
        self.cal_shortnames = {}

    def readconfig(self, confname):
        cp = configparser.ConfigParser()
        try:
            cp.read(confname)
        except configparser.Error:
            raise "parse error config file"

        for (sectname, sect) in cp.items():
            if 'url' in sect.keys():
                self.url = sect.get('url')
                self.usrname = sect.get('username')
                self.passwd = sect.get('password')
            elif 'calname' in sect.keys():
                self.cal_shortnames[sect['calname']] = sectname


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
        cal_shortnames = self.calinfo.cal_shortnames
        for c in self.principal.calendars():
            shortname = cal_shortnames.get(c.name, c.name)
            self.calendars[shortname] = c

    def print_calendars(self, config_style=False):
        if not config_style:
            for calname in self.calendars.keys():
                print(calname)
        else:
            shortnames = self.calinfo.cal_shortnames
            for (i,c) in enumerate(self.calendars.values()):
                sectname = shortnames.get(c.name)
                if not sectname:
                    sectname = "Calendar %d" % i
                print("[%s]\ncalname = %s\n" % (sectname, c.name))


def test():
    cdget = CalDVGetState()
    cdget.connect()
    cdget.print_calendars(True)


if __name__ == "__main__":
    pass
