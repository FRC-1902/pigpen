from django.core.management.base import BaseCommand
from django.utils import timezone

from teammanager.models import Punch


def close_old_punches():
    yesterday = timezone.now().replace(hour=3, minute=0, second=1)
    q = Punch.objects.filter(end__isnull=True, start__lt=yesterday)

    for p in q:
        if p.meeting.type == 'build':
            if p.start.weekday() > 4:  # Weekends
                p.end = p.start.replace(hour=17, minute=0, second=0)
            else:  # Weekdays
                p.end = p.start.replace(hour=21, minute=0, second=0)

            if p.start < p.end:  # Sanity check
                p.save()
            else:  # Discard punches in after meeting end if not manually punched out.
                p.delete()


class Command(BaseCommand):
    def handle(self, **options):
        close_old_punches()
