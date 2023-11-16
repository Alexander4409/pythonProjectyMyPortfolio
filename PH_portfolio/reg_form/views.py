from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import DTModel
from .forms import DTModelForm, SignupForm
from django.contrib import messages
from .forms import Discount

from datetime import timedelta



# Create your views here.
def home(request):
    return render(request,'index')

#рабочая регистрация
def signupuser(request):
    if request.method == "GET":
        return render(request, "reg_form/signupuser.html", {'form': SignupForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    email=request.POST['email'],  # Добавьте эту строку для включения адреса электронной почты
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('reg_form:currentRegForm_v2')
            except IntegrityError:
                return render(request, "reg_form/signupuser.html", {'form': SignupForm(),
                                                                    "error": "Такой пользователь уже существует"})
        else:
            return render(request, "reg_form/signupuser.html",
                          {'form': SignupForm(),
                           "error": "Пароли не совпадают!"})


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
            if user.is_staff:
                # Если пользователь - админ, перенаправляем его на страницу блога
                return redirect('blog:create_blog')
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
            dtmodel.calculate_duration_and_price()

            # Проверка значения favorites
            if request.POST.get('favorites'):
                dtmodel.toggle_favorite(request.user)

            selected_date = dtmodel.date
            # selected_start_time = dtmodel.time
            # selected_end_time = dtmodel.end_time

            # Проверка наличия записей на выбранную дату и временной интервал
            conflicting_records = DTModel.objects.filter(
                date=selected_date,
                # time__lte=selected_end_time,
                # end_time__gte=selected_start_time,
            ).exclude(id=dtmodel.id)

            # Проверка на прошедшую дату
            if selected_date < timezone.now().date():
                messages.error(request, "Вы не можете записаться на прошедшую дату.")
                return redirect('reg_form:currentRegForm_v2')

            if dtmodel.time > dtmodel.end_time:
                messages.error(request, "Время начала фотосессии, должна быть меньше времени конца фотосессии)")
                return redirect('reg_form:currentRegForm_v2')

            if conflicting_records.exists():
                messages.error(request, "На выбранную дату уже есть другая фотосессия.")
            else:
                discounts = Discount.objects.filter(start_date__lte=selected_date, end_date__gte=selected_date)

                if discounts.exists():
                    # Применяем первую подходящую скидку
                    discount = discounts[0]
                    dtmodel.discount = discount
                    dtmodel.calculate_duration_and_price()

                dtmodel.save()
                messages.success(request, "Фотосессия успешно забронирована!")

                form = DTModelForm()
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")

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


@login_required
def edit_record(request, record_id):
    record = get_object_or_404(DTModel, id=record_id)

    # Проверяем, можно ли редактировать запись
    if record.date - timedelta(days=3) < timezone.now().date():
        return render(request, 'reg_form/edit_record.html', {'record': record, 'error_message': 'Нельзя редактировать запись за 3 дня до начала фотосессии.'})

    if request.method == 'POST':
        form = DTModelForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('reg_form:photosessions')
    else:
        form = DTModelForm(instance=record)

    return render(request, 'reg_form/edit_record.html', {'form': form, 'record': record})

