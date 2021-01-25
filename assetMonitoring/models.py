from django.db import models

class Schedule(models.Model):
    minutes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.minutes)

class Asset(models.Model):
    asset_name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    user_email = models.CharField(max_length=200)
    up_price = models.FloatField(default=0)
    low_price = models.FloatField(default=0)

    def __str__(self):
        return self.asset_name

