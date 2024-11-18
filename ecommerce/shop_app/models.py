from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, blank=False, default='Untitled')
    category = models.CharField(max_length=255, blank=False, default='Untitled')
    price = models.FloatField(default=0.00)
    quantity = models.IntegerField(default=10)

class sale(models.Model):
    product_id = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    quantity_sold = models.IntegerField()
    total_amount = models.FloatField()
    sale_date = models.DateField(auto_now_add=True)


class inventory(models.Model):
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)

# create inventory when product is created !!
@receiver(post_save, sender=product)
def create_update_inventory(sender, instance, created, **kwargs):
    if created:
        inventory.objects.create(product_id=instance)
    else:
        inventory.objects.update_or_create(product_id=instance)