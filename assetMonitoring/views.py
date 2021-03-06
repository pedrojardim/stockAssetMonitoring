from django.shortcuts import render, redirect
from django.http import HttpResponse
from yahooquery import Ticker
from apscheduler.schedulers.background import BackgroundScheduler
from .model_form import AssetForm, ScheduleForm

from .models import Asset, Schedule

def index(request):
    assets = Asset.objects.all()
    schedule = Schedule.objects.last()
    return render(request, 'assets.html', { 'assets': assets, 'schedule': schedule })

def create_asset(request):
    newAsset = AssetForm()
    if request.method == 'POST':
        newAsset = AssetForm(request.POST, request.FILES)

        if newAsset.is_valid():
            assetName = newAsset.cleaned_data['asset_name']             
            consultAsset = Ticker(assetName)
            if 'Quote not found' in consultAsset.summary_detail[assetName]:
                return render(request, 'asset_form.html', { 'newAsset': newAsset, 'assetNotFound': True })
            else:
                price = consultAsset.price[assetName]['regularMarketPrice']
                asset = newAsset.save(commit=False)
                asset.price = price
                asset.save()
                return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index' }}">reload</a>""")
    else:
        return render(request, 'asset_form.html', { 'newAsset': newAsset })

def update_asset(request, asset_id):
    asset_id = int(asset_id)
    try:
        selectedAsset = Asset.objects.get(id = asset_id)
    except selectedAsset.DoesNotExist:
        return redirect('index')
    updaedAsset = AssetForm(request.POST or None, instance = selectedAsset)

    if updaedAsset.is_valid():
        assetName = updaedAsset.cleaned_data['asset_name']
        consultAsset = Ticker(assetName)
        if 'Quote not found' in consultAsset.summary_detail[assetName]:
            return render(request, 'asset_form.html', { 'newAsset': updaedAsset, 'assetNotFound': True })
        else:
            price = consultAsset.price[assetName]['regularMarketPrice']
            asset = updaedAsset.save(commit=False)
            asset.price = price
            asset.save()
            return redirect('index')

    return render(request, 'asset_form.html', { 'newAsset': updaedAsset })

def delete_asset(request, asset_id):
    asset_id = int(asset_id)
    try:
        asset_to_delete = Asset.objects.get(id = asset_id)
    except Asset.DoesNotExist:
        return redirect('index')
    asset_to_delete.delete()
    return redirect('index')

def create_schedule(request):
    newSchedule = ScheduleForm()
    if request.method == 'POST':
        newSchedule = ScheduleForm(request.POST, request.FILES)
        if newSchedule.is_valid():
            newSchedule.save()
            from checkAssetsPrices import checkStockJob
            checkStockJob.start()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index' }}">reload</a>""")
    else:
        return render(request, 'schedule_form.html', { 'newSchedule': newSchedule })

def update_schedule(request, schedule_id):
    schedule_id = int(schedule_id)
    try: 
        selectedSchedule = Schedule.objects.get(id = schedule_id)
    except selectedSchedule.DoesNotExist:
        return redirect('index')
    updaedScheduler = ScheduleForm(request.POST or None, instance = selectedSchedule)
    if updaedScheduler.is_valid():
       updaedScheduler.save()

       from checkAssetsPrices import checkStockJob
       checkStockJob.re_start()

       return redirect('index')
    return render(request, 'schedule_form.html', { 'newSchedule': updaedScheduler })