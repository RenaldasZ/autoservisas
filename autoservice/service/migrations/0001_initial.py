# Generated by Django 4.2.1 on 2023-05-30 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence_plate', models.CharField(max_length=20, verbose_name='Licence Plate')),
                ('vin_code', models.CharField(max_length=50, verbose_name='VIN Code')),
                ('customer', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100, verbose_name='Make')),
                ('model', models.CharField(max_length=100, verbose_name='Model')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
                ('engine', models.CharField(max_length=100, verbose_name='Engine')),
            ],
            options={
                'verbose_name': 'CarModel',
                'verbose_name_plural': 'CarModels',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50, verbose_name='Date')),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.car')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('price', models.IntegerField(verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=50, verbose_name='Quantity')),
                ('price', models.CharField(max_length=50, verbose_name='Price')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.order')),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
            options={
                'verbose_name': 'Order List',
                'verbose_name_plural': 'Order Lists',
            },
        ),
        migrations.AddField(
            model_name='car',
            name='car_model_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.carmodel'),
        ),
    ]
