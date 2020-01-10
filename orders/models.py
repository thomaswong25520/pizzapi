from django.db import models

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


