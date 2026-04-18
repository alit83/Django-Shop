from django import forms
from django.utils.translation import gettext_lazy as _
from shop.models import Product , ProductImage , ProductCategory 



class AdminProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.filter().exclude(parent__parent=None), required=True)
    class Meta:
        model = Product
        fields = [
            "category",
            "title",
            "slug",
            "description",
            "brief_description",
            "stock",
            "status",
            "price",
            "discount_percent",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['brief_description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['id'] = 'ckeditor'
        self.fields['stock'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['type'] = 'number'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['discount_percent'].widget.attrs['class'] = 'form-control'
        
        

class  AdminCreateImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['file',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['accept'] = 'image/png, image/jpg, image/jpeg'

class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = [
            "title",
            "slug",
            "parent",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['parent'].widget.attrs['class'] = 'form-control'