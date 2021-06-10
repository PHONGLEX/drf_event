# Generated by Django 3.2.4 on 2021-06-10 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
        ('event_controller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmain',
            name='address_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_address', to='user.addressglobal'),
        ),
        migrations.AddField(
            model_name='eventmain',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventfeature',
            name='eventmain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_features', to='event_controller.eventmain'),
        ),
        migrations.AddField(
            model_name='eventattender',
            name='eventmain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_attenders', to='event_controller.eventmain'),
        ),
        migrations.AddField(
            model_name='eventattender',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attendant', to=settings.AUTH_USER_MODEL),
        ),
    ]
