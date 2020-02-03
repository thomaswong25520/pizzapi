from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


from django.contrib import messages

from .models import Topping, Pizza, Sub, Pasta, Salad, Dinner, User, ShoppingCart, Item, Order
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
    if request.method == 'POST':
        if 'pizza' in request.POST:
            p = Pizza.objects.get(id=request.POST['pizza'])
            item = Item.objects.create(piz=p)
            user_cart.pizzas.add(item)
            user_cart.price += item.piz.price
        if 'sub' in request.POST:
            sub_to_add = Sub.objects.get(id=request.POST['sub'])
            user_cart.subs.add(sub_to_add)
            user_cart.price += sub_to_add.price
        if 'pasta' in request.POST:
            pasta_to_add = Pasta.objects.get(id=request.POST['pasta'])
            user_cart.pastas.add(pasta_to_add)
            user_cart.price += pasta_to_add.price
        if 'salad' in request.POST:
            salad_to_add = Salad.objects.get(id=request.POST['salad'])
            user_cart.salads.add(salad_to_add)
            user_cart.price += salad_to_add.price
        if 'dinner' in request.POST:
            dinner_to_add = Dinner.objects.get(id=request.POST['dinner'])
            user_cart.dinners.add(dinner_to_add)
            user_cart.price += dinner_to_add.price

        user_cart.number_of_articles += 1
        user_cart.save()
        messages.success(request, 'Item successfully added')
        return redirect('menu')
    else:
        context = {
            "toppings": Topping.objects.all(),
            "pizzas": Pizza.objects.all(),
            "subs": Sub.objects.all(),
            "pastas": Pasta.objects.all(),
            "salads": Salad.objects.all(),
            "dinners": Dinner.objects.all()
        }
        return render(request, "menu.html", context)


def cart(request):
    # user_cart = get_object_or_404(ShoppingCart, user_id=request.user.id)
    user_cart = ShoppingCart.objects.get_or_create(user_id=request.user.id)[0]
    print(user_cart)
    # print("HERE")
    # messages.success(request, 'Successfully in mycart.html')
    if request.POST:
        if "del-cart" in request.POST:
            user_cart.delete()
            messages.success(request, 'ShoppingCart successfully emptied')
            return redirect('cart')
        if "del-pizza" in request.POST:
            print(request.POST['del-pizza'])
            user_cart.number_of_articles -= 1
            pid = user_cart.pizzas.values().get(id=request.POST['del-pizza'])['piz_id']
            user_cart.price -= Pizza.objects.get(id=pid).price
            user_cart.pizzas.remove(user_cart.pizzas.get(id=request.POST['del-pizza']))
            user_cart.save()
            Item.objects.get(id=request.POST['del-pizza']).delete()
            messages.success(request, 'Pizza successfully removed from ShoppingCart')
            return redirect('cart')
        
        if "del-sub" in request.POST:
            print(request.POST['del-sub'])
            user_cart.number_of_articles -= 1
            user_cart.price -= user_cart.subs.get(id=request.POST['del-sub']).price
            user_cart.subs.remove(user_cart.subs.get(id=request.POST['del-sub']))
            user_cart.save()
            messages.success(request, 'Sub successfully removed from ShoppingCart')
            return redirect('cart')

        if "del-pasta" in request.POST:
            print(request.POST['del-pasta'])
            user_cart.number_of_articles -= 1
            user_cart.price -= user_cart.pastas.get(id=request.POST['del-pasta']).price
            user_cart.pastas.remove(user_cart.pastas.get(id=request.POST['del-pasta']))
            user_cart.save()
            messages.success(request, 'Pasta successfully removed from ShoppingCart')
            return redirect('cart')

        if "del-salad" in request.POST:
            print(request.POST['del-salad'])
            user_cart.number_of_articles -= 1
            user_cart.price -= user_cart.salads.get(id=request.POST['del-salad']).price
            user_cart.salads.remove(user_cart.salads.get(id=request.POST['del-salad']))
            user_cart.save()
            messages.success(request, 'Salad successfully removed from ShoppingCart')
            return redirect('cart')

        if "del-dinner" in request.POST:
            print(request.POST['del-dinner'])
            user_cart.number_of_articles -= 1
            user_cart.price -= user_cart.dinners.get(id=request.POST['del-dinner']).price
            user_cart.dinners.remove(user_cart.dinners.get(id=request.POST['del-dinner']))
            user_cart.save()
            messages.success(request, 'Dinner successfully removed from ShoppingCart')
            return redirect('cart')

    else:
        context = {
            'user_cart': user_cart,
            'user_id': ShoppingCart.objects.get(user_id=request.user.id).user_id,
            'items': ShoppingCart.objects.filter(user_id=request.user.id).all(),
            'pizzas' : user_cart.pizzas.all(),
            'subs' : user_cart.subs.values(),
            'pastas' : user_cart.pastas.values(),
            'salads' : user_cart.salads.values(),
            'dinners' : user_cart.dinners.values(),
        }
        return render(request, "mycart.html", context)


