# Generated by Django 3.2.9 on 2022-05-16 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_remove_account_account_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='title',
        ),
    ]