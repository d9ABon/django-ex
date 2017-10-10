from django.core.management.base import BaseCommand, CommandError

import logging
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("I'm doing something")

