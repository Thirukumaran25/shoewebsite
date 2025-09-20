from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order
from django.contrib.auth.models import User

class EnquiryForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600",
            "placeholder": "Your full name",
            "autocomplete": "name",
        }),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600",
            "placeholder": "you@example.com",
            "autocomplete": "email",
        }),
    )
    phone = forms.CharField(
        label="Phone",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600",
            "placeholder": "+91 98765 43210",
            "autocomplete": "tel",
        }),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            "class": "block w-full rounded-md border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600 min-h-36",
            "placeholder": "How can we help?",
            "rows": 5,
        }),
    )


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email id", widget=forms.EmailInput(attrs={
        "class": "block w-full border border-slate-400 px-3 py-2 rounded-md",
        "placeholder": "Enter your email",
        "autocomplete": "email",
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class": "block w-full border border-slate-400 px-3 py-2 rounded-md",
        "placeholder": "Enter password",
        "autocomplete": "current-password",
    }))


class RegistrationForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['username', 'password1', 'password2']
            help_texts = {
                'username': None,
                'password1': None,
                'password2': None,
            }
        def _init_(self, *args, **kwargs):
            super()._init_(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({
                    "class": " w-full border border-black px-3 py-2 rounded-md"
                })
        username = forms.EmailField(label="Email id")






class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'card_holder_name', 'card_number', 'cvv', 'expiry_date', 'cash_on_delivery',
            'address_line_1', 'city', 'state', 'landmark', 'pincode',
        ]
        widgets = {
            'cash_on_delivery': forms.CheckboxInput(attrs={'id': 'id_cash_on_delivery'}),
            'card_holder_name': forms.TextInput(attrs={'maxlength': 50, 'id': 'id_card_holder_name'}),
            'card_number': forms.TextInput(attrs={'maxlength': 20, 'id': 'id_card_number'}),
            'cvv': forms.PasswordInput(attrs={'maxlength': 4, 'id': 'id_cvv'}),
            'expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY', 'id': 'id_expiry_date'}),
        }

