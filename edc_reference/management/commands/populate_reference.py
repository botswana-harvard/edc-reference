from django.core.management.base import BaseCommand

from edc_reference.populater import Populater
from edc_constants.constants import YES, NO


class Command(BaseCommand):

    help = 'Populates the reference model'

    def add_arguments(self, parser):

        parser.add_argument(
            '--models',
            dest='models',
            nargs='*',
            default=None,
            help=('run for a select list of models (label_lower syntax)'),
        )
        parser.add_argument(
            '--exclude_models',
            dest='exclude_models',
            nargs='*',
            default=None,
            help=('exclude a select list of models (label_lower syntax)'),
        )

        parser.add_argument(
            '--skip-existing',
            dest='skip_existing',
            nargs='?',
            choices=[YES, NO],
            default=NO,
            const=YES,
            help=(f'skip model if records already exist (Default: {NO})'),
        )

        parser.add_argument(
            '--summarize',
            dest='summarize',
            nargs='?',
            choices=[YES, NO],
            const=YES,
            default=NO,
            help=(f'Summarize existing data (Default: {NO})'),
        )

        parser.add_argument(
            '--dry-run',
            dest='dry_run',
            nargs='?',
            choices=[YES, NO],
            const=YES,
            default=NO,
            help=(f'Summarize existing data (Default: {NO})'),
        )

    def handle(self, *args, **options):
        models = options.get('models')
        exclude_models = options.get('exclude_models')
        skip_existing = options.get('skip_existing')
        skip_existing = None if skip_existing == NO else YES
        summarize = options.get('summarize')
        summarize = None if summarize == NO else YES
        dry_run = options.get('dry_run')
        dry_run = None if dry_run == NO else YES
        populater = Populater(
            models=models, exclude_models=exclude_models,
            skip_existing=skip_existing,
            dry_run=dry_run)
        if summarize:
            populater.summarize()
        else:
            populater.populate()