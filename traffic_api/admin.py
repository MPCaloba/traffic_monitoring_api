from django.contrib import admin
from .models import RoadSegments, TrafficReadings

# To access the models in the Django admin page
admin.site.register(RoadSegments)
admin.site.register(TrafficReadings)