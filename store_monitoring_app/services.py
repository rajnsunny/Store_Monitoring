import csv
from io import StringIO
from django.core.files import File
from datetime import datetime, timedelta
from django.utils import timezone
from store_monitoring_app.models import Store, StoreStatus, BusinessHours
import pytz

def generate_report():
    # Your logic to generate the report based on the data in the database.
    # Calculate the uptime and downtime for each store within business hours.
    # Extrapolate the uptime and downtime based on the periodic polls.
    report_data = report()

    # ... Generate the report_data ...

    # Create and store the CSV file
    csv_file = StringIO()
    fieldnames = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'update_last_week',
                  'downtime_last_hour', 'downtime_last_day', 'downtime_last_week']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for data in report_data:
        writer.writerow(data)

    # Save the CSV file temporarily on the server
    temp_csv_file = File(csv_file)
    temp_csv_file.name = 'report.csv'  # Assign a temporary name to the file
    return temp_csv_file


def report():

    report_data = []

    current_time = timezone.now()

    stores = Store.objects.all()

    # Loop through each store to calculate the uptime and downtime
    for store in stores:
        # Get the business hours for the store
        business_hours = BusinessHours.objects.filter(store=store).order_by('day_of_week')

        # Initialize variables to hold total uptime and downtime
        total_uptime_last_hour = timedelta(seconds=0)
        total_uptime_last_day = timedelta(seconds=0)
        total_uptime_last_week = timedelta(seconds=0)
        total_downtime_last_hour = timedelta(seconds=0)
        total_downtime_last_day = timedelta(seconds=0)
        total_downtime_last_week = timedelta(seconds=0)

        # Loop through each business day to calculate uptime and downtime
        for day_info in business_hours:
            # Get the start and end time for the current business day
            start_time_local = day_info.start_time_local
            end_time_local = day_info.end_time_local

            # Convert the start and end time to UTC based on the store's timezone
            start_time_utc, end_time_utc = convert_to_utc(store.timezone_str, current_time, start_time_local, end_time_local)

            # Get the store status entries within the current business day
            status_entries = StoreStatus.objects.filter(
                store=store,
                timestamp_utc__gte=start_time_utc,
                timestamp_utc__lt=end_time_utc
            ).order_by('timestamp_utc')

            # Calculate the uptime and downtime for the current business day
            uptime_day, downtime_day = calculate_uptime_downtime(status_entries, start_time_utc, end_time_utc)

            # Accumulate the uptime and downtime for the last day and last week
            total_uptime_last_day += uptime_day
            total_downtime_last_day += downtime_day
            total_uptime_last_week += uptime_day
            total_downtime_last_week += downtime_day

            # Extrapolate the uptime and downtime for the last hour
            uptime_hour, downtime_hour = extrapolate_uptime_downtime(status_entries, current_time - timedelta(hours=1))
            total_uptime_last_hour += uptime_hour
            total_downtime_last_hour += downtime_hour

        # Append the store's report data to the main report_data list
        report_data.append({
            'store_id': store.store_id,
            'uptime_last_hour': total_uptime_last_hour.total_seconds() / 60,
            'uptime_last_day': total_uptime_last_day.total_seconds() / 3600,
            'uptime_last_week': total_uptime_last_week.total_seconds() / 3600,
            'downtime_last_hour': total_downtime_last_hour.total_seconds() / 60,
            'downtime_last_day': total_downtime_last_day.total_seconds() / 3600,
            'downtime_last_week': total_downtime_last_week.total_seconds() / 3600,
        })

    return report_data


def convert_to_utc(timezone_str, reference_time, local_start_time, local_end_time):
    # Convert local start and end time to aware datetime objects based on the given timezone
    start_time_local = timezone.make_aware(datetime.combine(reference_time.date(), local_start_time))
    end_time_local = timezone.make_aware(datetime.combine(reference_time.date(), local_end_time))

    # Convert local start and end time to UTC
    timezone_obj = pytz.timezone(timezone_str)
    start_time_utc = start_time_local.astimezone(timezone_obj).replace(tzinfo=None)
    end_time_utc = end_time_local.astimezone(timezone_obj).replace(tzinfo=None)

    return start_time_utc, end_time_utc



def calculate_uptime_downtime(status_entries, start_time_utc, end_time_utc):
    uptime = timedelta(seconds=0)
    downtime = timedelta(seconds=0)

    # Initialize the status and last timestamp variables
    last_status = None
    last_timestamp = start_time_utc

    for entry in status_entries:
        stores = Store.objects.filter(store_id=entry.store)
        if len(stores) == 0:
            continue
        time_stamp,time_stamp1 = convert_to_utc(Store.objects.get(store_id=entry.store).timezone_str,timezone.now(),entry.timestamp_utc,entry.timestamp_utc)
        if time_stamp >= end_time_utc:
            break

        # Calculate the time difference between the last timestamp and the current entry's timestamp
        time_diff = time_stamp - last_timestamp

        if last_status == 'active':
            uptime += time_diff
        elif last_status == 'inactive':
            downtime += time_diff

        # Update the last status and timestamp for the next iteration
        last_status = entry.status
        last_timestamp = time_stamp

    # Calculate the time difference from the last entry to the end of the business day
    time_diff = end_time_utc - last_timestamp
    if last_status == 'active':
        uptime += time_diff
    elif last_status == 'inactive':
        downtime += time_diff

    return uptime, downtime


def extrapolate_uptime_downtime(status_entries, reference_time_utc):
    last_status = None
    last_timestamp = None
    uptime = timedelta(seconds=0)
    downtime = timedelta(seconds=0)

    for entry in status_entries:
        stores = Store.objects.filter(store_id=entry.store)
        if len(stores) == 0:
            continue
        time_stamp,time_stamp1 = convert_to_utc(Store.objects.get(store_id=entry.store).timezone_str,timezone.now(),entry.timestamp_utc,entry.timestamp_utc)
        if time_stamp > reference_time_utc:
            break

        if last_status is not None:
            time_diff = time_stamp - last_timestamp

            if last_status == 'active':
                uptime += time_diff
            elif last_status == 'inactive':
                downtime += time_diff

        last_status = entry.status
        last_timestamp = time_stamp

    # Extrapolate the remaining time from the last entry to the reference time
    if last_status == 'active':
        uptime += reference_time_utc - last_timestamp
    elif last_status == 'inactive':
        downtime += reference_time_utc - last_timestamp

    return uptime, downtime
