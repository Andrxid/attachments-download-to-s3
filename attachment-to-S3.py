import imaplib
import email
import os
import boto3
import random
import string

# initializing connections
# mail connection
username = "your email"
password = "your password"
mail = imaplib.IMAP4_SSL("email host ex: imap.mail.com")
mail.login(username, password)
#---------------------------------------

# Bucket S3 connections
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='your aws s3 id key',
    aws_secret_access_key='your access key'
)

# check availble buckets
for bucket in s3.buckets.all():
    print("Bucket available: " + bucket.name)

# filtro per le mail da selezionare
mail.select("Inbox")
type, data = mail.search(None, 'UNSEEN', 'Subject', 'your subject')
mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
    
# converto bytestring in stringa normale decodifica utf8
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    
# downloading attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        print("file Name: " + fileName)
        
        # creating directory if not exists
        if os.path.exists('attachments'):
            pass
        else:
            print("creating attachments directory...\n")
            os.mkdir("attachments")
        
        if bool(fileName):
            filePath = os.path.join('attachments/', fileName)
            print(filePath)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                
        # printing lowercase
        letters = string.ascii_lowercase
        randomString = ''.join(random.choice(letters) for i in range(10))
        
        #upload dei file nel bucket prescelto
        nameBucket = "bucket-test12"
        s3.Bucket(nameBucket).upload_file(Filename='attachments/' + fileName, Key=randomString)
        print("\nfile: " + fileName + " uploaded succesfully with key: " + randomString)
        
        # elimino i file scaricati dopo l upload su S3
        os.remove(path=filePath)
                

            