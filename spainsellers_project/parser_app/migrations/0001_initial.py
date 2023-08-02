# Generated by Django 4.2.2 on 2023-07-28 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpainSellersItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=256, unique=True)),
                ('item_name', models.CharField(max_length=512)),
                ('price', models.CharField(max_length=256)),
                ('in_stock', models.BooleanField()),
            ],
            options={
                'verbose_name': 'SpainSellersItem',
                'verbose_name_plural': 'SpainSellersItems',
            },
        ),
    ]