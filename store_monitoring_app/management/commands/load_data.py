import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from store_monitoring_app.models import Store, StoreStatus, BusinessHours

class Command(BaseCommand):
    help = 'Load data from CSV into the database'

    def handle(self, *args, **kwargs):
    #    Load Store data
        with open('D:\Project\loop\store_monitoring_project\store_monitoring_app\data\store_data.csv', 'r') as file:
            reader = csv.reader(file)
            bool = True
            for row in reader:
                if(bool):
                    bool = False
                    continue
                store_id, timezone_str = row
                store, created = Store.objects.get_or_create(store_id=store_id)
                if created:  # Only set the timezone_str if the store is newly created
                    store.timezone_str = timezone_str
                    store.save()

      #  Load StoreStatus data
        with open('D:\Project\loop\store_monitoring_project\store_monitoring_app\data\store.csv', 'r') as file:
            reader = csv.reader(file)
            bool = True
            for row in reader:
                if(bool):
                    bool = False
                    continue
                    
                store_id, status, timestamp_utc  = row
                stores = Store.objects.filter(store_id=store_id)
                if len(stores) == 0:
                    continue
                store = Store.objects.get(store_id=store_id)
                timestamp_utc = timestamp_utc[:timestamp_utc.find('.')]
                timestamp_utc = datetime.strptime(timestamp_utc, '%Y-%m-%d %H:%M:%S')
                StoreStatus.objects.create(store=store, timestamp_utc=timestamp_utc, status=status)

        # # Load BusinessHours data
        with open('D:\Project\loop\store_monitoring_project\store_monitoring_app\data\Bussiness_Hour.csv', 'r') as file:
            reader = csv.reader(file)
            bool = True
            for row in reader:
                if(bool):
                    bool = False
                    continue
                store_id, day_of_week, start_time_local, end_time_local = row
                stores = Store.objects.filter(store_id=store_id)
                if len(stores) == 0:
                    continue
                store = Store.objects.get(store_id=store_id)
                if(store is None):
                    start_time_local = "00:00:00"
                    end_time_local = "23:59:59"
                    store = store_id

                BusinessHours.objects.create(store=store, day_of_week=day_of_week,
                                             start_time_local=start_time_local, end_time_local=end_time_local)
