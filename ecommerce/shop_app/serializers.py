from rest_framework import serializers

from . import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.product
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    total_amount = serializers.FloatField(read_only=True)
    class Meta:
        model = models.sale
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    inventory = ProductSerializer(source='product_id', read_only=True)
    low_stock_threshold = serializers.SerializerMethodField()
    class Meta:
        model = models.inventory
        # fields = '__all__'
        exclude = ('id', 'product_id',)

    def get_low_stock_threshold(self, obj):
        pdt = obj.product_id
        thd = self.context.get('low_stock_threshold', 10)
        
        # Check if the quantity is less than 9, and return True if so, else False
        return pdt.quantity < thd if pdt and pdt.quantity is not None else False
    

class InventoryUpdateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = models.product
        fields = ['product_id', 'quantity']
