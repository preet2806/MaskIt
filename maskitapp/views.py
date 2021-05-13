from django.shortcuts import render , redirect
from django.contrib.auth import logout , login , authenticate
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta, timezone
from maskitapp.models import company_table, employee_table, history_table
from uuid import uuid1

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        current_user = request.user.username
    else:
        current_user = "Login"
    return render(request,'maskitapp/index.html', context={'login':current_user})
def manage(request):
    if request.user.is_authenticated:
        current_user = request.user.username
        employeelist=employee_table.objects.filter(company=request.user)
        # print(employeelist[0].image1.url)
        return render(request,'maskitapp/manage.html', context={'login':current_user,'allemp':employeelist})
    else:
        current_user = "Login"
        return render(request,'maskitapp/login.html', context={'login':current_user})
def account(request):
    if request.user.is_authenticated:
        current_user = request.user.username
    else:
        current_user = "Login"
    if(request.method == 'POST'):
        try:
            one_entry = company_table.objects.get(user=request.user)
        except company_table.DoesNotExist:
            user = request.user
            name=request.POST.get('name')
            email=request.POST.get('email')
            message=request.POST.get('message')
            company=company_table(user=user, name=name, email=email, message=message)
            company.save()
        else:
            one_entry.name=request.POST.get('name')
            one_entry.email=request.POST.get('email')
            one_entry.message=request.POST.get('message')
            one_entry.save()
        saved="data saved!"
        return render(request, 'maskitapp/account.html', context={'login':current_user, 'saved':saved}) 
    else:
        if request.user.is_authenticated:
            # Do something for authenticated users.
            try:
                one_entry = company_table.objects.get(user=request.user)
            except company_table.DoesNotExist:
                return render(request,'maskitapp/account.html', context={'login':current_user})
            else:
                name = one_entry.name
                email = one_entry.email
                message = one_entry.message
            return render(request,'maskitapp/account.html', context={'login':current_user, 'name':name, 'email':email, 'message':message})
        else:
            # Do something for anonymous users.
            form = UserCreationForm()
            return render(request, 'maskitapp/login.html', context={'form':form, 'login':current_user}) 
            
def add(request):
    if request.user.is_authenticated:
        current_user = request.user.username
        if(request.method == 'POST'):
            name=request.POST.get('name')
            number=request.POST.get('number')
            image1=request.FILES.get('image1')
            image2=request.FILES.get('image2')
            image3=request.FILES.get('image3')
            image4=request.FILES.get('image4')
            image5=request.FILES.get('image5')
            employee=employee_table(company=request.user, name=name, number=number)
            employee.image1.save(str(uuid1())+"."+image1.name.split(".")[-1],image1)
            employee.image2.save(str(uuid1())+"."+image2.name.split(".")[-1],image2)
            employee.image3.save(str(uuid1())+"."+image3.name.split(".")[-1],image3)
            employee.image4.save(str(uuid1())+"."+image4.name.split(".")[-1],image4)
            employee.image5.save(str(uuid1())+"."+image5.name.split(".")[-1],image5)
            employee.save()
            employeelist=employee_table.objects.filter(company=request.user)
            return render(request,'maskitapp/manage.html', context={'login':current_user,'allemp':employeelist})
        else:
            return render(request,'maskitapp/add.html', context={'login':current_user})
    else:
        current_user = "Login"
        return render(request,'maskitapp/login.html', context={'login':current_user})
def gotoedit(request):
    if request.user.is_authenticated:
        current_user = request.user.username
        empid=request.POST.get('empid')
        print(empid)
        empid=int(empid)
        one_entry = employee_table.objects.get(employee_id=empid)
        name = one_entry.name
        number = one_entry.number
        return render(request,'maskitapp/edit.html', context={'login':current_user, 'empid':empid, 'name':name, 'number':number})
    else:
        current_user = "Login"
        return render(request,'maskitapp/login.html', context={'login':current_user})
