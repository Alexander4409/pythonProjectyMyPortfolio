from django.shortcuts import render
from .models import Skill

def index (request):
    skills = Skill.objects.all()
    return render(request, 'skills/index.html', {'skills': skills})