from django.contrib import admin
from django.contrib.auth.models import User
from .models import product, sale, inventory

# Register your models here.
admin.site.register(product)
admin.site.register(sale)
admin.site.register(inventory)