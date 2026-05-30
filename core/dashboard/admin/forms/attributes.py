from django import forms
from shop.models import ProductAttribute, Attribute, AttributeGroup


class AdminProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = [
            "attribute",
            "value",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["value"].widget.attrs["class"] = "form-control"


class AdminAttributeMiddleForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ["title", "group"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"


class AdminAttributeGroupForm(forms.ModelForm):
    class Meta:
        model = AttributeGroup
        fields = [
            "title",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
