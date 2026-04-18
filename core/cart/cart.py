from shop.models import Product , ProductStatus
from cart.models import CartModel , CartItemModel
class CartSession:
    def __init__(self,session):
        self.session= session
        self._cart = self.session.setdefault("cart",{
            "items":[],
        })
    
    def update_product_quantity(self , product_id,quantity):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        self.save()
    def remove_product(self , product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        self.save()

    def add_product(self , product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if  Product.objects.get(id=product_id).stock <= item["quantity"]:
                    break
                else:
                    item["quantity"] +=1
                    break
        else:
            new_item = {
                "product_id":product_id ,
                "quantity" : 1 ,
            }
            self._cart["items"].append(new_item)
        self.save()
    def reduce_product(self , product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if item["quantity"] ==1:
                    break
                else:
                    item["quantity"] -=1
                    break
        self.save()
  
    
    def clear(self):
        self._cart = self.session["cart"] = {
            "items":[],
        }
        self.save()
    
    def get_cart_dict(self):
        return self._cart["items"]

    def get_cart_items(self):
        for item in self._cart["items"]:
            product_obj= Product.objects.get(id=item["product_id"], status=ProductStatus.publish.value)
            item.update({"product_obj" :product_obj,"total_price":item["quantity"] * product_obj.get_price()})
        return self._cart["items"]

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])
    
    def sync_cart_items_db(self , user):
        cart,created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)

        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {"product_id":str(cart_item.product.id),"quantity":cart_item.quantity}
                self._cart["items"].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()
    def merge_session_cart_in_db(self , user):
        cart,created = CartModel.objects.get_or_create(user=user)
        for item in self._cart["items"]:
            product_obj= Product.objects.get(id=item["product_id"], status=ProductStatus.publish.value)

            cart_item , created = CartItemModel.objects.get_or_create(cart=cart,product=product_obj)
            cart_item.quantity = item["quantity"]
            cart_item.save()
        session_product_ids = [item["product_id"] for item in self._cart["items"] ]
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()

    def save(self):
        self.session.modified = True