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
    # user_cart = get_object_or_404(ShoppingCart, user_id=request.user.id)
    user_cart, created = ShoppingCart.objects.get_or_create(user_id=request.user.id)
    if created:
        print(f'shoppingcart has been created, id is {user_cart.user_id}')
    else:
        print(f'shoppingcart already created!, id is {user_cart.user_id}')
    # print(user_cart)
    # print(type(user_cart))
    # print(user_cart[0])
    # print(user_cart[1])
    if request.method == 'POST':
        # p_id = list(request.POST.keys())[-1]
        # pizza_to_add = get_object_or_404(Pizza, id=p_id)

        # print(type(pizza_to_add))
        print(request.POST)
        if 'pizza' in request.POST:
            print('pizza in here')
            pizza_to_add = Pizza.objects.get(id=request.POST['pizza'])
            user_cart.pizzas.add(pizza_to_add)
        if 'sub' in request.POST:
            print('sub in here')
            
        # user_cart.number_of_articles = user_cart.number_of_articles + 1
        # user_cart.price += pizza_to_add.price
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


def cart(request):
    # user_cart = get_object_or_404(ShoppingCart, user_id=request.user.id)
    user_cart = ShoppingCart.objects.get_or_create(user_id=request.user.id)[0]
    print(user_cart)
    # messages.success(request, 'Successfully in mycart.html')
    if request.POST:
        if "del-cart" in request.POST:
            user_cart.delete()
            messages.success(request, 'ShoppingCart successfully emptied')
            return redirect('cart')
    else:
        context = {
            'user_cart': user_cart,
            'user_id': ShoppingCart.objects.get(user_id=request.user.id).user_id,
            'items': ShoppingCart.objects.filter(user_id=request.user.id).all(),
        }
        return render(request, "mycart.html", context)
