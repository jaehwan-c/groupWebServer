from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid
from django.contrib.auth.models import User
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from datetime import datetime

class Category(models.Model):
    categoryName = models.CharField(max_length=300, help_text="Type in the Category of the Item")
    def __str__(self):
        return self.categoryName

class Status(models.Model):
    """Only for the admin to change!!"""
    status = models.CharField(max_length=300)

    def __str__(self):
        return self.status

class Unit(models.Model):
    unit = models.CharField(max_length=20, help_text="Unit of the Item")

    def __str__(self):
        return self.unit

class Item(models.Model):
    itemName = models.CharField(max_length=300, help_text="Name of the Item")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID to be generated")
    description = models.TextField(max_length=300, help_text="Brief Description of the Item")
    categoryName = models.ManyToManyField(Category, help_text="Select Category of the Item")
    qr_code = models.ImageField(blank=True, null=True, upload_to="QR_CODE/")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    entry_date = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        qr = f"{self.itemName}"
        qr_code = qrcode.make(qr)
        qr_offset = Image.new('RGB', qr_code.size, 'white')
        draw_img = ImageDraw.Draw(qr_offset)
        qr_offset.paste(qr_code)

        file_name = f"{self.itemName}-{self.id}.png"
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)        

    def __str__(self):
        return f'{self.itemName}'

    def get_absolute_url(self):
        return reverse("item_details")

    def display_category(self):
        return ", ".join(categoryName.categoryName for categoryName in self.categoryName.all()[:4])

class ItemInstance(models.Model):
    instanceName = models.ForeignKey(Item, on_delete=models.RESTRICT, null=True, related_name="instanceName")
    instanceId = models.UUIDField(default=uuid.uuid1, help_text="Unique Instance ID", unique=False)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT, default="AVAILABLE")
    production_date = models.DateTimeField('Date Produced')
    expiry_date = models.DateTimeField('Date Expiring')
    quantity = models.PositiveIntegerField("Quantity, unit defined in Basic Item Information", null=False, default=1)
    entry_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """String for representing the model object"""
        return f'({self.instanceName}) {self.instanceId}'
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']