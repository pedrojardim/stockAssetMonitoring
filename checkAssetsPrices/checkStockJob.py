from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from checkAssetsPrices import checkAssetsPricesAPI
from assetMonitoring.models import Schedule 

def start():
    schedule = Schedule.objects.last()
    if schedule:
        scheduler = BackgroundScheduler()
        scheduler.add_job(checkAssetsPricesAPI.start_check_assets_prices, 'interval', minutes=schedule.minutes, id='check=prices')
        scheduler.start()