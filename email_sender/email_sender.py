import smtplib
import ssl

from data import config


def send_code(email_to: str, code: str):
    message = f'Привет. Твой код подтверждения - {code}'.encode('utf8')
    email_context = ssl.create_default_context()
    email_from = 'bogdan.bogdan2525@gmail.com'
    TIE_server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    try:
        print("Connecting to smtp server...")
        TIE_server.starttls(context=email_context)
        TIE_server.login(email_from, config.GOOGLE_APP_PASS)
        print('Connected!')
        TIE_server.sendmail(email_from, email_to, message)
        print('Message send successfully!')
    except Exception as ex:
        print(ex)
    finally:
        TIE_server.quit()

