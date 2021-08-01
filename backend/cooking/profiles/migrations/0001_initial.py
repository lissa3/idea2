# Generated by Django 3.2.4 on 2021-07-30 20:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import timestamp.broadcast_utils.idea_utils
import timestamp.broadcast_utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unid', models.CharField(blank=True, db_index=True, max_length=6)),
                ('image', models.ImageField(blank=True, null=True, upload_to=timestamp.broadcast_utils.idea_utils.upload_img, validators=[django.core.validators.FileExtensionValidator(('JPG', 'JPEG', 'PNG')), timestamp.broadcast_utils.validators.validate_size])),
                ('bio', models.TextField(blank=True, default='')),
                ('website', models.URLField(blank=True, default='', max_length=100)),
                ('badge_bg', models.CharField(blank=True, default='', max_length=30)),
                ('following', models.ManyToManyField(blank=True, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
