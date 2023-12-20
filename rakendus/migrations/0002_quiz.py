# Generated by Django 4.2.8 on 2023-12-11 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rakendus", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.TextField()),
                ("correct_answer", models.TextField()),
                ("user_answer", models.TextField()),
            ],
        ),
    ]
