# ITOnline

Python3.7 + Django 2.1.4


用户模块：
  *用户model继承AbstractUser
  *Email验证码model
  *首页轮播图model
  
  
  
机构模块：
  *城市model
      |
      |
     \|/
  *机构model
      |
      |
     \|/
  *讲师model
  
  
  
课程模块：



操作模块：


功能：
1、用户账号注册、激活、登录、找回密码功能。
  *django.forms验证表单
  *django-simple-captcha实现验证码功能
  *django.core.mail.send_mail实现邮件发送功能
2、课程机构展示
  *django-pure-pagination实现分页功能
