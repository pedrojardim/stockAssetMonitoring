from django.shortcuts import render, redirect
from django.http import HttpResponse
from yahooquery import Ticker

from .model_form import AssetForm, ScheduleForm

from .models import Asset, Schedule

def index(request):
    assets = Asset.objects.all()
    schedule = Schedule.objects.last()
    return render(request, 'assets.html', { 'assets': assets, 'schedule': schedule })

def create_asset(request):
    newAsset = AssetForm()
    if request.method == 'POST':
        #checkAsset = Ticker(newAsset.asset_name)
        #print(summary = checkAsset.summary_detail[asset.asset_name])
        newAsset = AssetForm(request.POST, request.FILES)
        if newAsset.is_valid():
            assetName = newAsset.cleaned_data['asset_name']
            consultAsset = Ticker(assetName)
            print('consultAsset: ', consultAsset)
            print('consultAsset: ', consultAsset.summary_detail[assetName])
            if 'Quote not found' in consultAsset.summary_detail[assetName]:
                return render(request, 'asset_form.html', { 'newAsset': newAsset, 'assetNotFound': True })
            else:
                newAsset.save()
                return redirect('index')
            print("consultAsset: ", consultAsset.summary_detail)
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index' }}">reload</a>""")
    else:
        return render(request, 'asset_form.html', { 'newAsset': newAsset })

def update_asset(request, asset_id):
    asset_id = int(asset_id)
    try:
        selectedAsset = Asset.objects.get(id = asset_id)
    except Asset.DoesNotExist:
        return redirect('index')
    updaedAsset = AssetForm(request.POST or None, instance = selectedAsset)
    if updaedAsset.is_valid():
       updaedAsset.save()
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
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index' }}">reload</a>""")
    else:
        return render(request, 'schedule_form.html', { 'newSchedule': newSchedule })

