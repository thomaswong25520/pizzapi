from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    toppings = models.ManyToManyField(Topping, default='Cheese')
    price = models.IntegerField(help_text="Price in $")

    def __str__(self):
        return f"Size: {self.get_pizza_size_display()}, Type: {self.pizza_type}, Price: {self.price}, Toppings: {self.toppings.in_bulk()}"


class Sub(models.Model):
    SUBS_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )

    subs_size = models.CharField(max_length=1, choices=SUBS_SIZES)
    name = models.CharField(max_length=64)
    price = models.IntegerField(help_text="Price in $")

    def __str__(self):
        return f"{self.name}, {self.get_subs_size_display()} : {self.price}"

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField(help_text="Price in $")

    def __str__(self):
        return f"{self.name} : {self.price}"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField(help_text="Price in $")

    def __str__(self):
        return f"{self.name} : {self.price}"

    
class Dinner(models.Model):
    DINNER_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )

    dinner_size = models.CharField(max_length=1, choices=DINNER_SIZES)

    name = models.CharField(max_length=64)
    price = models.IntegerField(help_text="Price in $")

    def __str__(self):
        return f"{self.name}, {self.get_dinner_size_display()} : {self.price}"

    
class ShoppingCart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza)
    sub = models.ManyToManyField(Sub)
    pasta = models.ManyToManyField(Pasta)
    dinner = models.ManyToManyField(Dinner)
    
    number_of_articles = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    instance.profile.save()
