# Generated by Django 4.2.3 on 2023-11-01 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_alter_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent_id',
            field=models.IntegerField(default=0),
        ),
    ]
