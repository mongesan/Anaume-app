from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


def index(request):
    print(request.user)
    return HttpResponse('account page')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account:index')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form, 'user': request.user, })