# Generated by Django 3.0.1 on 2020-01-09 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_emoji_emojimatch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emoji',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
