from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.urls import reverse_lazy
from payment.models import PaymentModel, PaymentStatusType
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel, OrderStatusType

# Create your views here.


class PaymentVerifyView(View):
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        payment_obj = get_object_or_404(
            PaymentModel, authority_id=authority_id
        )
        order_obj = OrderModel.objects.get(payment=payment_obj)
        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_verify(
            int(payment_obj.amount), payment_obj.authority_id
        )
        try:
            code = response["data"]["code"]
            ref_id = response["data"]["ref_id"]
        except (KeyError, TypeError):
            code = response["errors"]["code"]
            ref_id = None
        payment_obj.ref_id = ref_id
        payment_obj.response_code = code
        payment_obj.status = (
            PaymentStatusType.success.value
            if code in {100, 101}
            else PaymentStatusType.failed.value
        )

        payment_obj.response_json = response["data"]
        payment_obj.save()

        order_obj.status = (
            OrderStatusType.success.value
            if code in {100, 101}
            else OrderStatusType.failed.value
        )
        order_obj.save()
        coupon_obj = order_obj.coupon
        if coupon_obj:
            if code in {100, 101}:
                coupon_obj.used_by.add(request.user)
                coupon_obj.save()
            else:
                order_obj.coupon = None
                order_obj.save()

        return redirect(
            reverse_lazy("order:completed")
            if code in {100, 101}
            else reverse_lazy("order:failed")
        )
