import requests #http requests

from bs4 import BeautifulSoup #web scraping

import smtplib #Send email

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime #date and time

now = datetime.datetime.now()

# email content
content = ''

line = '-'*55

#extract from reddit
def extract_category(url):
    print('Extracting From Reddit...')
    print(f'Url: {url}')
    cnt = ''
    cnt += f'<b>Today\'s Top Growing Communities on <b style="color:red;">Reddit<span>:</b>\n'
    cnt += f'<br><span style="color:green;">{line}</span><br>'
    
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    
    for i,tag in enumerate(soup.find_all('a',attrs={'class':'_2ARwkAW45Urhf_fMfAMi5_ _3WPeZCt6k7JXmTo4Kcf1vQ', 'rel':'noopener'}), start=1):
        href = tag.get('href')
        cnt += f'{i}: <a href="https://www.reddit.com/{href}">{href[1:-1]}</a>\n <br>'
    return(cnt)
    
cnt = extract_category('https://www.reddit.com/subreddits/leaderboard/')
content += cnt
content += f'<br><b style="color:green;">{line}</b><br><br>'
content +=('<br><br>End of Message')

print(content) #print content that is to be sent in the email

#send the email
print('Composing Email...')

# add info
SERVER = '' # "your smtp server"
PORT = 587 # your port number
FROM =  '' # "your from email id"
TO = '' # "your to email id(s)"
PASS = '' # "your email id password"

# Create a message
msg = MIMEMultipart()
msg['Subject'] = f'Today\'s Top Growing Communities [Automated Email] {now.month}-{now.day}-{now.year}'
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
