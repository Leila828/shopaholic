# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NonSeamlessTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txnid', models.CharField(max_length=32, db_index=True)),
                ('productinfo', models.CharField(max_length=100)),
                ('amount', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('currency', models.CharField(max_length=8, null=True, blank=True)),
                ('firstname', models.CharField(max_length=32, null=True, blank=True)),
                ('lastname', models.CharField(max_length=32, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=12, null=True, blank=True)),
                ('address1', models.CharField(max_length=48, null=True, blank=True)),
                ('address2', models.CharField(max_length=48, null=True, blank=True)),
                ('city', models.CharField(max_length=32, null=True, blank=True)),
                ('state', models.CharField(max_length=32, null=True, blank=True)),
                ('country', models.CharField(max_length=32, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=8, null=True, blank=True)),
                ('udf1', models.CharField(max_length=255, null=True, blank=True)),
                ('udf2', models.CharField(max_length=255, null=True, blank=True)),
                ('udf3', models.CharField(max_length=255, null=True, blank=True)),
                ('udf4', models.CharField(max_length=255, null=True, blank=True)),
                ('udf5', models.CharField(max_length=255, null=True, blank=True)),
                ('pg', models.CharField(max_length=8, null=True, blank=True)),
                ('drop_category', models.CharField(max_length=32, null=True, blank=True)),
                ('custom_note', models.CharField(max_length=128, null=True, blank=True)),
                ('note_category', models.CharField(max_length=32, null=True, blank=True)),
                ('offer_key', models.CharField(max_length=32, null=True, blank=True)),
                ('raw_response', models.TextField(max_length=1024)),
                ('raw_request', models.TextField(max_length=1024)),
                ('error_code', models.CharField(max_length=32, null=True, blank=True)),
                ('error_message', models.CharField(max_length=128, null=True, blank=True)),
                ('response', models.CharField(blank=True, max_length=2, null=True, choices=[('N', 'New'), ('W', 'Awaiting Confirmation'), ('S', 'Success'), ('F', 'Failure'), ('C', 'Cancelled')])),
                ('orderid', models.CharField(max_length=32, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]
