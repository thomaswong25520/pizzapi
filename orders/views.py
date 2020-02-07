from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


from django.contrib import messages

from .models import Topping, Pizza, Sub, Pasta, Salad, Dinner, User, ShoppingCart, Item, Order, OrderItem
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
            p = Sub.objects.get(id=request.POST['sub'])
            item = Item.objects.create(sub=p)
            user_cart.subs.add(item)
            user_cart.price += item.sub.price
        if 'pasta' in request.POST:
            p = Pasta.objects.get(id=request.POST['pasta'])
            item = Item.objects.create(past=p)
            user_cart.pastas.add(item)
            user_cart.price += item.past.price
        if 'salad' in request.POST:
            p = Salad.objects.get(id=request.POST['salad'])
            item = Item.objects.create(sal=p)
            user_cart.salads.add(item)
            user_cart.price += item.sal.price
        if 'dinner' in request.POST:
            p = Dinner.objects.get(id=request.POST['dinner'])
            item = Item.objects.create(din=p)
            user_cart.dinners.add(item)
            user_cart.price += item.din.price
            
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
            "dinners": Dinner.objects.all(),

        }
        return render(request, "menu.html", context)

def orders(request):
    user_order = Order.objects.filter(user_id=request.user.id).all()
    messages.success(request, 'Successfully in orders page')
    context = {
        "orders": user_order,
    }
    return render(request, "orders.html", context)



# def details(request):


def cart(request):
    # user_cart = get_object_or_404(ShoppingCart, user_id=request.user.id)
    user_cart = ShoppingCart.objects.get_or_create(user_id=request.user.id)[0]
    print(user_cart)
    # print("HERE")
    # messages.success(request, 'Successfully in mycart.html')
    if request.POST:
        if "del-cart" in request.POST:
            user_cart.pizzas.all().delete()
            user_cart.subs.all().delete()
            user_cart.pastas.all().delete()
            user_cart.salads.all().delete()
            user_cart.dinners.all().delete()
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
            pid = user_cart.subs.values().get(id=request.POST['del-sub'])['sub_id']
            user_cart.price -= Sub.objects.get(id=pid).price
            user_cart.subs.remove(user_cart.subs.get(id=request.POST['del-sub']))
            user_cart.save()
            Item.objects.get(id=request.POST['del-sub']).delete()
            messages.success(request, 'Sub successfully removed from ShoppingCart')
            return redirect('cart')
        
        if "del-pasta" in request.POST:
            print(request.POST['del-pasta'])
            user_cart.number_of_articles -= 1
            pid = user_cart.pastas.values().get(id=request.POST['del-pasta'])['past_id']
            user_cart.price -= Pasta.objects.get(id=pid).price
            user_cart.pastas.remove(user_cart.pastas.get(id=request.POST['del-pasta']))
            user_cart.save()
            Item.objects.get(id=request.POST['del-pasta']).delete()
            messages.success(request, 'Pasta successfully removed from ShoppingCart')
            return redirect('cart')

        if "del-salad" in request.POST:
            print(request.POST['del-salad'])
            user_cart.number_of_articles -= 1
            pid = user_cart.salads.values().get(id=request.POST['del-salad'])['sal_id']
            user_cart.price -= Salad.objects.get(id=pid).price
            user_cart.salads.remove(user_cart.salads.get(id=request.POST['del-salad']))
            user_cart.save()
            Item.objects.get(id=request.POST['del-salad']).delete()
            messages.success(request, 'Salad successfully removed from ShoppingCart')
            return redirect('cart')

        if "del-dinner" in request.POST:
            print(request.POST['del-dinner'])
            user_cart.number_of_articles -= 1
            pid = user_cart.dinners.values().get(id=request.POST['del-dinner'])['din_id']
            user_cart.price -= Dinner.objects.get(id=pid).price
            user_cart.dinners.remove(user_cart.dinners.get(id=request.POST['del-dinner']))
            user_cart.save()
            Item.objects.get(id=request.POST['del-dinner']).delete()
            messages.success(request, 'Dinner successfully removed from ShoppingCart')
            return redirect('cart')
    else:
        context = {
            'user_cart': user_cart,
            'user_id': ShoppingCart.objects.get(user_id=request.user.id).user_id,
            'items': ShoppingCart.objects.filter(user_id=request.user.id).all(),
            'pizzas' : user_cart.pizzas.all(),
            'subs' : user_cart.subs.all(),
            'pastas' : user_cart.pastas.all(),
            'salads' : user_cart.salads.all(),
            'dinners' : user_cart.dinners.all(),
        }
        return render(request, "mycart.html", context)


