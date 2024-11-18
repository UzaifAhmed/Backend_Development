from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.utils import timezone
import datetime

from .models import product, sale, inventory
from .serializers import (ProductSerializer, InventorySerializer,
                          InventoryUpdateSerializer, SalesSerializer)

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

class ProductView(generics.ListCreateAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

class InventoryView(views.APIView):
    def get(self, request):
        try:
            # Get the low stock threshold from query parameters or use 10 as the default
            low_stock_thresh = int(request.GET.get('low_stock_threshold', 10))
        except ValueError:
            return Response(
                {"error": "Invalid low_stock_threshold. It must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch all inventory objects and related products
        queryset = inventory.objects.select_related('product_id').all()

        inventory_with_alerts = []
        for item in queryset:
            product = item.product_id  # Access the related product
            low_stock_alert = product.quantity < low_stock_thresh

            # Create a dictionary with product data and the low stock alert
            product_with_alert = {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "category": product.category,
                "price": product.price,
                "quantity": product.quantity,
                "low_stock_alerts": low_stock_alert,
            }
            inventory_with_alerts.append(product_with_alert)

        # Return the response
        return Response(
            {"inventory": inventory_with_alerts}, status=status.HTTP_200_OK)

    

class InventoryUpdate(generics.UpdateAPIView):
    queryset = product.objects.all()
    serializer_class = InventoryUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            raise ValidationError({"product_id": "This field is required."})
        
        try:
            product_instance = product.objects.get(product_id=product_id)
        except product.DoesNotExist:
            raise ValidationError({"error": "Product not found."})
        
        serializer =self.get_serializer(product_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"message": "Quantity updated"}, status=status.HTTP_200_OK)
    

class SalesView(generics.ListAPIView):
    queryset = sale.objects.all()
    serializer_class =  SalesSerializer
    permission_classes = [IsAuthenticated]


class DailySales(generics.ListAPIView):
    queryset = sale.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        return sale.objects.filter(sale_date=today)
    

class WeeklySales(generics.ListAPIView):
    queryset = sale.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()

        start_date = today - timezone.timedelta(days=today.weekday())
        end_date = start_date + timezone.timedelta(days=6)
        return sale.objects.filter(sale_date__range=[start_date, end_date])
    

class MonthlySales(generics.ListAPIView):
    queryset = sale.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        return sale.objects.filter(sale_date__year=today.year, sale_date__month=today.month)
    

class AnnualSales(generics.ListAPIView):
    queryset = sale.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        return sale.objects.filter(sale_date__year=today.year)


class ByDateSales(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        # Dates string to datetime.time format
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        except (ValueError, TypeError):
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Validate dates
        if not start_date or not end_date:
            return Response({"error": "Both start_date and end_date are required."})
        
        sales = sale.objects.filter(sale_date__range=[start_date, end_date])
        serializer = SalesSerializer(sales, many=True)
        
        return Response(serializer.data)


class ByProduct(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        product_id = request.GET.get("product_id")

        if not product_id:
            return Response({"error": "Product id not provided!"})

        sales = sale.objects.filter(product_id=product_id)
        serializer = SalesSerializer(sales, many=True)
        return Response(serializer.data)
    

class ByCategory(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category = request.GET.get("category")

        if not category:
            return Response({"error": "Category not provided!"})
        
        sales = sale.objects.filter(product_id__category=category)
        serializer = SalesSerializer(sales, many=True)
        return Response(serializer.data)
    

class SalesByCompare(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date_1 = request.query_params.get('start_date_1')
        end_date_1 = request.query_params.get('end_date_1')
        start_date_2 = request.query_params.get('start_date_2')
        end_date_2 = request.query_params.get('end_date_2')

        # Dates string to datetime.time format
        try:
            start_date_1 = datetime.datetime.strptime(start_date_1, '%Y-%m-%d').date()
            end_date_1 = datetime.datetime.strptime(end_date_1, '%Y-%m-%d').date()
            start_date_2 = datetime.datetime.strptime(start_date_2, '%Y-%m-%d').date()
            end_date_2 = datetime.datetime.strptime(end_date_2, '%Y-%m-%d').date()
        except:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
        
        if not all([start_date_1, end_date_1, start_date_2, end_date_2]):
            return Response({"error": "Both start_date and end_date are required for phase 1 & 2."})
        
        revenue1 = sale.objects.filter(sale_date__range=[start_date_1, end_date_1]).aggregate(
            total_revenue=Coalesce(Sum(F('total_amount'), output_field=FloatField()), 0.0)
                        )['total_revenue']
        
        revenue2 = sale.objects.filter(sale_date__range=[start_date_2, end_date_2]).aggregate(
            total_revenue=Coalesce(Sum(F('total_amount'), output_field=FloatField()), 0.0)
                        )['total_revenue']
        
        return Response({"revenue1": revenue1, "revenue2": revenue2})
    

class SalesFilter(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)
        product_id = request.GET.get("product_id", None)
        category = request.GET.get("category", None)
        quantity_sold_min = request.GET.get("quantity_sold_min", None)
        quantity_sold_max = request.GET.get("quantity_sold_max", None)
        total_amount_min = request.GET.get("total_amount_min", None)
        total_amount_max = request.GET.get("total_amount_max", None)

        sales = sale.objects.all()

        if all([start_date, end_date]):
            # Dates string to datetime.time format
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            except:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
            
            sales = sale.objects.filter(sale_date__range=[start_date, end_date])

        if product_id:
            sales = sale.objects.filter(product_id=product_id)

        if category:
            sales = sale.objects.filter(product_id__category=category)

        if all([quantity_sold_min, quantity_sold_max]):
            sales = sale.objects.filter(quantity_sold__range=[quantity_sold_min, quantity_sold_max])

        if all([total_amount_min, total_amount_max]):
            sales = sale.objects.filter(total_amount__range=[total_amount_min, total_amount_max])
            
        serializer = SalesSerializer(sales, many=True)

        return Response(serializer.data)

    
class SalesAnalysis(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)
        product_id = request.GET.get("product_id", None)
        category = request.GET.get("category", None)
        quantity_sold_min = request.GET.get("quantity_sold_min", None)
        quantity_sold_max = request.GET.get("quantity_sold_max", None)
        total_amount_min = request.GET.get("total_amount_min", None)
        total_amount_max = request.GET.get("total_amount_max", None)

        sales = sale.objects.all()

        if all([start_date, end_date]):
            # Dates string to datetime.time format
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            except:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
            
            sales = sale.objects.filter(sale_date__range=[start_date, end_date])

        if product_id:
            sales = sale.objects.filter(product_id=product_id)

        if category:
            sales = sale.objects.filter(product_id__category=category)

        if all([quantity_sold_min, quantity_sold_max]):
            sales = sale.objects.filter(quantity_sold__range=[quantity_sold_min, quantity_sold_max])

        if all([total_amount_min, total_amount_max]):
            sales = sale.objects.filter(total_amount__range=[total_amount_min, total_amount_max])

        quantity_sold = sales.aggregate(
            total_quantity_sold=Coalesce(Sum('quantity_sold'),0))['total_quantity_sold']
    
        revenue = sales.aggregate(
            total_revenue=Coalesce(Sum(F('total_amount'), output_field=FloatField()), 0.0))['total_revenue']
        
        return Response({'total_quantity_sold': quantity_sold, 'total_revenue': revenue}, status=status.HTTP_200_OK)


class SalesCreate(generics.CreateAPIView):
    queryset = sale.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_instance = serializer.validated_data['product_id']
        quantity_sold = serializer.validated_data['quantity_sold']

        # Check stock in product
        if product_instance.quantity < quantity_sold:
            raise ValidationError("Not enough stock to complete this sale")
        
        # Calculate total amount
        total_amount = product_instance.price * quantity_sold

        # Update quantity in product
        product_instance.quantity -= quantity_sold
        product_instance.save()

        serializer.save(total_amount=total_amount)

        return serializer.data
    

class RevenueView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        # Dates string to datetime.time format
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        except (ValueError, TypeError):
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Validate dates
        if not start_date or not end_date:
            return Response({"error": "Both start_date and end_date are required."})
        
        revenue = sale.objects.filter(sale_date__range=[start_date, end_date]).aggregate(
            total_revenue=Coalesce(Sum(F('total_amount'), output_field=FloatField()), 0.0)
                        )['total_revenue']

        return Response({"revenue": revenue}, status=status.HTTP_200_OK)