import random
import smtplib

def send_otp(email):
    global r_otp
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('anupamsingh.5678901234@gmail.com',password='ynnfuylqzctahhof')
    gen_otp = ''.join([str(random.randint(0,9)) for i in range(6)])
    msg = 'Your otp is '+gen_otp
    try:
        server.sendmail('anupamsingh.5678901234@gmail.com',email,msg)
        server.quit()
    except:
        return 'error'
    else:
        return gen_otp