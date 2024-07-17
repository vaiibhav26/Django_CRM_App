from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def home(request):
	# check to see if logging in
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		#AUTHENTICATE
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.error(request, "Sorry! We Couldn't Log You In!")

	

	return render(request,'home.html',{})



def logout_user(request):
	logout(request)
	messages.success(request, "Thanks for spending some quality time with the web site today. You Have Been Logged Out")
	return redirect('home')


def register_user(request):
	
	return render(request, 'register.html',{}) 
	

