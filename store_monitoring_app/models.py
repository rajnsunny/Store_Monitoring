from django.db import models

class Store(models.Model):
    store_id = models.CharField(max_length=50, unique=True)
    timezone_str = models.CharField(max_length=100, default='America/Chicago')

class StoreStatus(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp_utc = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)

class BusinessHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    start_time_local = models.TimeField(auto_now_add=True)
    end_time_local = models.TimeField(auto_now_add=True)
