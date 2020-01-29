from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Topping, Pizza, Sub, Pasta, Salad, Dinner


class PizzaAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        super(PizzaAdmin, self).save_related(request, form, formsets, change)
        form.instance.toppings.add(Topping.objects.get(name='Cheese'))
        

# Register your models here.
admin.site.register(Topping)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner)

