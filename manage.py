from flask.ext.script import Manager

from rq import Queue

from ioos_catalog import app, db, queue, redis_connection

from ioos_catalog.tasks.stat import queue_ping_tasks
from ioos_catalog.tasks.harvest import queue_harvest_tasks
from ioos_catalog.tasks.reindex_services import reindex_services
from ioos_catalog.tasks.send_email import send_daily_report_email

manager = Manager(app)

@manager.command
def queue_pings():
    queue_ping_tasks()

@manager.command
def queue_harvests():
    queue_harvest_tasks()

@manager.command
def empty_queue():
    queue.empty()

@manager.command
def empty_failed():
    fqueue = Queue('failed', connection=redis_connection)
    fqueue.empty()

@manager.command
def queue_reindex():
    queue.enqueue(reindex_services)

@manager.command
def queue_daily_status():
    queue.enqueue(send_daily_report_email)

if __name__ == "__main__":
    manager.run()


