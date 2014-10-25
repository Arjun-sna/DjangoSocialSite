from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from friends.models import friends

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'],first_name=form.cleaned_data['first_name'],
											last_name=form.cleaned_data['last_name'],email=form.cleaned_data['email'],password=form.cleaned_data['password1'])
			userdet = User.objects.get(username__iexact = form.cleaned_data['username'])
			uid = userdet.id
			name = userdet.username
			storedata = friends(uid=uid,friendid=uid,friendname=name)
			storedata.save()
			return HttpResponseRedirect('/login')
	else:
		form = RegistrationForm()
	return render(request,'registration/register.html',{'form':form})
	
def login_view(request):
	error = False
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username,password=password)
			if user is not None and user.is_active:
				login(request,user)
				request.session['username']=username
				user = User.objects.get(username__iexact = form.cleaned_data['username'])
				request.session['email']=user.email
				request.session['id']=user.id
				return HttpResponseRedirect("/login_success")
			else:
				error = True
	else:
		form = LoginForm()
	return render(request,'registration/login.html',{'form':form,'error':error})
			
def register_success(request):
	return render(request,'registration/success.html')
	
def login_notsuccess(request):
	return render(request,'registration/loginnotsuccess.html',)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
    
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/login')
