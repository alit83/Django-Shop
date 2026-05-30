from django import forms
from .models import ContactModel, NewsLetterModel
from captcha.fields import CaptchaField


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:

        model = ContactModel
        fields = ["subject", "full_name", "email", "phone_number", "content"]

        error_messages = {
            "email": {"required": "فیلد ایمیل نمی تواند خالی باشد"},
            "content": {
                "required": "فیلد محتوا نمی تواند خالی باشد",
                "min_length": "طول محتوای وارد شده غیر مجاز است",
            },
            "subject": {"required": "فیلد  عنوان نمی تواند خالی باشد"},
            "full_name": {
                "required": "فیلد نام و نام خانوادگی نمی تواند خالی باشد"
            },
        }


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetterModel
        fields = [
            "email",
        ]
        error_messages = {
            "email": {"unique": "این ایمیل قبلا ثبت نام شده است"},
        }
