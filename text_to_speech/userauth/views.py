
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from text_to_speech.settings import *
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

                
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        myuser.is_active = True

        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to Gaming world Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Gaming world!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n from Gaming world Team"        
        from_email = EMAIL_HOST_USER
        to_list = [myuser.email]

        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Gaming world Login!!"
        passwordResetTokenGenerator = PasswordResetTokenGenerator()
        message2 = render_to_string('userauth/email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': passwordResetTokenGenerator.make_token(myuser)
        })
        print('passwordResetTokenGenerator.make_token(myuser)'+ passwordResetTokenGenerator.make_token(myuser))
        print('urlsafe_base64_encode(force_bytes(myuser.pk))' + urlsafe_base64_encode(force_bytes(myuser.pk)))
        email = EmailMessage(
        email_subject,
        message2,
         EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        send_mail(subject, message, from_email, to_list, fail_silently=False)
     
    return render(request,"userauth/register.html")

def activate(request,uidb64,token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None
    passwordResetTokenGenerator = PasswordResetTokenGenerator()
    if myuser is not None and passwordResetTokenGenerator.check_token(myuser,token):
        myuser.is_active = True
       
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=email, password=pass1)
        
        if user is not None:
            login(request, user)
            username = user.username
            # messages.success(request, "Logged In Sucessfully!!")
            
            return render(request, "tts/index.html",{"fname":username})
        else:
            
            messages.error(request, "Bad Credentials!!")
            return render(request,"userauth/signin.html")
    
    
    return render(request,"userauth/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return render(request,"userauth/signout.html")