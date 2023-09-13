from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import DTModel
from .forms import DTModelForm



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


@login_required
def currentRegForm_v2(request):
    if request.method == "POST":
        form = DTModelForm(request.POST)
        if form.is_valid():
            dtmodel = form.save(commit=False)
            dtmodel.user = request.user
            dtmodel.calculate_duration_and_price()  # Рассчитать стоимость и продолжительность
            dtmodel.save()
            form = DTModelForm()
        else:
            print("Error", form.errors)
    else:
        form = DTModelForm()

    return render(request, "reg_form/currentRegForm_v2.html", {'form': form})




@login_required
def photosessions(request):
    sort_by = request.GET.get('sort_by', 'booking_date')

    if sort_by == 'booking_date':
        photo_S = DTModel.objects.filter(user=request.user).order_by("-date_time")
    elif sort_by == 'photosession_date':
        photo_S = DTModel.objects.filter(user=request.user).order_by("date_time")
    else:
        photo_S = DTModel.objects.filter(user=request.user).order_by("-date_time")

    return render(request, 'reg_form/photosessions.html', {'blogs': photo_S, 'user': request.user, 'sort_by': sort_by})


#delete record


def delete_record(request, record_id):
    record = get_object_or_404(DTModel, id=record_id)

    if request.method == 'POST':
        record.delete()
        return redirect('reg_form:photosessions')

    return render(request, 'reg_form/confirm_delete.html', {'record': record})
#edit record
def edit_record(request, record_id):
    record = get_object_or_404(DTModel, id=record_id)

    if request.method == 'POST':
        form = DTModelForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('reg_form:photosessions')
    else:
        form = DTModelForm(instance=record)

    return render(request, 'reg_form/edit_record.html', {'form': form, 'record': record})

