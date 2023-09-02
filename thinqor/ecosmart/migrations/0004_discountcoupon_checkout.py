# Generated by Django 4.2.4 on 2023-08-31 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecosmart', '0003_shippingaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('total_amount', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.register')),
                ('user_shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.shippingaddress')),
            ],
        ),
    ]