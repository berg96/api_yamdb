# Generated by Django 3.2 on 2024-01-16 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Код подтверждения'),
        ),
    ]