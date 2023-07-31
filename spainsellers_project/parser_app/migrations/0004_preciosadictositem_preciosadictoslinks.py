# Generated by Django 4.2.2 on 2023-07-31 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0003_repuestosfuentesitem_repuestosfuenteslinks'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreciosadictosItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=256, unique=True)),
                ('link', models.CharField(max_length=512)),
                ('item_name', models.CharField(max_length=512)),
                ('price', models.CharField(max_length=256)),
                ('in_stock', models.BooleanField()),
            ],
            options={
                'verbose_name': 'PreciosadictosItem',
                'verbose_name_plural': 'PreciosadictosItems',
            },
        ),
        migrations.CreateModel(
            name='PreciosadictosLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=512, unique=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'PreciosadictosLink',
                'verbose_name_plural': 'PreciosadictosLinks',
            },
        ),
    ]
