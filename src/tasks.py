from celery import Celery
from src.model import get_total_unclassified, get_total_unclassified_images, get_total_unclassified_short_videos, get_total_unclassified_long_videos, get_total_unclassified_longest_videos
from src.model_batch import new_batch, schedule_batch, complete_batch, get_is_running
from src.classifier import Classifier
from src.utils import get_logger
from celery.schedules import crontab
from dotenv import dotenv_values

app = Celery('tasks', 
              broker='amqp://guest@localhost//',
              backend='rpc://guest@localhost//')
dotenv_path = '/app/.env'
env = dotenv_values(dotenv_path)

app.conf.timezone = 'America/New_York'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=env['HOUR'], minute=env['MINUTE'], day_of_month=env['DAY_OF_MONTH'], month_of_year=env['MONTH'], day_of_week=env['DAY_OF_WEEK']),
        start_schedule.s(),
    )

@app.task
def start_schedule():
    logger = get_logger("classifier.log")
    logger.info('**** STARTING SCHEDULED TASK ****')
    classify_task()

@app.task
def classify_task():
    total = get_total_unclassified()
    # Celery loses connection to the broker when it takes too long to classify and just restart the process with an empty batch
    # Stupid library...
    if total.total == 0:
        return False
    
    is_running = get_is_running()
    # Never runs if its already running
    if is_running:
        return False

    logger = get_logger("classifier.log")

    logger.info('*********************************************')
    logger.info('- PREPARING NEW BATCH')
    t_images = get_total_unclassified_images()
    t_short = get_total_unclassified_short_videos()
    t_videos = get_total_unclassified_long_videos()
    t_long = get_total_unclassified_longest_videos()
    
    # Completes any previously failed batch
    complete_batch()
    new_batch({
        'total_images': int(t_images.total), 
        'total_short_videos': int(t_short.total), 
        'total_videos': int(t_videos.total), 
        'total_long_videos': int(t_long.total)
    })

    is_running = get_is_running()
    
    
    logger.info('- BATCH '+ str(is_running.id) +' IS RUNNING')
    classifier = Classifier(is_running.id)
    prepare = classifier.prepare()
    logger.info('- VERIFYING CONNECTION/MOUNT ERRORS')
    if prepare['error']:
        logger.error(prepare)
        return prepare
    logger.info('  NO ERRORS FOUND')
    logger.info('- STARTING CLASSIFICATION')
    classifier.classify()
    logger.info('  CLASSIFICATION FINISHED')
    logger.info('*********************************************')
    return True