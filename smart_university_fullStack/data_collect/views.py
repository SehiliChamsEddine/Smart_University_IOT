from django.shortcuts import render
from .models import Tempurature,Himidity,WaterLevel
from django.http import JsonResponse
import time 
# Create your views here.

def get_latest_data(request):
    try:
        # Query the latest VoltageData from the database
        latest_tempurature_data = Tempurature.objects.latest('timestamp')
        latest_himidity_data = Himidity.objects.latest('timestamp')
        latest_waterlevel_data = WaterLevel.objects.latest('timestamp')
        print(latest_tempurature_data,latest_himidity_data,latest_waterlevel_data,'-----------------------------------------')
        # Extract the timestamp and voltage values
        timestamp_tempurature = latest_tempurature_data.timestamp
        tempurature = latest_tempurature_data.tempurature
        timestamp_himidity = latest_himidity_data.timestamp
        himidity = latest_himidity_data.himidity
        timestamp_waterlevel = latest_waterlevel_data.timestamp
        waterlevel = latest_waterlevel_data.waterlevel
        
        # Return the data as JSON
        return JsonResponse({'timestamp_tempurature': timestamp_tempurature, 
                             'tempurature': tempurature,
                             'timestamp_himidity': timestamp_himidity,
                             'himidity': himidity,
                             'timestamp_waterlevel': timestamp_waterlevel,
                               'waterlevel': waterlevel}
                             )
    except:
         print('will be returned -------')
         duration =time.time()
         return JsonResponse({'timestamp_tempurature': duration, 
                             'tempurature': 0.0,
                             'timestamp_himidity': duration,
                             'himidity': 0.0,
                             'timestamp_waterlevel': duration,
                               'waterlevel': 0.0})
    