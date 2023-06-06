# Generated by Django 4.2.1 on 2023-06-05 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0017_alter_car_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='customer',
        ),
        migrations.AddField(
            model_name='car',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL, verbose_name='client'),
        ),
        migrations.AddField(
            model_name='car',
            name='note',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Note'),
        ),
        migrations.AddField(
            model_name='order',
            name='due_back',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='due back'),
        ),
    ]