from django import forms
from shop.models import RecommendationProductModel, Product, ProductStatus


class AdminRecommendationForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(status=ProductStatus.publish.value),
        required=True,
    )

    class Meta:
        model = RecommendationProductModel
        fields = [
            "product",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs["class"] = "form-control"
