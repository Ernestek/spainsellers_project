# Generated by Django 4.2.2 on 2023-07-28 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spainsellersitem',
            name='link',
            field=models.CharField(default=1, max_length=512),
            preserve_default=False,
        ),
    ]
