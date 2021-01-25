from django.apps import AppConfig


class AssetmonitoringConfig(AppConfig):
    name = 'assetMonitoring'

    def ready(self):
        from checkAssetsPrices import checkStockJob
        checkStockJob.start()
