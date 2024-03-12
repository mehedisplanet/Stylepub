from .models import PurchaseHistory
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import ContactUsForm
from django.views.generic import ListView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Purchase,Wishlist
from product.models import Product
from django.http import HttpResponseRedirect






def register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            mail_subject='Activation link has been sent to your email Id'
            message=render_to_string('user/activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=form.cleaned_data.get('email')
            email=EmailMessage(
                mail_subject,message,
                to=[to_email]
            )
            email.send()
            messages.success(request,'Check email and active your account .')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'user/register.html',{'form':form})



def activate(request, uidb64, token):  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and default_token_generator.check_token(user, token):  
        user.is_active = True  
        user.save()
        messages.success(request,'Your account active successfully .')
        return redirect('login')
    else:
        return redirect('register')



class UserLogin(LoginView):
    template_name = 'user/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Login successfully")
        return reverse_lazy('home')



def UserLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful")
    else:
        messages.info(request, "You are not logged in.")
    return redirect('home')

class CartView(LoginRequiredMixin, ListView):
    template_name = 'user/cart.html'
    login_url = reverse_lazy('login')

    def get_context_data(self,**kwargs):
        context = {}
        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Purchase.objects.filter(user=user)
            wishlist = Wishlist.objects.filter(user=user)
            context['cart'] = cart
            context['wishlist'] = wishlist
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access your cart.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context=self.get_context_data()
        user_purchases = Purchase.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'data': user_purchases,**context
        })


class ShowWishlistView(LoginRequiredMixin, ListView):
    template_name = 'user/wishlist.html'
    login_url = reverse_lazy('login')

    def get_context_data(self,**kwargs):
        context = {}
        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Purchase.objects.filter(user=user)
            wishlist = Wishlist.objects.filter(user=user)
            context['cart'] = cart
            context['wishlist'] = wishlist
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access your wishlist.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context=self.get_context_data()
        user_wishlist = Wishlist.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'data': user_wishlist,**context
        })


class PurchaseView(LoginRequiredMixin,View):
    login_url=reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to buy product.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('/')
        Purchase.objects.create(user=request.user, product=product)
        request.user.save()
        messages.success(request, "Product purchase successful.")
        return redirect('/')




@login_required
def Checkout(request):
    purchases = Purchase.objects.filter(user=request.user)
    purchased_items_details = []
    for purchase in purchases:
        product_details = f"{purchase.product.title} - ${purchase.product.price}"
        purchased_items_details.append(product_details)
        PurchaseHistory.objects.create(user=request.user, product=purchase.product)
        request.user.save()
    
    if purchased_items_details:
        # Send email
        subject = 'Purchase Confirmation'
        message = f'Thank you for your purchase! You have bought: {", ".join(purchased_items_details)}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [request.user.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Delete purchases
        purchases.delete()
        messages.success(request, "Product checkout successful. Purchase confirmation email sent.")
    else:
        messages.info(request, "Your cart is empty. Please purchase first.")
    return redirect('/')



class WishlistView(LoginRequiredMixin,View):
    login_url=reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to add product.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id):
        try:
           product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('/')
        Wishlist.objects.create(user=request.user, product=product)
        request.user.save()
        messages.success(request, "Product add successful.")
        return redirect('/')



class ContactUs(View):
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
        form = ContactUsForm()
        return render(request, 'contact.html',{'form': form,**context})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'We will contact you as soon as possible .')
            return redirect('contact')
        return render(request, 'contact.html', {'form': form})


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'user/profile.html')
    else:
        messages.warning(request,'Please Login First')
        return redirect('login')
    

class ProfileView(View):
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
        if self.request.user.is_authenticated:
            context=self.get_context_data()
            return render(request, 'user/profile.html',context)
        else:
            messages.warning(request,'Please Login First')
        return redirect('login')



def deleteCartProduct(request,id):
    if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to delete to your cart product.")
            return redirect('login')
    
    else:
        try:
            root = Purchase.objects.get(pk=id)
            root.delete()
            messages.success(request, "Cart product deleted successfully.")
        except Purchase.DoesNotExist:
            messages.error(request, "Cart delete product not found.")
        return redirect('cart')



def deleteWishProduct(request,id):
    if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to delete to your wishlist product.")
            return redirect('login')
    else:
        try:
            root = Wishlist.objects.get(pk=id)
            root.delete()
            messages.success(request, "Wishlist product deleted successfully.")
        except Wishlist.DoesNotExist:
            messages.error(request, "Wishlist delete product not found.")
        return redirect('wishlist')
    



class PurchaseHistoryView(LoginRequiredMixin, ListView):
    template_name = 'user/purchase_history.html'
    login_url = reverse_lazy('login')

    def get_context_data(self,**kwargs):
        context = {}
        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Purchase.objects.filter(user=user)
            history = PurchaseHistory.objects.filter(user=user)
            context['cart'] = cart
            context['history'] = history
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access your history.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context=self.get_context_data()
        history = PurchaseHistory.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'data': history,**context
        })
