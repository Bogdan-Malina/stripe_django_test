# Generated by Django 4.1.6 on 2023-02-15 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('api', '0013_remove_order_item_remove_order_quantity_basketitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.session', unique=True),
        ),
    ]
