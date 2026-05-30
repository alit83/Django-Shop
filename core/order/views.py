from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from order.permissions import HasCustomerAccessPermission
from order.models import (
    UserAddressModel,
    OrderModel,
    OrderItemModel,
    CouponModel,
)
from cart.models import CartModel
from cart.cart import CartSession
from .forms import CheckOutForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.http.response import JsonResponse
from payment.zarinpal_client import ZarinPalSandbox
from payment.models import PaymentModel
from django.shortcuts import redirect


class OrderCheckOutView(
    HasCustomerAccessPermission, LoginRequiredMixin, FormView
):
    template_name = "order/checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy("order:completed")

    def get(self, request, *args, **kwargs):
        cart = CartModel.objects.get(user=request.user)
        if not self.valid_quantity_of_itmes(cart):
            messages.error(
                self.request, "تعداد محصول بیشتر از تعداد موجود است"
            )
            return redirect(reverse_lazy("cart:session-cart-summary"))
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(OrderCheckOutView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user_obj = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data["address_id"]
        coupon_obj = cleaned_data["coupon"]
        cart = CartModel.objects.get(user=user_obj)
        order_obj = self.create_order(address)
        self.create_order_items(order_obj, cart)
        self.clear_cart(cart)
        total_price = order_obj.calculate_total_price()
        self.apply_coupon(coupon_obj, order_obj, total_price)
        order_obj.save()
        return redirect(self.create_payment_url(order_obj))

    def create_order(self, address):
        return OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )

    def create_payment_url(self, order_obj):
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_request(order_obj.get_price())
        authority = response["data"]["authority"]
        payment_obj = PaymentModel.objects.create(
            authority_id=authority, amount=order_obj.get_price()
        )
        order_obj.payment = payment_obj
        order_obj.save()
        return zarinpal.generate_payment_url(authority)

    def create_order_items(self, order_obj, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order_obj,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

    def valid_quantity_of_itmes(self, cart):
        for item in cart.cart_items.all():
            product_obj = item.product
            if product_obj.stock < item.quantity:
                return False

        return True

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon_obj, order_obj, total_price):
        if coupon_obj:
            order_obj.coupon = coupon_obj
            coupon_obj.save()
        order_obj.total_price = total_price

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["addresses"] = UserAddressModel.objects.filter(
            user=self.request.user
        )
        cart = CartModel.objects.get(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round((total_price) / 100)
        return context


class OrderCompletedView(
    LoginRequiredMixin, HasCustomerAccessPermission, TemplateView
):
    template_name = "order/completed.html"


class ValidateCouponView(
    LoginRequiredMixin, HasCustomerAccessPermission, View
):
    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        user = self.request.user
        status_code = 200
        message = "کد تخفیف با موفقیت ثبت شد"
        total_price = 0
        total_tax = 0

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"message": "کد تخفیف یافت نشد"}, status=404)
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, "محدودیت در تعداد استفاده"

            elif (
                coupon.expiration_date
                and coupon.expiration_date < timezone.now()
            ):
                status_code, message = 403, "کد تخفیف منقضی شده است"

            elif user in coupon.used_by.all():
                status_code, message = (
                    403,
                    "این کد تخفیف قبلا توسط شما استفاده شده است",
                )

            else:
                cart = CartModel.objects.get(user=self.request.user)

                total_price = cart.calculate_total_price()
                total_price = round(
                    total_price
                    - (total_price * (coupon.discount_percent / 100))
                )
                total_tax = round((total_price * 9) / 100)
        return JsonResponse(
            {
                "message": message,
                "total_tax": total_tax,
                "total_price": total_price,
            },
            status=status_code,
        )


class OrderFailedView(
    LoginRequiredMixin, HasCustomerAccessPermission, TemplateView
):
    template_name = "order/failed.html"
