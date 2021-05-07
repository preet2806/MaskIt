from django.shortcuts import render , redirect
from django.contrib.auth import logout , login , authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request,'maskitapp/index.html')
def manage(request):
    return render(request,'maskitapp/manage.html')
def account(request):
    return render(request,'maskitapp/account.html')
def add(request):
    return render(request,'maskitapp/add.html')
def edit(request):
    return render(request,'maskitapp/edit.html')
def history(request):
    return render(request,'maskitapp/history.html')
def livefeed(request):
    return render(request,'maskitapp/livefeed.html')
def signupview(request):
    return render(request,'maskitapp/signup2.html')
def logoutview(request):
    logout(request)
    return redirect('home')
def loginview(request):
    if(request.method == 'POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if(user is None):
            print ('error')
            return render(request, 'maskitapp/login.html', context={'error':'Username or Password is invalid'})
        else:
            login(request, user)
            return render(request, 'maskitapp/manage.html')
    else:
        return render(request, 'maskitapp/login.html')
def registerview(request):
    if(request.method == 'POST'):
        data = UserCreationForm(request.POST)
        if(data.is_valid()):
            data.save()
        # elif(data.cleaned_data['password1']==data.cleaned_data['password2']):
            user=authenticate(username=data.cleaned_data['username'],password=data.cleaned_data['password1'])
            if(user is None):
                print ('error')
                return render(request, 'maskitapp/login.html', context={'error':'Username or Password is invalid'})
            else:
                login(request, user)
                return render(request, 'maskitapp/signup2.html')
        else:
            return render(request, 'maskitapp/login.html', context={'error':'Passwords do not match'})    
    else:
        form = UserCreationForm()
        return render(request, 'maskitapp/signup.html', context={'form':form}) 