# Generated by Django 4.2.1 on 2023-05-30 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_alter_service_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=18, null=True, verbose_name='Price'),
        ),
    ]
