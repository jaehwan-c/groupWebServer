from django import forms
from django.forms import ModelForm
from .models import *

class ItemInfoForm(forms.ModelForm): 
    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap.html"
        fields = ['itemName', 'id', 'description', 'categoryName', 'qr_code', 'unit']
        widgets = {
            'itemName': forms.TextInput(attrs={"class": 'form-control'}),
            'categoryName': forms.CheckboxSelectMultiple(attrs={'categoryName': 'categoryName'})
        }

class ItemInstanceForm(forms.ModelForm):
    class Meta:
        model = ItemInstance
        template_name = "django_tables2/bootstrap.html"
        fields = ['instanceName', 'instanceId', 'status', 'production_date', 'expiry_date', 'quantity']

class AddStockForm(forms.ModelForm):
    class Meta:
        model = ItemInstance
        template_name = "django_tables2/bootstrap.html"
        fields=['instanceName', 'quantity']

class DataAnalyticsForm(forms.ModelForm):
    class Meta:
        model = ItemInstance
        template_name = "django_tables2/bootstrap.html"
        fields=['instanceName', 'entry_date']