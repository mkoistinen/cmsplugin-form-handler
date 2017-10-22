# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SamplePluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, to='cms.CMSPlugin', parent_link=True, related_name='sample_samplepluginmodel', auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
