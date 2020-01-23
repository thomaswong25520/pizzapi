from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages

from .models import Topping, User, ShoppingCart
from .forms import SignUp


def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            password1 = form.cleaned_data.get('password1')
            messages.success(request, 'Account successfully created')
            return redirect('home')
    else:
        form = SignUp()
    return render(request, 'signup.html', {'form': form})
            
    
def menu(request):
    if request.method == 'POST':
         messages.success(request, 'Item successfully added')
         return redirect('menu')
    else:
        context = {
            "toppings": Topping.objects.all()
        }
    return render(request, "menu.html", context)


# def cart(request):
#     user_cart = ShoppingCart.objects.all()
#     orders = 
