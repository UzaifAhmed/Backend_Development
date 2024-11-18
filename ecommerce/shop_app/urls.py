from django.urls import path,  include
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('products/register', views.ProductView.as_view(), name='product-view'),
    path('inventory', views.InventoryView.as_view(), name='inventory-view'),
    path('inventory/update', views.InventoryUpdate.as_view(), name='inventory-update'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('sales/create', views.SalesCreate.as_view(), name='sales-create'),
    path('sales', views.SalesView.as_view(), name='sales-view'),
    path('sales/revenue', views.RevenueView.as_view(), name='revenue-view'),
    path('sales/daily', views.DailySales.as_view(), name='daily-sale'),
    path('sales/weekly', views.WeeklySales.as_view(), name='weekly-sale'),
    path('sales/monthly', views.MonthlySales.as_view(), name='monthly-sale'),
    path('sales/annual', views.AnnualSales.as_view(), name='annual-sale'),
    path('sales/bydate', views.ByDateSales.as_view(), name='bydate-sale'),
    path('sales/byproduct', views.ByProduct.as_view(), name='byproduct-sale'),
    path('sales/bycategory', views.ByCategory.as_view(), name='bycategory-sale'),
    path('sales/compare', views.SalesByCompare.as_view(), name='bycompare-sale'),
    path('sales/filter', views.SalesFilter.as_view(), name='sales-filter'),
    path('sales/analysis', views.SalesAnalysis.as_view(), name='sales-analysis')
]