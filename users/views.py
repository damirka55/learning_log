from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm 

def logout_view(request):
    """Завершает сеанс работы с приложением."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def regist(request):
    """Регистрация новых пользователей."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
    
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'users/regist.html', context)
