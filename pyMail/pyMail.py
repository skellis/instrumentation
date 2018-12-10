#Modified for python 2.71 by Scott Ellis 12-10-2018
#A short script for sending bulk emails with a message of message.txt sent to recipients mycontacts.txt
#https://arjunkrishnababu96.gitlab.io/post/send-emails-using-code/
#This code has been set up to send from a gmail account but host='smtp.gmail.com', port=587 can be modified to send from other account
#Common Providers
#Google Apps / Gmail     
#SMTP HOST: smtp.gmail.com
#SMTP PORT: 587

#Yahoo   SMTP HOST: smtp.mail.yahoo.com
#SMTP PORT: 465 

#Office 365  
#SMTP HOST:  smtp.office365.com
#SMTP PORT: 587 

#Rackspace   
#SMTP HOST:  secure.emailsrvr.com
#SMTP PORT:  465

import smtplib
import io
import shutil
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'fakeemail@gmail.com'
PASSWORD = 'fakepassword'

def get_contacts(filename):
    names = []
    emails = []
    with io.open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with io.open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    names, emails = get_contacts('mycontacts.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    print s
    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        text = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        subject = "Automated Message from pyMail"
        # setup the parameters of the message
        message = 'Subject: {}\n\n{}'.format(subject, text)


        
        # send the message via the server set up earlier.
        s.sendmail(MY_ADDRESS,email,message)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()