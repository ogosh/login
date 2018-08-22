# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, LoginForm, EmailSignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import email_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
               if user.is_active:
                   if user.last_login == None and not user.email:
                       login(request, user)
                       return redirect('email_sign_up')
                   else:
                       login(request, user)
                       return HttpResponse('Authenticated '\
                                       'successfully')
               else:
                   return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'login.html',{'form': form})


def email_sign_up(request):
    if request.method == 'POST':
        try:
            form = EmailSignupForm(data=request.POST, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Email Activation'
                message = render_to_string('activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':email_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
        except Exception, err:
            raise err

    else:
        form = EmailSignupForm()
    return render(request, 'email_sign_up.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception, err:
        user = None
        raise err
    if user is not None and email_activation_token.check_token(user, token):
        user.save()
        return redirect('/settings/security')
        #return HttpResponse("Thank you for your email confirmation. Now you can login your account")
    else:
        return HttpResponse("Email Activation link is invalid")  
