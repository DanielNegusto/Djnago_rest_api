# Generated by Django 5.1.4 on 2025-01-25 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_customuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет'), ('stripe', 'Stripe')], max_length=10),
        ),
    ]
