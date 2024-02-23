from django.urls import path
from .views import register,activate,UserLogin,UserLogout,PurchaseView,WishlistView,CartView,ShowWishlistView,deleteCartProduct,deleteWishProduct,ProfileView



urlpatterns = [
    path('register/',register,name='register'),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogout,name='logout'),
    path('product/purchase/<int:id>/',PurchaseView.as_view(),name='purchase_product'),
    path('product/wishlist/<int:id>',WishlistView.as_view(),name='wishlist_product'),
    path('cart/',CartView.as_view(),name='cart' ),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('wishlist/',ShowWishlistView.as_view(),name='wishlist' ),
    path('cart/delete/product/<int:id>',deleteCartProduct,name="delete_cart_product"),
    path('wishlist/delete/product/<int:id>',deleteWishProduct,name="delete_wish_product"),
]
