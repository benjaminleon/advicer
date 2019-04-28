# Generated by Django 2.1.5 on 2019-04-01 19:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0010_auto_20190401_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='user_name',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('movie', 'user')},
        ),
    ]