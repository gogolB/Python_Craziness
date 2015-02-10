#!/usr/bin/env python

# All Python Modules
import time
import getpass
import sys

# Custom built scrips
from Mailbox import *


mailServer = 'imap.gmail.com'


print("Starting....")
time.sleep(1)
username = input("Enter your GMail: ")
password = getpass.getpass("Enter your password: ")
print("Attempting to connect to mail box (%s)...." % username)
mailbox = Mailbox(mail_server=mailServer, verbose=True)
print("Connection extablished to (%s) \n \t--Attempting Login" % mailServer)
mailbox.login(username=username, password=password)
print()
mailbox.list_Folders()
print()
print("Number of Unread in (INBOX): %d" % mailbox.get_num_unread("INBOX"))
print()
mailbox.print_all_unread("INBOX")
print()
print()
print()
print("Processing (Inbox)...")
mailbox.process_all_emails("INBOX")
print()
print()
print()
print("Logging out of (%s)...." % username)
mailbox.logout()
print("Session to (%s) with username (%s) successfully closed!" % (mailServer, username))
sys.exit(0)
