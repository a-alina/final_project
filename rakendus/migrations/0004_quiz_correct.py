# Generated by Django 4.2.8 on 2023-12-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rakendus", "0003_quiz_attempt_number_quiz_quiz_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz", name="correct", field=models.BooleanField(default=False),
        ),
    ]
