# Generated by Django 4.2.5 on 2023-10-11 10:07

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Hospital", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hospital",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False, populate_from="hospital_name", unique=True
            ),
        ),
    ]
