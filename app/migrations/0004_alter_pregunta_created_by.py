# Generated by Django 4.2.7 on 2023-11-08 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_remove_comentario_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
