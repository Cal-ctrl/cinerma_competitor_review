import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

with open('Film Time files/cineworld_times.txt', 'w') as time_txt:
    time_txt.truncate(0)
with open('Film Time files/odeon_times.txt', 'w') as time_txt:
    time_txt.truncate(0)
with open('Film Time files/vue_times.txt', 'w') as time_txt:
    time_txt.truncate(0)

from vue_film_times import vue_film_list
import odeon_test
import cineworld_test


html = Template(Path('index.html').read_text())

email = EmailMessage()
email['from'] = 'Callum McNeil'
email['to'] = 'callum-mcneil@hotmail.com'
email['subject'] = 'Film Times review'

email.set_content(html.substitute({'vue_data': 'See attached for Film Data'}), 'html')

email.add_attachment(open('Film Time files/vue_times.txt', "r").read(), filename="Vue Film Times for Next week.txt")
email.add_attachment(open('Film Time files/odeon_times.txt', "r").read(), filename="Odeon Film Times for next Weekend.txt")
email.add_attachment(open('Film Time files/cineworld_times.txt', "r").read(), filename="Cineworld Film Times for next Weekend.txt")


with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login('callum.pythoncode@gmail.com', '0094Ugcinu')
    smtp.send_message(email)
    print('all good boss!')