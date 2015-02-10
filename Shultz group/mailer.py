'''
    --- DEPRICIATED ---
        DO NOT USE.


    USE MAILBOX INSTEAD.

    
'''

#!/usr/bin/env python

import sys
import os
import imaplib
import getpass
import email
import datetime

# TODO  Find out SSL connection stuff.
#       We need to figure out how to get all the SSL Stuff to work out. Can't keep disabling SSL logins for accounts.
#import ssl

#ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
M = imaplib.IMAP4_SSL('imap.gmail.com')

def init(username):
    try:
        M.login(username, getpass.getpass("Enter your Pasword: "))
        print ("Login to account %s successful!" % username)
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

# Prints all mailboxes.
def printAllMailBoxes():
    rv, mailboxes = M.list()
    if rv == 'OK':
        print ("Mailboxes: ")
        print (mailboxes)

# Prints all emails in current box.
def printNewEmails():

    # Gets the status of the Inbox.
    folderStatus, UnseenInfo = M.status('INBOX', "(UNSEEN)")
    print("INBOX STATUS: %s " % folderStatus)

    # Prints the number of unread emails.
    string = UnseenInfo[0].split()[2]
    string = string.decode("UTF-8")
    string = string.strip(').,]')
    NotReadCounter = int(string)
    print("Number of Unread Emails: %d" % NotReadCounter)

    # Select the Inbox
    M.select('INBOX')

    # Print Unread Emails
    print()
    print("=================================")
    print("|    Printing unread Emails!    |")
    print("=================================")
    print()

    # Seacrh for all UNSEEN emails (Unread).
    typ, data = M.search(None, '(UNSEEN)')
    for num in data[0].split():

        print("-------------------------------------------------------------------------------")
        print()

        # Fetches the email.
        typ, data = M.fetch(num, '(RFC822)')

        # Gets the binary data from the raw data bytes.
        msg = data[0][1]

        # Gets the actual email from the message string, but first it needs to decode the msg in to a UTF-8 string.
        mail = email.message_from_string(msg.decode("UTF-8"))

        # Prints out the info for the email.
        print("Message: %s: %s \nFrom %s @ %s" % (num.decode('UTF-8'), mail['Subject'], mail['From'], mail['Date']))

        # Marks the email as UNSEEN
        typ, data = M.store(num,'-FLAGS','\Seen')
        print()

        print()
        print("-------------------------------------------------------------------------------")


    print("-------------------------------------------------------------------------------")
    print("         ===============  No More UNREAD Emails to list ===============")
    print("-------------------------------------------------------------------------------")
    print()

    process_mailbox()

# Actually goes through the INBOX and processes all the UNSEEN emails.
def process_mailbox():

    # Gets the status of the INBOX and All UNSEEN Info.
    folderStatus, UnseenInfo = M.status('INBOX', "(UNSEEN)")
    print("INBOX STATUS: %s " % folderStatus)

    # Gets the Number of UNREAD Emails.
    string = UnseenInfo[0].split()[2]
    string = string.decode("UTF-8")
    string = string.strip(').,]')
    NotReadCounter = int(string)
    print("Number of Unread Emails: %d" % NotReadCounter)

    # Prints the Processing Unread Emails.
    print()
    print("===================================")
    print("|    Processing unread Emails!    |")
    print("===================================")
    print()

    # Select the INBOX.
    M.select('INBOX')

    # Search through all the UNSEEN.
    typ, data = M.search(None, '(UNSEEN)')

    # Go through every email.
    for num in data[0].split():

        # Fetch the raw data from the email.
        typ, data = M.fetch(num, '(RFC822)')

        # Get the message raw data from the data.
        msg = data[0][1]

        # Get the string from the msg, but first decode the msg using UTF-8.
        mail = email.message_from_string(msg.decode("UTF-8"))

        # Mark the email as seen.
        typ, data = M.store(num,'+FLAGS','\Seen')

        # Begin handleing Emails.
        print("-------------------------------------------------------------------------------")

        # Print the subject.
        print("Subject: %s" % mail['SUBJECT'])

        # Print the sender.
        print("Sender:  %s" % mail['FROM'])

        # Print the Date.
        print("Date:    %s" % mail['DATE'])

        # Print random Space.
        print()

        attch_found = False

        # Go through the email looking for the attachement
        for part in mail.walk():

            # Its a reply to a email thread.
            if part.get_content_maintype() == 'multipart':
                #print("No Attachments!")
                continue

            # There is nothing attached to this email.
            if part.get('Content-Disposition') is None:
                #print("No Attachments!")
                continue

            # There is something attached to this email!! (An Attachements)
            filename = part.get_filename()
            filepath = "Downloads/" + mail['SUBJECT']

            # Is this an actual filename.
            if bool(filename):
                # Attachment Found
                attch_found = True

                # Printing out the name of the file.
                print ("Attachment Filename = %s" % filename)
                print ("Downloading!")

                # Check if the directory exists.
                if not os.path.exists(filepath):
                    # Make the directories for the file path.
                    os.makedirs(filepath)

                # Opening the file for writing in binary format.
                fp = open(filepath + "/" + filename , 'wb')

                # Write the file Byte for byte while downloading.
                fp.write(part.get_payload(decode=True))

                # Close the file path.
                fp.close()

        if not attch_found:
            print ("No Attachments!")

        # End of Mail
        print("-------------------------------------------------------------------------------")
        print()

        # Process the next Email.
        ans = input("Next Email? ")
        if(ans == "n" or ans == "N"):
            sys.exit(2)
        print()

    # No more emails!
    print("-------------------------------------------------------------------------------")
    print("        ===============  No More UNREAD Emails to Process ===============")
    print("-------------------------------------------------------------------------------")
    print()
