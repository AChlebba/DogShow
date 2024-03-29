# Generated by Django 4.0.6 on 2022-10-01 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0008_dog_dog_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='dog_img',
            field=models.ImageField(default='img/dog_default.jpg', upload_to='static/img'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(blank=True, default=0, max_length=9)),
                ('user_img', models.ImageField(default='img/default_avatar.jpg', upload_to='static/img')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
