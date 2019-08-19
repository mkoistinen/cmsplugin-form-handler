# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__version__ = '0.3.0'


def get_session_key(plugin_id):
    return 'cmsplugin_form_{0}'.format(plugin_id)
