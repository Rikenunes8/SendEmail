import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def setup_message(sender, receiver, subject, text, attachments): # attachments should be a list
  # Setup the MIME
  message = MIMEMultipart()
  message['From'] = sender
  message['To'] = receiver
  message['Subject'] = subject

  # The body for the mail
  message.attach(MIMEText(text, 'plain'))
  
  # The attachments for the mail
  for filename in attachments:
    attachment = open(filename, 'rb')
    part = MIMEApplication(attachment.read(), Name=filename)
    attachment.close()
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % filename.split('/')[-1]
    message.attach(part)
  
  return message

def create_smtp_session(address, password):
  # Create SMTP session for sending the mail
  session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port
  session.starttls() # enable security
  session.login(address, password) # login with mail_id and password
  return session

def parse():
  argv = sys.argv
  argc = len(argv)
  if argc != 7 and argc != 1:
    print('Usage: send_email.py sender password receiver subject text attachments')
    print("e.g. send_email.py test123@gmail.com pass1234 receiver_test@gmail.com 'Important subject' 'This is a try text' 'document.txt another.pdf'")
    return None

  if argc != 1:
    sender    = argv[1]
    password  = argv[2]
    receiver  = argv[3]
    subject   = argv[4]
    text      = argv[5].replace('\\n', '\n')
    attachments = argv[6].split()
  else:
    sender    = input('From: ')
    password  = input('Password: ')
    receiver  = input('To: ')
    subject   = input('Subject: ')
    text      = input('Text:\n').replace('\\n', '\n')
    attachments = input('Attachments (e.g. filepath_1 filepath_2 filepath_3):\n').split()

  return (sender, password, receiver, subject, text, attachments)

def main():
  parsed = parse()
  if parsed == None:
    return

  sender, password, receiver, subject, text, attachments = parsed

  message = setup_message(sender, receiver, subject, text, attachments)

  session = create_smtp_session(sender, password)
  mail = message.as_string()

  print('Mail Sending...')
  session.sendmail(sender, receiver, mail)
  session.quit()
  print('Mail Sent')

if __name__ == '__main__':
  main()