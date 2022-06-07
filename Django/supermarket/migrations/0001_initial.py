# Generated by Django 3.2.11 on 2022-04-21 16:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(help_text='Type in the Category of the Item', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('itemName', models.CharField(help_text='Name of the Item', max_length=300)),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID to be generated', primary_key=True, serialize=False)),
                ('description', models.TextField(help_text='Brief Description of the Item', max_length=300)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='QR_CODE/')),
                ('entry_date', models.DateTimeField(default=datetime.datetime.now)),
                ('categoryName', models.ManyToManyField(help_text='Select Category of the Item', to='supermarket.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(help_text='Unit of the Item', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ItemInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instanceId', models.UUIDField(default=uuid.uuid1, help_text='Unique Instance ID')),
                ('production_date', models.DateTimeField(verbose_name='Date Produced')),
                ('expiry_date', models.DateTimeField(verbose_name='Date Expiring')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity, unit defined in Basic Item Information')),
                ('entry_date', models.DateTimeField(default=datetime.datetime.now)),
                ('instanceName', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='instanceName', to='supermarket.item')),
                ('status', models.ForeignKey(default='AVAILABLE', on_delete=django.db.models.deletion.RESTRICT, to='supermarket.status')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supermarket.unit'),
        ),
    ]
