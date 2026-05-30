from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django import forms

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["email"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_validation.validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password")

        pass2 = cleaned_data.get("password1")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError(
                "دو پسورد وارد شده باهمدیگر مطابقت ندارند"
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
            return user
        else:
            return user


class EmailForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_validation.validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password")

        pass2 = cleaned_data.get("password1")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError(
                "دو پسورد وارد شده باهمدیگر مطابقت ندارند"
            )
        return cleaned_data
