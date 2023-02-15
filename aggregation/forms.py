import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def proper_date(value):
    now = timezone.now()
    future = now + datetime.timedelta(milliseconds=172_800_000)  # Exactly 48 hours
    if (value < now) or (value > future):
        raise ValidationError(
            _('Not Past, not Future more than 2 days.'),
            params={'value': value},
        )


class ReminderForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        help_text='Enter a valid Email for receiving the Reminder.',
    )

    reminder_text = forms.CharField(
        label="Reminder",
        widget=forms.Textarea(attrs={"rows": "5"}),
        help_text='Write down your reminder, please.',
    )

    date_time = forms.DateTimeField(
        label="Date&Time",
        help_text='Enter a valid Day and Time when you will receive the Reminder.\n'
                  'Not Past, not Future more than 2 days',
        validators=[proper_date],
    )
