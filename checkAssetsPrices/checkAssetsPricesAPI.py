import requests
from yahooquery import Ticker
from assetMonitoring.models import Asset, Schedule
from django.core.mail import send_mail
import json
import sys

def prepare_email(subject, msg, to):
    try: 
        send_mail(
            subject,
            msg,
            'drope.jardim@gmail.com',
            [to],
            fail_silently=False,
        )
    except:
        e = sys.exc_info()[0]
        print(e)

def check_asset_price(asset):
    checkAsset = Ticker(asset.asset_name)
    if checkAsset:
        summary = checkAsset.summary_detail[asset.asset_name]
        if summary:
            price = summary['bid']
            print('summary: ', summary)
            if (price):
                asset.price = price
                asset.save()
                if price >= asset.up_price:
                    print('Vender')
                    subject = 'Venda seu ativo: '+ asset.asset_name
                    msg = 'Ativo ' +  asset.asset_name + ' está valendo mais de: R$: ' + str(asset.up_price)
                    prepare_email(subject, msg, asset.user_email)
                elif price <= asset.low_price:
                    print('comprar')
                    subject = 'Compre o ativo: '+ asset.asset_name
                    msg = 'Ativo ' +  asset.asset_name + ' está abaixo de: R$: ' + str(asset.low_price)
                    prepare_email(subject, msg, asset.user_email)

def start_check_assets_prices():
    assets = Asset.objects.all()
    schedule = Schedule.objects.last()
    if schedule:
        for asset in assets:
            check_asset_price(asset)