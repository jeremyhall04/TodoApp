# Generated by Django 2.2.7 on 2019-11-15 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todoApp", "0002_auto_20191111_1443"),
    ]

    operations = [
        migrations.AddField(
            model_name="item", name="completed_date", field=models.TimeField(null=True),
        ),
    ]
