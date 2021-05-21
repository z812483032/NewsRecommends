# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth.management import create_permissions


class Command(BaseCommand):
    args = '<app app ...>'
    help = 'Sync permissions for specified apps, or all apps if none specified'

    def handle(self, *args, **options):
        if not args:
            appconfigs = apps.get_app_configs()
        else:
            appconfigs = set()
            for arg in args:
                appconfigs.add(apps.get_app_config(arg))
        for app in appconfigs:
            create_permissions(app, options.get('verbosity', 2))
