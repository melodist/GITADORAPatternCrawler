from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', hour='0')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass