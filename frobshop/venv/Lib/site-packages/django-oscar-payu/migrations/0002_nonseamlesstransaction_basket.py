# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonseamlesstransaction',
            name='basket',
            field=models.CharField(db_index=True, max_length=12, null=True, blank=True),
        ),
    ]
