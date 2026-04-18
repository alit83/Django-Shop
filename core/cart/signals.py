from django.contrib.auth.signals import user_logged_in , user_logged_out 
from django.dispatch import receiver
from django.contrib.sessions.backends.db import SessionStore
from django.db.models.signals import pre_save
from .cart import CartSession
from .models import CartItemModel , CartModel
from django.contrib.sessions.models import Session
from shop.models import Product , ProductStatus

@receiver(user_logged_in)
def post_login(sender,user,request,**kwargs):
    cart = CartSession(request.session)
    cart.sync_cart_items_db(user)

@receiver(user_logged_out)
def pre_logout(sender,user,request,**kwargs):
    cart = CartSession(request.session)
    cart.merge_session_cart_in_db(user)



@receiver(pre_save, sender=Product)
def status_changed(sender, instance, **kwargs):
    if not instance.pk:
        return   # new object; nothing changed yet

    old_value = sender.objects.get(pk=instance.pk).status
    new_value = instance.status

    if old_value == new_value or new_value == ProductStatus.publish.value :
        return

    #user = instance.user

    CartItemModel.objects.filter(product=instance).delete()

    # 2.remove session data
    sessions= Session.objects.all()
    for session in sessions:
        data = session.get_decoded()
        cart = data.get('cart',{})
        items=cart['items']
        for item in items:
            if int(item['product_id']) ==instance.pk:
                cart['items'].remove(item)
                data["cart"] = cart

            # Re-encode session properly
            store = SessionStore(session_key=session.session_key)
            store.update(data)
            store.save()
    return