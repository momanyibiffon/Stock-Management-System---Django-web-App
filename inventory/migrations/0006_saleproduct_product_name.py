# Generated by Django 3.0.2 on 2020-12-28 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20201205_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleproduct',
            name='product_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]