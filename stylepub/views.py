from django.views import View
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from product.models import Product,Color,Size,Category
from django.views.generic import TemplateView
from user.models import Purchase,Wishlist


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Purchase.objects.filter(user=user)
            wishlist = Wishlist.objects.filter(user=user)
            context['cart'] = cart
            context['wishlist'] = wishlist


        color_slug = self.kwargs.get('color_slug')
        size_slug = self.kwargs.get('size_slug')
        category_slug = self.kwargs.get('category_slug')
        sort_option = self.request.GET.get('sort')

        # if color_slug:
        #     color = get_object_or_404(Color, slug=color_slug)
        #     product = Product.objects.filter(color=color)
        if color_slug:
            try:
                color = Color.objects.get(slug=color_slug)
                product = product.filter(color=color)
            except Color.DoesNotExist:
                messages.warning(self.request, 'This color product not found .')

        # if size_slug:
        #     size = get_object_or_404(Size, slug=size_slug)
        #     product = Product.objects.filter(size=size)
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
            except Size.DoesNotExist:
                messages.warning(self.request, 'This category product not found .')

        

        if sort_option == 'price_Ascending':
            product = product.order_by('price')
        elif sort_option == 'price_Descending':
            product = product.order_by('-price')
        
        product = Product.objects.all()
        colors = Color.objects.all()
        sizes = Size.objects.all()
        category = Category.objects.all()

        context['product'] = product
        context['colors'] = colors
        context['sizes'] = sizes
        context['category'] = category
        context['sort_option'] = sort_option
        return context


class BlogView(View):
    def get_context_data(self,**kwargs):
        context = {}
        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Purchase.objects.filter(user=user)
            wishlist = Wishlist.objects.filter(user=user)
            context['cart'] = cart
            context['wishlist'] = wishlist
        return context
    def get(self, request):
        context=self.get_context_data()
        return render(request, 'blog.html',context)


def no_data(request):
    messages.error(request,'Under Contraction')
    return redirect('/')


