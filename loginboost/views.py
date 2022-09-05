# from contextlib import _RedirectStream
# import email
# from readline import get_current_history_length
from email.message import EmailMessage
from lib2to3.pgen2.tokenize import generate_tokens
from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from login import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.utils.encoding import force_str
from base64 import urlsafe_b64encode
from .tokens import generate_token
import django
django.utils.encoding.force_text = force_str
# Create your views here.

def lobby(request):
    return render(request,"loginboost/index.html")

def signup(request):
    if request.method == "POST":
        # username = request.POST.get('fn')
        fn = request.POST.get('fn')
        sn = request.POST.get('ln')
        un= request.POST.get('un')
        em = request.POST.get('em')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        tac = request.POST.get('tac')
        #CHECKING IF A USER NAME ACCOUNT ALREADY EXISTS
        if User.objects.filter(username=un):
           messages.error(request, "Your request for creating an account using the username ",{'fn':fn}," alreay exists!!!")
           return redirect('lobby')
       
        if User.objects.filter(email=em):
          messages.error(request, "Your request for creating an account using the email alreay exists!!!")
          return redirect('lobby')
      
        if len(un)>16:
           messages.error(request, "User name must be within 16 characters!!!")
          
        if pass1 != pass2:
           messages.error(request, "Password Din't match!!!")
             
        if not un.isalnum():
           messages.error(request, "Username must be Alplanumeric!!!")
           return redirect('lobby')
        #reg in backend the user details
        myuser = User.objects.create_user(un,em,pass1)
        myuser.first_name =fn
        myuser.sur_name =sn
        # myuser.curr_pwd = pass2
        myuser.T_C =tac
        myuser.is_active =False
        myuser.save()
        messages.success(request, "Congratulations for joining our community!!!\n We have sent you a Confirmation email to activate your account")
        
       #Welcome message to email
        subject = "Welcome to TCE~BUZZ Login!!!" 
        message = "Hello user: "+ myuser.first_name +"!! \n" + "Welcome to TCE~BUZZ !!! \n We Welcome you to our community and thank you for visiting our website \n We have also sent you a confirmation email to verify your email address in order to activate your account. \n\n Thanking you \n TCE Buzzer"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently =True)
        
        #Confirmation email to the users
        current_site = get_current_site(request)
        email_sub = "Join us by authenticating into the Buzz site "
        message2 = render_to_string('email_confirm.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid' : urlsafe_b64encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_sub,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently =True
        email.send()
        return redirect('signin')
    return render(request,"loginboost/signup.html")
def signin(request):
    if request.method == "POST":
        un= request.POST.get('un')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(username =un, password=pass1)
        
        if user is not None:
            login(request,user)
            fn = user.first_name
            return render(request,"loginboost/index.html",{'fn':fn})
            
        else:
            messages.error(request, "Error:404 : Poor Connection") 
            return redirect('lobby')  
    return render(request,"loginboost/signin.html")
def signout(request):
    logout(request)
    messages.success(request,"Logged-out Successfully!!")
    return redirect('lobby')
    # return render(request,"loginboost/signup.html")
def activate(request,uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser =None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True    
        myuser.save()
        login(request, myuser)
        return redirect('lobby')
    else:
        return render(request,'activation_failed.html')
def avc(request):
      return render(request,"loginboost/avc.html")
def Meet(request):
      return render(request,"loginboost/Meet.html")