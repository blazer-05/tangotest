# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20160130_1235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', 'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430', 'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b'},
        ),
    ]
