# Generated by Django 3.2.16 on 2023-05-10 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20230510_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
