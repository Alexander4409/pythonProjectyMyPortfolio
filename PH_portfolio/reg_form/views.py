from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from .models import DTModel

# Create your views here.
def home(request):
    return render(request,'index')

def signupuser(request):
    if request.method == "GET":
        return render(request, "reg_form/signupuser.html", {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('reg_form:currentRegForm_v2')
            except IntegrityError:
                return render(request, "reg_form/signupuser.html", {'form': UserCreationForm(),
                                                                   "error": "Такой пользователь уже есть"})
        else:
            return render(request, "reg_form/signupuser.html",
                          {'form': UserCreationForm(),
                           "error" : "Пароли не совпадают!"})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'reg_form/loginuser.html',{"form": AuthenticationForm()} )
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request,'reg_form/loginuser.html',
                          {"form": AuthenticationForm(),
                           'error': "Неверные данные для входа!"})
        else:
            login(request, user)
            return redirect('reg_form:currentRegForm_v2')

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')

# def currentRegForm(request):
#     #DTModel
#     form = DTForm()
#     return render(request, "reg_form/currentRegForm.html",{'form':form}) #DTModel

#DTModel
class DTForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    your_name = forms.CharField(max_length=64)
    date_input = forms.DateField(widget=AdminDateWidget())
    time_input = forms.DateField(widget=AdminTimeWidget())
    date_time_input = forms.DateField(widget=AdminSplitDateTime())

class DTModelForm(forms.ModelForm):
    date_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    class Meta:
        model = DTModel
        fields = "__all__"
        widgets = {
            'date': AdminDateWidget(),
            'time': AdminTimeWidget(),
        }


def currentRegForm_v2(request):
    #DTModel
    if request.method == "POST":
        form = DTModelForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Error",form.errors)

    form = DTModelForm()
    return render(request, "reg_form/currentRegForm_v2.html",{'form':form}) #DTModel




@login_required
def photosessions(request):
    photo_S = DTModel.objects.filter(user=request.user).order_by("-date")
    return render(request, 'reg_form/photosessions.html', {'blogs': photo_S, 'user': request.user})
