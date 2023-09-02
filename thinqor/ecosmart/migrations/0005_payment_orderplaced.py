# Generated by Django 4.2.4 on 2023-09-01 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecosmart', '0004_discountcoupon_checkout'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('razorpay_order_id', models.CharField(max_length=100)),
                ('razorpay_payment_status', models.CharField(max_length=100)),
                ('razorpay_payment_id', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.register')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending')], default='Pending', max_length=50)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.products')),
                ('quantity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.checkout')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosmart.register')),
            ],
        ),
    ]