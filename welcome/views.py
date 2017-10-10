import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

# Create your views here.

def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    return HttpResponse(PageView.objects.count())

def test(request):
    from raven import Client
    client = Client('https://2fe25e1e32c94897badae5897fcf983d:4e3150d3cc1146afa86e2ac062efddf2@sentry.io/228141')


    def test1():
        client.user_context({
           'env': os.environ,
        })

    def test2():
        from raven import breadcrumbs
        breadcrumbs.record(message='This is an important message',
                           category='my_module', level='warning')
        client.captureMessage('Something went fundamentally wrong')

    def test3():
        client.context.activate()
        client.context.merge({'user': {
            'email': 'sdgfdsghf'
        }})
        try:
            1 / 0
        except ZeroDivisionError:
            client.captureException()
        finally:
            client.context.clear()

    def test4():
        from raven.handlers.logging import SentryHandler
        handler = SentryHandler(client)

        from raven.conf import setup_logging
        setup_logging(handler)

        import logging
        logger = logging.getLogger(__name__)

        # If you're actually catching an exception, use `exc_info=True`
        #logger.error('There was an error, with a stacktrace!', exc_info=True)

        # If you don't have an exception, but still want to capture a
        # stacktrace, use the `stack` arg
        logger.error('There was an error, with a stacktrace!', extra={
            'stack': True,

            'data': {
                # You may specify any values here and Sentry will log and output them
                'username': 'AAAAAA',
            }
        })

    def test5():
        from raven.contrib.django.raven_compat.models import client
        try:
            1 / 0
        except ZeroDivisionError:
            client.captureException()

    def test6():
        import logging
        logger = logging.getLogger(__name__)
        logger.info('CCCCC')
        logger.error('DDDDD')



    test1()
    test2()
    test3()
    test4()
    test5()
    test6()

    return HttpResponse('DONE')