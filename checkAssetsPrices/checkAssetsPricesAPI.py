import requests
from yahooquery import Ticker
from assetMonitoring.models import Asset, Schedule
from django.core.mail import send_mail
from stockAssetMonitoring.settings import EMAIL_HOST_USER
import json
import sys

def prepare_email(subject, msg, to):
    try: 
        send_mail(
            subject,
            msg,
            EMAIL_HOST_USER,
            [to],
            fail_silently=False,
        )
    except:
        e = sys.exc_info()[0]
        print(e)

def check_asset_price(asset):
    assetName = asset.asset_name
    checkAsset = Ticker(assetName)
    if checkAsset:
        price = checkAsset.price[assetName]['regularMarketPrice']
        if (price):
            asset.price = price
            asset.save()
            if price >= asset.up_price:
                subject = 'Venda seu ativo: '+ assetName
                msg = 'Ativo ' +  assetName + ' está valendo mais de: R$: ' + str(asset.up_price)
                prepare_email(subject, msg, asset.user_email)
            elif price <= asset.low_price:
                subject = 'Compre o ativo: '+ assetName
                msg = 'Ativo ' +  assetName + ' está abaixo de: R$: ' + str(asset.low_price)
                prepare_email(subject, msg, asset.user_email)

def start_check_assets_prices():
    assets = Asset.objects.all()
    schedule = Schedule.objects.last()
    if schedule:
        for asset in assets:
            check_asset_price(asset)