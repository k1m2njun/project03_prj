from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse

def contact(request):
    return render(
        request,
        'single_pages/contact.html'
    )

def landing(request):
    return render(
        request,
        'single_pages/landing.html'
    )
    
def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )

def my_account(request):
    if request.method == 'POST': 
        if request.POST['password'] == request.POST['password']:
            user = User.objects.create(
                password=request.POST['password1'],
                username=request.POST['username'],
                email=request.POST['email'],
            )
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/my_account')
        return render(request, 'single_pages/my_account.html')
    else:
        form = UserCreationForm
        return render(request, 'single_pages/my_account.html', {'form':form})

                
    
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'],
            )
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        return render(request, 'single_pages/signup.html')
    else:
        form = UserCreationForm
        return render(request, 'single_pages/signup.html', {'form':form})
    
    
    
    
    ######################
    # class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password']    

# def signin(request):
#     # if request.method == 'POST':
#     #     form = LoginForm(request.POST)
#     email = request.POST['email']
#     password = request.POST['password']
#     user = authenticate(request, email = email, password = password)
#     if user is not None:
#         login(request, user)
#         return redirect('/')
#     else:
#         return HttpResponse('로그인 실패. 다시 시도 하세요.')
    # else:
    #     form = LoginForm()
    #     return render(request, '/')
    
    
# def change_password(request):        
#     u = User.objects.get(email=request.POST['email'])
#     u.set_password('new password')
#     u.save()
            
    #     if request.POST['password'] == request.POST['password']:
    #         user = User.objects.create_user()
    #         auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    #         return redirect('/')
    #     return render(request, 'single_pages/signup.html')
    # else:
    #     form = UserCreationForm
    #     return render(request, 'single_pages/signup.html', {'form':form})
# def login(request):
#     user = authenticate(email=request.POST['email'], password=request.POST['password'])
#     if user is not None:
#         auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#     else:
#         return HttpResponse('로그인 실패. 다시 시도 하세요.')