def confirm(request):
    if request.POST:
        user_cart = ShoppingCart.objects.get_or_create(user_id=request.user.id)[0]
        order = Order.objects.create(user_id=request.user.id, date_order=datetime.now(), qty=user_cart.number_of_articles, tot=user_cart.price)
        # order = Order.objects.create()
        # Pizza.objects.get(id=s2.pizzas.values()[0]['piz_id'])

        for pizza_item in user_cart.pizzas.values():
            order_piz = OrderItem.objects.create(order_id=order.pk)
            order_piz.pizzas.add(Pizza.objects.get(id=pizza_item['piz_id']))

        # for sub_item in user_cart.subs.values():
        #     order_sub = OrderItem.objects.create()
        #     order_sub.item.add(order_sub)

        # for pasta_item in user_cart.pastas.values():
        #     order_pas = OrderItem.objects.create()
        #     order_pas.item.add(order_pas)

        # for salad_item in user_cart.salads.values():
        #     order_sal = OrderItem.objects.create()
        #     order_sal.item.add(order_sal)

        # for dinner_item in user_cart.dinners.values():
        #     order_din = OrderItem.objects.create()
        #     order_din.item.add(order_din)

            
            
        # user_cart.pk = None
        # user_cart.save()
        
        # user_cart_old = ShoppingCart.objects.get_or_create(user_id=request.user.id, pk=request.POST['old_cart'])[0]
        # user_cart_old.delete()
        

        # order.cart.add(user_cart)


        messages.success(request, 'Order confirmed!')
        
        context = {
            'user_cart': user_cart,
            'order': order,
            'pizzas' : order_piz.pizzas.all(),
            'subs' : user_cart.subs.all(),
            'pastas' : user_cart.pastas.all(),
            'salads' : user_cart.salads.all(),
            'dinners' : user_cart.dinners.all(),
        }
        
    return render(request, "confirmation.html", context)


def details(request):
    if request.POST:
        order_id = request.POST['o_id']
        order = Order.objects.get(pk=order_id)
        
        # pizzas = order.cart.pizzas.values()
        qs_pizza = []
        lid_pizza = []
        pizzas = []
        orderitem_qs = OrderItem.objects.filter(order_id=order_id).all()
        for orderitem in orderitem_qs:
            qs_pizza.append(orderitem.pizzas.values()[0])
        for i in qs_pizza:
            lid_pizza.append(i['id'])
        for i in lid_pizza:
            pizzas.append(Pizza.objects.get(id=i))


        context = {
            "order": order,
            "total": order.tot,
            "qty": order.qty,
            "pizzas": pizzas,
            # "subs": ls,
            # "pastas": lpa,
            # "salads": lsa,
            # "dinners": ld,
        }
        return render(request, "details.html", context)
#     l = []
#     lp = []

#     subs = order.cart.subs.values()
#     l1 = []
#     ls = []
#     for i in subs:
#         l1.append(i['sub_id']) 
#     for i in l1:
#         ls.append(Sub.objects.get(id=i))

#     pastas = order.cart.pastas.values()
#     l2 = []
#     lpa = []
#     for i in pastas:
#         l2.append(i['past_id'])
#     for i in l2:
#         lpa.append(Pasta.objects.get(id=i))
        
#     salads = order.cart.salads.values()
#     l3 = []
#     lsa = []
#     for i in salads:
#         l3.append(i['sal_id']) 
#     for i in l3:
#         lsa.append(Salad.objects.get(id=i))

#     dinners = order.cart.dinners.values() 
#     l4 = []
#     ld = []
#     for i in dinners:
#         l4.append(i['din_id']) 
#     for i in l4:
#         ld.append(Dinner.objects.get(id=i))

        

            




# def orderDetails(request):
    

