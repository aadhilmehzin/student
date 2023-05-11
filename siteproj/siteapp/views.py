from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.
def home(request):
    return render(request,'home.html')
def signup(request):
    return render(request,'register.html')
def usercreate(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'This username already exists !!!!')
                return redirect('signup')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                user.save()
                print('Success....')
        else:
            messages.info(request,'Password doesnt match')
            print("Password is not matching...")
            return redirect('signup')
        return redirect('loginpage')
    else:
        return render(request,'register.html')

def loginpage(request):
    return render(request,'login.html')
 
#@login_required(login_url='loginpage')#(login_required method part)
def about(request):
    if 'uid' in request.session:#session method part
    #if request.user.is_authenticated:#(is authenticated method part)
        return render(request,'about.html') 
    return render(request,'login.html')#(is authenticated method part)&#session method part
def login1(request):
 if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']
    user = auth.authenticate(username=username, password=password) 
    request.session["uid"]=user.id#session method part
    if user is not None:
        if user.is_staff:
            login(request,user)
            return redirect('admins')
        else:
            login(request,user)
            auth.login(request,user)
            messages.info(request,f'Welcome{username}')
            return redirect('about')
        
    else:
        messages.info(request,'Invalid Username or Password. Try again.')
        return redirect('loginpage')
 else:
     return redirect('loginpage')
#@login_required(login_url='loginpage')#(login_required method part)
def logout(request):
    #if request.user.is_authenticated:(is authenticated method part)
    request.session["uid"] = ""#session method part
    auth.logout(request)
    return redirect('home')
def admins(request):
    return render(request,'admin.html')        