from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from .models import Topping, Pizza, Sub, Pasta, Salad, Dinner, User, ShoppingCart
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
    user_cart = get_object_or_404(ShoppingCart, user_id=request.user.id)
    if request.method == 'POST':
        messages.success(request, 'Item successfully added')
        return redirect('menu')
    else:
        context = {
            "toppings": Topping.objects.all(),
            "pizzas": Pizza.objects.all(),
            "subs": Sub.objects.all(),
            "pastas": Pasta.objects.all(),
            "salads": Pasta.objects.all(),
            "dinners": Salad.objects.all()
        }
        return render(request, "menu.html", context)


# def cart(request, id=None):
#     user_cart = get_object_or_404(ShoppingCart, id=id)
#     messages.success(request, 'Successfully in mycart.html')
#     context = {
#         'user_cart': user_cart
#         "toppings": Topping.objects.all(),
#         "pizzas": Pizza.objects.all(),
#         "subs": Sub.objects.all(),
#         "salads": Pasta.objects.all(),
#         "dinners": Salad.objects.all()
#     }
#     return render(request, "mycart.html", context)


def cart(request):
    user_cart = get_object_or_404(ShoppingCart, user_id=request.user.id)
    messages.success(request, 'Successfully in mycart.html')
    context = {
        'user_cart': user_cart,
        'user_id': ShoppingCart.objects.get(user_id=request.user.id).user_id
    }
    return render(request, "mycart.html", context)
