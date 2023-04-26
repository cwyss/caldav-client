import configparser
import getpass
import argparse, sys
import caldav

config = configparser.ConfigParser()
config.read('caldvrc')
print(config.sections())

url = config['Calendar']['url']
usrname = config['Calendar']['username']
print(url, usrname)

sys.exit()

passwd = getpass.getpass()

client = caldav.DAVClient(url, username="wyss", password=passwd)
calendars = client.principal().calendars()

calendars[0].name
