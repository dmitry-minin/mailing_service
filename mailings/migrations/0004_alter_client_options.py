# Generated by Django 5.2.3 on 2025-07-27 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0003_alter_client_options_alter_mailing_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'permissions': [('view_all_clients', 'Может просматривать всех клиентов')], 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
    ]
