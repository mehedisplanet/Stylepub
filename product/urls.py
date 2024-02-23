from django.urls import path
from .views import ProductDetails,All_product
from stylepub.views import HomeView


urlpatterns = [
    path('all_product',All_product.as_view(),name='all_product'),
    path('details/<int:id>',ProductDetails.as_view(),name='details'),
    path('color/<slug:color_slug>', All_product.as_view(), name='color_wise_post'),
    path('size/<slug:size_slug>', All_product.as_view(), name='size_wise_post'),
    path('category/<slug:category_slug>', All_product.as_view(), name='category_wise_post'),
]