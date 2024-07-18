from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
# Create your views here.

def home(request):
	records = Record.objects.all()
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

	

	return render(request,'home.html',{'records': records})



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out Succesfully!")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			#AUTHENTICATE AND LOGIN
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username = username, password = password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered!")
			return redirect(home)
	else:
		form = SignUpForm()
		return render(request, 'register.html',{'form': form}) 

	return render(request, 'register.html',{'form': form}) 

	



def customer_record(request, pk):
	if request.user.is_authenticated:
		#Look up the record
		customer_record = Record.objects.get(id = pk)
		return render(request, 'record.html', {'customer_record' : customer_record})

	else:
		messages.error(request, "You Must Be Logged In to View The Record")
		return redirect('home')

def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id = pk)
		delete_it.delete()
		messages.success(request, "The Record Has Been Deleted Successfully!")
		return redirect('home')
	else:
		messages.success(request, "Oops! You Must Be Logged In To Delete Records!")
		return redirect('home')

	
def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added Successully")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	
	else:
		messages.error(request, "Oops! You Must Be Logged In To Add Records!")
		return redirect('home')



def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id = pk)
		form = AddRecordForm(request.POST or None, instance= current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "The Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.error(request, "Oops! You Must Be Logged In To Update Records!")
		return redirect('home')


