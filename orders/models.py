from django.contrib import admin

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

# Create your models here.


class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return(f"{self.name}")
    
    
class Pizza(models.Model):
    PIZZA_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )

    pizza_type = models.CharField(max_length=64)
    pizza_size = models.CharField(max_length=1, choices=PIZZA_SIZES)
    qty_toppings = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    toppings = models.ManyToManyField(Topping, related_name='pizzas', blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Price in $")

    
    def __str__(self):
        return f"Size: {self.get_pizza_size_display()}, Type: {self.pizza_type}, Number of Toppings: {self.qty_toppings},  Price: {self.price}, Toppings: {self.toppings.in_bulk()}"
    
    def save(self, *args, **kwargs):
        super(Pizza, self).save(*args, **kwargs)
        self.toppings.add(Topping.objects.get(name='Cheese'))

    
class Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Price in $")

    def __str__(self):
        return f"{self.name} : {self.price}"
    


    
class Sub(models.Model):
    SUBS_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )

    subs_size = models.CharField(max_length=1, choices=SUBS_SIZES)
    name = models.CharField(max_length=64)
    extras = models.ManyToManyField(Extra, related_name='subs', blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Price in $")

    def __str__(self):
        return f"{self.name}, {self.get_subs_size_display()} : {self.price}"

    

    
class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Price in $")

    def __str__(self):
        return f"{self.name} : {self.price}"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Price in $")

    def __str__(self):
        return f"{self.name} : {self.price}"

    
class Dinner(models.Model):
    DINNER_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )

    dinner_size = models.CharField(max_length=1, choices=DINNER_SIZES)

    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Price in $")

    def __str__(self):
        return f"{self.name}, {self.get_dinner_size_display()} : {self.price}"


class Euser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return(f"{self.id}")

    
class Item(models.Model):
    piz = models.ForeignKey(Pizza,on_delete=models.CASCADE, null=True)
    sub = models.ForeignKey(Sub,on_delete=models.CASCADE, null=True)
    past = models.ForeignKey(Pasta,on_delete=models.CASCADE, null=True)
    sal = models.ForeignKey(Salad,on_delete=models.CASCADE, null=True)
    din = models.ForeignKey(Dinner,on_delete=models.CASCADE, null=True)

    
class ShoppingCart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pizzas = models.ManyToManyField(Item, related_name='pizzas')
    subs = models.ManyToManyField(Item, related_name='subs')
    pastas = models.ManyToManyField(Item, related_name='pastas')
    salads = models.ManyToManyField(Item, related_name='salads')
    dinners = models.ManyToManyField(Item, related_name='dinners')
    
    number_of_articles = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return(
            # f'{self.user}\'s cart\n'
            # f'total basket: {self.price}\n'
            # f'tot articles: {self.number_of_articles}\n'
            f'{self.pizzas.in_bulk()}\n'
            f'{self.subs.in_bulk()}\n'
            f'{self.pastas.in_bulk()}\n'
            f'{self.salads.in_bulk()}\n'
            f'{self.dinners.in_bulk()}\n'
        )


class Order(models.Model):

    date_order = models.DateField()
    cart = models.ForeignKey(ShoppingCart,on_delete=models.CASCADE,default=None, null=False)


    
@receiver(post_save, sender=get_user_model())
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(user=instance)