def edit(request):
    if request.user.is_authenticated:
        current_user = request.user.username
        if(request.method == 'POST'):
            empid=request.POST.get('empid')
            empid=int(empid)
            one_entry = employee_table.objects.get(employee_id=empid)
            one_entry.name=request.POST.get('name')
            one_entry.number=request.POST.get('number')
            image1=request.FILES.get('image1')
            image2=request.FILES.get('image2')
            image3=request.FILES.get('image3')
            image4=request.FILES.get('image4')
            image5=request.FILES.get('image5')
            one_entry.image1.save(str(uuid1())+"."+image1.name.split(".")[-1],image1)
            one_entry.image2.save(str(uuid1())+"."+image2.name.split(".")[-1],image2)
            one_entry.image3.save(str(uuid1())+"."+image3.name.split(".")[-1],image3)
            one_entry.image4.save(str(uuid1())+"."+image4.name.split(".")[-1],image4)
            one_entry.image5.save(str(uuid1())+"."+image5.name.split(".")[-1],image5)
            one_entry.save()
            employeelist=employee_table.objects.filter(company=request.user)
            return render(request,'maskitapp/manage.html', context={'login':current_user,'allemp':employeelist}) 
        else:
            return render(request,'maskitapp/edit.html', context={'login':current_user})
    else:
        current_user = "Login"
        return render(request,'maskitapp/login.html', context={'login':current_user})
def history(request):
    if request.user.is_authenticated:
        current_user = request.user.username
        if(request.method == 'POST'):
            fromtime=request.POST.get('from')
            totime=request.POST.get('to')
            historylist=history_table.objects.filter(timestamp__range=[fromtime,totime])
            return render(request,'maskitapp/history.html', context={'login':current_user, 'historylist':historylist})
        else:
            historylist=history_table.objects.all()
            return render(request,'maskitapp/history.html', context={'login':current_user, 'historylist':historylist})
    else:
        current_user = "Login"
        return render(request,'maskitapp/login.html', context={'login':current_user})
    
def livefeed(request):
    if request.user.is_authenticated:
        current_user = request.user.username
        momemt=datetime.now()
        fromtime=momemt-timedelta(minutes=5)
        totime=momemt+timedelta(minutes=5)
        violatorlist=history_table.objects.filter(timestamp__range=[fromtime,totime])
        return render(request,'maskitapp/livefeed.html', context={'login':current_user, 'violatorlist':violatorlist})
    else:
        current_user = "Login"
        return render(request,'maskitapp/login.html', context={'login':current_user})
def logoutview(request):
    current_user = "Login"
    logout(request)
    return render(request,'maskitapp/login.html', context={'login':current_user})
def loginview(request):
    if request.user.is_authenticated:
        current_user = request.user.username
    else:
        current_user = "Login"
    if(request.method == 'POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if(user is None):
            print ('error')
            return render(request, 'maskitapp/login.html', context={'error':'Username or Password is invalid', 'login':current_user})
        else:
            login(request, user)
            current_user = request.user.username
            employeelist=employee_table.objects.filter(company=request.user)
            return render(request,'maskitapp/manage.html', context={'login':current_user,'allemp':employeelist}) 
    else:
        return render(request, 'maskitapp/login.html', context={'login':current_user})
def registerview(request):
    if request.user.is_authenticated:
        current_user = request.user.username
    else:
        current_user = "Login"
    if(request.method == 'POST'):
        data = UserCreationForm(request.POST)
        if(data.is_valid()):
            data.save()
        # elif(data.cleaned_data['password1']==data.cleaned_data['password2']):
            user=authenticate(username=data.cleaned_data['username'],password=data.cleaned_data['password1'])
            if(user is None):
                print ('error')
                return render(request, 'maskitapp/login.html', context={'error':'Username or Password is invalid', 'login':current_user})
            else:
                login(request, user)
                return render(request, 'maskitapp/account.html')
        else:
            return render(request, 'maskitapp/signup.html', context={'error':'Passwords do not match', 'login':current_user})    
    else:
        form = UserCreationForm()
        return render(request, 'maskitapp/signup.html', context={'form':form, 'login':current_user}) 
