from django.http import HttpResponse
from django.shortcuts import render

from .models import Topping

# Create your views here.
def menu(request):
    context = {
        "toppings": Topping.objects.all()
    }
    return render(request, "menu.html", context)

