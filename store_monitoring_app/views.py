import random
from django.http import JsonResponse
from rest_framework.decorators import api_view
from store_monitoring_app.models import Store, StoreStatus, BusinessHours
from store_monitoring_app.services import generate_report


@api_view(['POST'])
def trigger_report(request):
    # Your logic to generate the report asynchronously and save it in the database.
    # Return a report_id that can be used for polling the status.
    report_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
    return JsonResponse({'report_id': report_id})

def is_report_complete(report_id):
        return True


@api_view(['GET'])
def get_report(request,id):
    report_id = request.GET.get('report_id', '')
    # Your logic to check the status of the report based on the report_id.
    # If the report is not complete, return 'Running' status.
    # If the report is complete, serve the CSV file for download as a response.
    if is_report_complete(report_id):
        # Generate and serve the CSV file
        csv_file = generate_report()
        response = HttpResponse(csv_file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        return response
    else:
        return JsonResponse({'status': 'Running'})
    


    