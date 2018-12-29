from django.core.mail import send_mail
from ITOnline.settings import EMAIL_FROM, EMAIL_IP
from users.models import EmailVerityRecord
from random import Random


def send_register_email(email, send_type="register"):
    email_register = EmailVerityRecord()
    code = random_str(16)
    email_register.email = email
    email_register.code = code
    email_register.send_type = send_type
    email_register.save()

    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "欢迎小老弟注册"
        email_body = f"复制下面用链接浏览器打开http://{EMAIL_IP}:8000/active/{code}"
        send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_type == "forget":
        email_title = "欢迎小老弟找回密码"
        email_body = f"找回密码请复制下面用链接浏览器打开http://{EMAIL_IP}:8000/reset/{code}"
        send_mail(email_title, email_body, EMAIL_FROM, [email])


def random_str(randomlen=8):
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlen):
        str += chars[random.randint(0, length)]
    return str
