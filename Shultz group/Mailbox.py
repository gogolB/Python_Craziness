#!/usr/bin/env python

import sys
import os
import imaplib
import getpass
import email
import datetime
import re

#import MySQLdb

# Source: Mailbox.py
# Author: Gogol Bhattacharya
# Date: 1/22/2015
#
# Brief: This class represents the Object Orientated version of the mailer.py module.
#        In this class will be all methods to connect to a mailbox and handle all IMAP details.

# ------------------------------------------------------------------------------
# TODO   Figure out the SSL connection to Gmail servers to prevent the less than secure setting.
# TODO   Add in the file paths to a database for the correct patient.

class Mailbox:

    def __init__(self, mail_server, verbose):
        self.conn = imaplib.IMAP4_SSL(mail_server)
        self.verbose = verbose

    # Sets the IMAP Server, tries to connect to the server.
    def set_IMAP_Server(self, mail_server):
        self.conn = imaplib.IMAP4_SSL(mail_server)

    # Attmepts to login to an account on the IMAP server set on self.conn
    def login(self, username, password):
        # Attempt to login to the connection with the given user and pass.
        try:
            self.conn.login(username, password)
            if self.verbose:
                print ("[*] Login to account (%s) successful!" % username)

        # There was some kind of error. Display hints.
        except imaplib.IMAP4.error:
            print ("*** ERROR *** LOGIN FAILED *** ERROR ***")
            print ("    Please check the following: ")
            print ("        (1) Username")
            print ("        (2) Password")
            print ("        (3) Email Server")
            print ("        (4) Account security settings. (Must be configured to allow non-SSL logins.)")
            print ("        IF SSL LOG-INs ARE ENABLED")
            print ("        (5) Make sure the cert file is valid.")
            print ("        (6) Make sure the key file for the account is valid.")
            sys.exit(1)

    # Logout gracefully
    def logout(self):
        # Disconnect from the server.
        self.conn.logout()

    # Lists all valid folders in this mailbox.
    # TODO Make it print nicer.
    def list_Folders(self):
        # Page the server for a list, get the response and the list if applicable.
        responce, folders = self.conn.list()

        # If everything is okay, print the mailboxes
        if responce == "OK":
            print("==========     All Mailboxes     ==========")
            print(folders)

    # Gets the number of unread emails in the folder given.
    def get_num_unread(self, folder):
        # Gets the status of the folder as well as all the UNSEEN emails.
        folderStatus, UnseenInfo = self.conn.status(folder, "(UNSEEN)")

        # Print the folder status.
        if self.verbose:
            print("[*] %s Status: %s" % (folder, folderStatus))

        # If there is nothing wrong and the connection is valid.
        if folderStatus == 'OK':
            string = UnseenInfo[0].split()[2]
            string = string.decode("UTF-8")
            string = string.strip(').,]')
            return int(string)

    # Prints all unread emails to console.
    def print_all_unread(self, folder):
        # Selects the folder
        self.conn.select(folder)

        # Print Unread Emails
        if self.verbose:
            print()
            print("=================================")
            print("|    Printing unread Emails!    |")
            print("=================================")
            print()

        # Seacrh for all UNSEEN emails (Unread).
        typ, data = self.conn.search(None, '(UNSEEN)')
        for num in data[0].split():

            # Print Header
            print("-------------------------------------------------------------------------------")
            print()

            # Fetches the email using RFC-822 Protocol.
            typ, data = self.conn.fetch(num, '(RFC822)')

            # Gets the binary data from the raw data bytes.
            msg = data[0][1]

            # Gets the actual email from the message string, but first decode the msg in to a UTF-8 string.
            mail = email.message_from_string(msg.decode("UTF-8"))

            # Prints out the info for the email.
            print("Message #%s: %s \nSender: %s \nDate: %s" % (num.decode('UTF-8'), mail['Subject'], mail['From'], mail['Date']))

            # Marks the email as UNSEEN
            typ, data = self.conn.store(num,'-FLAGS','\Seen')

            # Print Footer
            print()
            print("-------------------------------------------------------------------------------")

        # Prints the end of the listing of all unread emails.
        if self.verbose:
            print("-------------------------------------------------------------------------------")
            print("         ===============  No More UNREAD Emails to list ===============")
            print("-------------------------------------------------------------------------------")
            print()

    # Goes through an email and downloads all the attachments.
    def download_all_attachements(self, mail):
        # Attachment found variable.
        attch_found = False

        # Go through the email looking for the attachement
        for part in mail.walk():

            # Its a part of a email thread.
            if part.get_content_maintype() == 'multipart':
                continue

            # There is nothing attached to this email.
            if part.get('Content-Disposition') is None:
                continue

            # There is something attached to this email! (An Attachement)
            filename = part.get_filename()

            restOfPath = self.parse_file_path(mail['SUBJECT'], mail['DATE'])

            # Put the file in its place.
            filepath = "c:/Bilirubin/Downloads/" + restOfPath

            # Is this an actual filename.
            if bool(filename):
                # Attachment Found
                attch_found = True

                # Printing out the name of the file.
                print ("[*] Attachment found! Filename = %s" % filename)

                # Download it?
                resp = input("Download attachment? (Y or N): ")

                # Downloading the attachment.
                if resp == 'Y' or resp == 'y':
                    print ("[*] Downloading.....")

                    # Check if the directory exists.
                    if not os.path.exists(filepath):
                        # Make the directories for the file path.
                        os.makedirs(filepath)

                        # Opening the file for writing in binary format.
                        fp = open(filepath + "/" + self.scrub_filepath(filename) , 'wb')

                        # Write the file Byte for byte while downloading.
                        fp.write(part.get_payload(decode=True))

                        # Close the file path.
                        fp.close()

                        # TODO Add the filepath to the database.

        # No attachment found.
        if not attch_found:
            print ("[*] No Attachments!")

    # Removes all invalid filepath chars and a clean one.
    #      + For windows they are as follows: <>:"/\|?*
    def scrub_filepath(self, filepath):
        return re.sub('[<>:\"\\/?*|]', '', filepath)

    # Generate the proper filepath.
    def parse_file_path(self, Subject, Date):
        # For every '|' that we see, split the string.
        listofparts = Subject.split('|')

        # We only expect to see 3 vertical bars, no more no less. If it doesn't match we don't have a correctly formatted file.
        if len(listofparts) != 3:
            print("[*] Invalid subject header, does not conform to types expected! (<patient number>|<Data type>|<Time>)")
            print("    Returning normal scrubbed subject header. %s => %s" % (Subject, self.scrub_filepath(Subject)))
            return self.scrub_filepath(Subject)

        # Everything lines up, procede to downloading it.
        print("[*] Name conforms to standard.")

        # The first thing should be the patient ID
        PatientId = listofparts[0]

        # The second thing should be the Data type
        Datatype = listofparts[1]

        # The third thing should be the time that it was sent.
        Time = listofparts[2]

        # Scrub and filter user Input
        if Datatype == "Image" or Datatype == "image" or Datatype == "img":
            Datatype = "Image"
        elif Datatype == "Spectra" or Datatype == "spectra" or Datatype == "spec":
            Datatype = "Spectra"
        else:
            Datatype = "Other"

        # Last cleaning before returning to use.
        PatientId   = re.sub('[<>:\"\\/?*|]', '', PatientId)
        Datatype    = re.sub('[<>:\"\\/?*|]', '', Datatype)

        # Get rid of all the other vernier stuff.
        Time        = Time.split()[0]
        Time        = re.sub('[<>:\"\\/?*|]', '', Time)

        # Get rid of all the other gunk in date
        date        = re.sub('[<>:\"\\/?*|]', '-', Date)

        return PatientId + "/" + Datatype + "/" + date + "/" + Time


    # Go through all the emails and process them.
    def process_all_emails(self, folder):
        # Selects folder
        self.conn.select(folder)

        # Print Unread emails
        if self.verbose:
            print()
            print("=======================================")
            print("|    Processing All UNREAD Emails!    |")
            print("=======================================")
            print()

        # Seacrh for all UNSEEN emails (Unread).
        typ, data = self.conn.search(None, '(UNSEEN)')

        # For every unread email.....
        for num in data[0].split():
            # Fetch the raw data from the email using RFC-822 Protocol.
            typ, data = self.conn.fetch(num, '(RFC822)')

            # Get the message raw data from the data.
            msg = data[0][1]

            # Get the string from the msg, but first decode the msg using UTF-8.
            mail = email.message_from_string(msg.decode("UTF-8"))

            # Mark the email as seen.
            typ, data = self.conn.store(num,'+FLAGS','\Seen')

            # Begin handleing this email.
            print("-------------------------------------------------------------------------------")

            # Print the subject.
            print("Subject: %s" % mail['SUBJECT'])

            # Print the sender.
            print("Sender:  %s" % mail['FROM'])

            # Print the Date.
            print("Date:    %s" % mail['DATE'])

            # Print random Space.
            print()

            self.download_all_attachements(mail)

            # End handleing this email.
            print("-------------------------------------------------------------------------------")

            # Process the next email?
            ans = input("Process next email? (Y or N): ")

            # No, exiting application
            if ans=='N' or ans=='n':
                sys.exit(2)

            # New line to seperate the emails and continue processing emails.
            print()

        if self.verbose:
            # No more emails!
            print("-------------------------------------------------------------------------------")
            print("        ===============  No More UNREAD Emails to Process ===============")
            print("-------------------------------------------------------------------------------")
            print()
