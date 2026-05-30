from django import forms
from .models import ReviewModel
from shop.models import Product, ProductStatus


class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ["product", "rate", "description"]
        error_messages = {
            "description": {
                "required": "فیلد توضیحات اجباری است",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")

        try:
            Product.objects.get(
                id=product.id, status=ProductStatus.publish.value
            )
        except Product.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد")
        return cleaned_data
