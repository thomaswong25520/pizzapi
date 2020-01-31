from django.contrib import admin
from django.contrib.admin import ModelAdmin

from import_export.admin import ImportExportModelAdmin

from .models import Topping, Pizza, Sub, Pasta, Salad, Dinner, Extra


class PizzaAdmin(ImportExportModelAdmin):
    def save_related(self, request, form, formsets, change):
        super(PizzaAdmin, self).save_related(request, form, formsets, change)
        form.instance.toppings.add(Topping.objects.get(name='Cheese'))

        
    
@admin.register(Sub)
class SubAdmin(ImportExportModelAdmin):
    pass


class PastaAdmin(ImportExportModelAdmin):
    pass


class SaladAdmin(ImportExportModelAdmin):
    pass


class DinnerAdmin(ImportExportModelAdmin):
    pass


# Register your models here.
admin.site.register(Topping)
admin.site.register(Pizza, PizzaAdmin)
# admin.site.register(Sub)
admin.site.register(Extra)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Salad, SaladAdmin)
admin.site.register(Dinner, DinnerAdmin)

