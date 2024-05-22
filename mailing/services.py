import pytz
from datetime import timedelta, datetime
from config import settings
from django.core.mail import send_mail
from django.core.cache import cache

from mailing.models import Mailing, Logs


def my_job():
    day = timedelta(days=1)
    week = timedelta(days=7)
    month = timedelta(days=28)

    # mailings = Mailing.objects.all().filter(is_activated=True)
    zone = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(zone)
    mailings = Mailing.objects.all().filter(next_date__lte=today).filter(is_activated=True)

    for mailing in mailings:
        if mailing.status != 'finished':
            mailing.status = 'active'
            mailing.save()
            emails_list = [client.email for client in mailing.mail_to.all()]

            print(f'Рассылка {mailing.name} - начало {mailing.next_date}, конец {mailing.end_date}')

            result = send_mail(
                subject=mailing.message.topic,
                message=mailing.message.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=emails_list
            )

            status = result == True

            log = Logs(mailing=mailing, status=status)
            log.save()

            if status:  # на случай сбоя рассылки она останется активной
                if mailing.next_date < mailing.end_date:
                    mailing.status = 'created'
                else:
                    mailing.status = 'finished'

            if mailing.interval == 'daily':
                mailing.next_date = log.last_datetime_sending + day
            elif mailing.interval == 'weekly':
                mailing.next_date = log.last_datetime_sending + week
            elif mailing.interval == 'monthly':
                mailing.next_date = log.last_datetime_sending + month
            elif mailing.interval == 'once':
                mailing.next_date = mailing.end_date

            mailing.save()
            print(f'Рассылка {mailing.name} отправлена {today} (должна была {mailing.next_date}'
                  f'')


def get_cache_mailing_count():
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_mailing_active():
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(is_activated=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_activated=True).count()
    return active_mailings_count