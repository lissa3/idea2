# Generated by Django 3.2.4 on 2021-09-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_alter_comment_deleted_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(max_length=6548),
        ),
    ]
