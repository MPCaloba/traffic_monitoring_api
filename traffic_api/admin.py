from django.contrib import admin
from .models import RoadSegments, TrafficReadings, Sensors, SensorReadings, Cars

# To access the models in the Django admin page
admin.site.register(RoadSegments)
admin.site.register(TrafficReadings)
admin.site.register(Sensors)
admin.site.register(SensorReadings)
admin.site.register(Cars)