# Generated by Django 5.0.6 on 2024-05-23 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0004_keyword_keywordmapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordmapping',
            name='frequency',
            field=models.IntegerField(default=1),
        ),
    ]
