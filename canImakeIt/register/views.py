# django user models method
from django.shortcuts import render, redirect
from .forms import RegisterForm

# user registration via django models
def register(response):
    # check if data is valid and save data
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect('/')

    # if form data is invalid
    else:
        form = RegisterForm()



    return render(response, 'register/register.html', {'form':form})
