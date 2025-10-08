from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

def validate_cyrillic(value):
    # Проверяем, что строка состоит только из кириллических букв, пробелов и тире
    if not re.match(r'^[А-ЯЁа-яё\s\-]+$', value):
        raise ValidationError('Разрешены только кириллица, пробел и тире')

def validate_login(value):
    # Проверяем, что строка состоит только из латинских букв, цифр и тире
    if not re.match(r'^[A-Za-z0-9\-]+$', value):
        raise ValidationError('Разрешены только латиница, цифры и тире')

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, validators=[validate_cyrillic], error_messages={'required': 'Это поле обязательно для заполнения.'})
    surname = forms.CharField(max_length=100, required=True, validators=[validate_cyrillic], error_messages={'required': 'Это поле обязательно для заполнения.'})
    patronymic = forms.CharField(max_length=100, required=False, validators=[validate_cyrillic])
    login = forms.CharField(max_length=100, required=True, validators=[validate_login], error_messages={'required': 'Это поле обязательно для заполнения.'})
    email = forms.EmailField(required=True, error_messages={'required': 'Это поле обязательно для заполнения.'})
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, required=True, error_messages={'required': 'Это поле обязательно для заполнения.'})
    password_repeat = forms.CharField(widget=forms.PasswordInput, min_length=6, required=True, error_messages={'required': 'Это поле обязательно для заполнения.'})
    rules = forms.BooleanField(required=True, error_messages={'required': 'Вы должны согласиться с правилами регистрации.'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password and password_repeat and password != password_repeat:
            raise ValidationError("Пароли не совпадают")

        return cleaned_data
