# Generated by Django 4.1 on 2022-08-27 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_question_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questfollower',
            name='user',
        ),
    ]
