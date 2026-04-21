from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator , MaxValueValidator
from django.core.cache import cache
# Create your models here.
class ProductStatus(models.IntegerChoices):
    publish = 1 , ('نمایش')
    draft = 2 , ('عدم نمایش')
class ProductCategory(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(allow_unicode=True)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='category_child')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class ProductImage(models.Model):
    file = models.ImageField(default='/default/img1.png',upload_to='product/img/')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
class Product(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.PROTECT)
    category= models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,null=True ,related_name='category_product')
    title=models.CharField(max_length=255)
    slug=models.SlugField(allow_unicode=True , unique=True)
    image = models.ManyToManyField(ProductImage)
    description = models.TextField()
    brief_description=models.TextField(null=True,blank=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=ProductStatus.choices,default=ProductStatus.draft.value)
    price = models.DecimalField(default=0,max_digits=11,decimal_places=0)
    discount_percent=models.IntegerField(default=0 , validators= [MinValueValidator(0),MaxValueValidator(100)])
    avg_rate = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title

    def get_first_image(self):
        first_image =self.image.first()
        return first_image.file.url
    def has_image(self):
        return self.image.first() != None  
    def get_price(self):
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        discount_amount = self.price - discount_amount
        return round(discount_amount)
    def show_price(self):
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        discount_amount = self.price - discount_amount
        return '{:,}'.format(round(discount_amount))
    def is_discounted(self):
        return self.discount_percent != 0
    def is_published(self):
        return self.status == ProductStatus.publish.value

class AttributeGroup(models.Model):
    category = models.ForeignKey(ProductCategory , on_delete=models.CASCADE,related_name='attribute_group_category')
    title=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.category} - {self.title}"
    
class Attribute(models.Model):
    group = models.ForeignKey(AttributeGroup , on_delete=models.CASCADE,related_name='attributes_group')
    title=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.group} - {self.title}"

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE,related_name='product_attribute')
    attribute=models.ForeignKey(Attribute , on_delete=models.CASCADE,related_name='attribute_attributes')
    value=models.CharField(max_length=255)
    def __str__(self):
        return f"{self.product} - {self.attribute}: {self.value}"
    class Meta:
        unique_together = ('attribute', 'product')

class WishlistProductModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title
    
class RecommendationProductModel(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)