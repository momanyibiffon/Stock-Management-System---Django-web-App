# Generated by Django 3.0.2 on 2020-12-28 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_saleproduct_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiveproduct',
            name='product_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]