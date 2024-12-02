# Generated by Django 5.1.3 on 2024-12-01 21:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adote', '0006_animal_foto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adocao',
            options={'verbose_name': 'Adoção', 'verbose_name_plural': 'Adoções'},
        ),
        migrations.AlterModelOptions(
            name='animal',
            options={'verbose_name': 'Animal', 'verbose_name_plural': 'Animais'},
        ),
        migrations.AlterModelOptions(
            name='historiaanimal',
            options={'verbose_name': 'História do Animal', 'verbose_name_plural': 'Histórias dos Animais'},
        ),
        migrations.AlterModelOptions(
            name='local',
            options={'verbose_name': 'Local', 'verbose_name_plural': 'Locais'},
        ),
        migrations.AlterModelOptions(
            name='tipoanimal',
            options={'verbose_name': 'Tipo de Animal', 'verbose_name_plural': 'Tipos de Animais'},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'verbose_name': 'Usuário', 'verbose_name_plural': 'Usuários'},
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='Telefone inválido. Use um número válido com 10 a 15 dígitos.', regex='^\\+?\\d{10,15}$')]),
        ),
    ]
