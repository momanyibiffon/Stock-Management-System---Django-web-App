# Generated by Django 3.0.2 on 2020-12-29 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_receiveproduct_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiveproduct',
            name='received_bottle_capacity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.BottleVolume'),
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='sold_bottle_capacity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.BottleVolume'),
        ),
    ]