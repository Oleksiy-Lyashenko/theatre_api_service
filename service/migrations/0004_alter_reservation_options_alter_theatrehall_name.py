# Generated by Django 5.0.1 on 2024-01-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0003_alter_performance_show_time_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reservation",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterField(
            model_name="theatrehall",
            name="name",
            field=models.CharField(max_length=63, unique=True),
        ),
    ]
