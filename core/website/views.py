from django.shortcuts import render , redirect
from django.views.generic import TemplateView , CreateView
from django.contrib import messages
from shop.models import RecommendationProductModel , ProductStatus , ProductCategory , Product
from order.models import CouponModel
from datetime import datetime, timedelta
from .forms import ContactForm , NewsLetterForm
from .models import ContactModel
# Create your views here.

class IndexView(TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['recommendations']=RecommendationProductModel.objects.filter(product__status=ProductStatus.publish.value)
        categories=ProductCategory.objects.filter(category_child= None).order_by('-created_date')[:3]
        for category in categories:
            category.new_products = category.category_product.filter(status=ProductStatus.publish.value)[:3]
            category.min_price = category.category_product.filter(status=ProductStatus.publish.value).order_by("price")[:1]
        context["categories"]=categories
        try:
            coupon = CouponModel.objects.last()
            
            context['target_datetime']=coupon.expiration_date.isoformat()
            context['coupon']=coupon
        except:
            pass
        return context
class ContactView(TemplateView):
    template_name = "website/contact.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ContactForm
        return context
class AboutView(TemplateView):
    template_name = "website/about.html"

class ContactSendView(CreateView):
    http_method_names = ['post']
    form_class = ContactForm
    def form_valid(self, form):
        form.is_valid(raise_exception=True)
        form.save()
        messages.success(self.request,'تیکت شما با موفقیت ثبت شد و در اسرع وقت با شما تماس حاصل خواهد شد')
        return super().form_valid(form)
    def form_invalid(self, form):
        for field , errors in form.errors.items():
            for error in errors:
                messages.error(self.request,error)
        messages.error(self.request,'مشکلی در ارسال فرم شما پیش آمد لطفا ورودی ها رو بررسی کنین و مجدد ارسال نمایید')
        return redirect(self.request.META.get('HTTP_REFERER'))
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
class NewsLetterView(CreateView):
    http_method_names = ['post']
    form_class = NewsLetterForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'ایمیل شما با موفقیت ثبت شد و اخبار جدید رو براتون ارسال می کنیم')
        return super().form_valid(form)
    def form_invalid(self, form):
        for field , errors in form.errors.items():
            for error in errors:
                messages.error(self.request,error)
        return redirect('website:index')
    def get_success_url(self):
        return redirect('website:index')