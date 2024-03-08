
import smtplib
import ssl
from email.message import EmailMessage

feedback = "Hola, soy Johan Pina y este es un feedback para la Model UAI"

msg = EmailMessage()
msg['Subject'] = 'Nuevo feedback para la Model UAI'
msg['From'] = 'jspinad@gmail.com'
msg['To'] = 'johanpina1420@gmail.com'
msg.set_content(feedback)

context = ssl.create_default_context()

# Configura los parámetros del servidor SMTP y envía el correo electrónico
with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
    smtp.login('jspinad@gmail.com', 'caar kfqv zjoo isfn')
    smtp.sendmail("jspinad@gmail.com","johanpina1420@gmail.com",msg.as_string())

