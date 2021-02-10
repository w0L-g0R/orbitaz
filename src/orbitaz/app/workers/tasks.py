from django.utils import timezone
from orbitaz.app.cron.func import create_text_file

from django_q.models import Schedule

Schedule.objects.create(
    func="orbitaz.app.cron.func.create_text_file",
    kwargs={"content": "Insert this into a text file"},
    hook="orbitaz.app.cron.hooks.print_result",
    name="Text file creation process",
    schedule_type=Schedule.ONCE,
    next_run=timezone.now(),
)
