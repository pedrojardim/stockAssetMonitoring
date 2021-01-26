from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from checkAssetsPrices import checkAssetsPricesAPI
from assetMonitoring.models import Schedule 
import sys

scheduler = BackgroundScheduler()

def start():
    try:
        schedule = Schedule.objects.last()
        if schedule:
            scheduler.add_job(checkAssetsPricesAPI.start_check_assets_prices, 'interval', minutes=schedule.minutes, id='check-prices')
            scheduler.start()
    except:
        e = sys.exc_info()[0]
        print(e)

def re_start():
    schedule = Schedule.objects.last()
    scheduler.reschedule_job('check-prices', trigger='cron', minute=schedule.minutes)