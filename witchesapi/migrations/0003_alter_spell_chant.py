# Generated by Django 4.2.8 on 2023-12-07 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('witchesapi', '0002_spell_repeat_chant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='chant',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]