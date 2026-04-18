from django import forms
from django.utils.translation import gettext_lazy as _
from shop.models import ProductCategory



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