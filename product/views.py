from django.shortcuts import render,redirect
from django.views.generic import DetailView
from .forms import ReviewForm
from .models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from product.models import Product,Color,Size,Category
from django.views.generic import TemplateView
from user.models import Purchase,Wishlist
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect

# Create your views here.
class ProductDetails(DetailView):
    model=Product
    pk_url_kwarg='id'
    template_name='product/details.html'


    def get(self, request, *args, **kwargs):
        if kwargs.get('id') is  None:
            messages.error(request,'product not found')
            return HttpResponseRedirect(reverse_lazy('all_product'))
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        product = self.get_object()
        review_form = ReviewForm(request.POST)
        if request.user.is_authenticated:
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.save()
                messages.success(request, 'Your review has been added successfully!')
                return self.get(request, *args, **kwargs)
        else:
            messages.error(request, 'You must be logged in to review this product.')
            return redirect(request.path)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        reviews = post.comments.all()
        review_form=ReviewForm()
        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Purchase.objects.filter(user=user)
            wishlist = Wishlist.objects.filter(user=user)
            context['cart'] = cart
            context['wishlist'] = wishlist
            
        context['reviews']= reviews
        context['review_form']= review_form
        return context
    

class All_product(TemplateView):
    template_name = 'product/all_product.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Purchase.objects.filter(user=user)
            wishlist = Wishlist.objects.filter(user=user)
            context['cart'] = cart
            context['wishlist'] = wishlist


        product = Product.objects.all()
        color_slug = self.kwargs.get('color_slug')
        size_slug = self.kwargs.get('size_slug')
        category_slug = self.kwargs.get('category_slug')
        sort_option = self.request.GET.get('sort')


        if color_slug:
            try:
                color = Color.objects.get(slug=color_slug)
                product = product.filter(color=color)
            except Color.DoesNotExist:
                messages.warning(self.request, 'This color product not found .')


        if size_slug:
            try:
                size = Size.objects.get(slug=size_slug)
                product = product.filter(size=size)
            except Size.DoesNotExist:
                messages.warning(self.request, 'This size product not found .')


        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                product = product.filter(category=category)
            except Category.DoesNotExist:
                messages.warning(self.request, 'This category product not found .')

        

        if sort_option == 'price_Ascending':
            product = product.order_by('price')
        elif sort_option == 'price_Descending':
            product = product.order_by('-price')
        
        colors = Color.objects.all()
        sizes = Size.objects.all()
        category = Category.objects.all()

        context['product'] = product
        context['colors'] = colors
        context['sizes'] = sizes
        context['category'] = category
        context['sort_option'] = sort_option
        return context