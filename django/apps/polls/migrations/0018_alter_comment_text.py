# Generated by Django 3.2.9 on 2022-06-09 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_account_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1000),
        ),
    ]