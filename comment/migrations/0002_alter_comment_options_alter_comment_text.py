# Generated by Django 4.2.3 on 2023-10-29 03:00

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-comment_time']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
