# Generated by Django 3.2.4 on 2021-09-08 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted_content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(max_length=1024),
        ),
    ]
