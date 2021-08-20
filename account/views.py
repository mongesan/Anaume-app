from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from main.models import Note, Text, User


@login_required
def index(request):
    notes = Note.objects.filter(user=request.user)
    c_text = 0
    c_word = 0
    for note in notes:
        texts = Text.objects.filter(note=note)
        for text in texts:
            c_text += 1
            c_word += len(text.words)

    data = {
        "c_note": Note.objects.filter(user=request.user).count(),
        "c_text": c_text,
        "c_word": c_word
    }
    return render(request, 'account/account.html', data)


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


@login_required
def delete_user(request):
    if request.method == 'POST':
        User.objects.filter(username=request.user.username).delete()
        logout(request)
        return redirect('main:index')
    else:
        return render(request, 'account/delete_user.html')
