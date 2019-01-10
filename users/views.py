from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
	if request.method == 'POST':
		registrationform = UserCreationForm(request.POST)
		if registrationform.is_valid():
			registrationform.save()
			newuser = registrationform.cleaned_data.get('username')
			messages.success(request, f'Account created for {newuser}, please log in')
			return render (request, 'users/register.html', {'registrationform': registrationform, 'title': 'Registration'})
	else:
		registrationform = UserCreationForm()
	return render (request, 'users/register.html', {'registrationform': registrationform, 'title': 'Registration'})


