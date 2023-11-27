from django.urls import path
from .views import (TrafficReadingsView, TrafficReadingsUpdateView, CreateTrafficReadingView,
                    HighIntensityTrafficReadingsView, MediumIntensityTrafficReadingsView, LowIntensityTrafficReadingsView,
                    RoadSegmentsView, RoadSegmentsUpdateView, CreateRoadSegmentView,
                    HighIntensityRoadSegmentsView, MediumIntensityRoadSegmentsView, LowIntensityRoadSegmentsView,
                    SensorsView, SensorsUpdateView, SensorReadingsView, CreateSensorReadingView, SensorReadingsUpdateView,
                    CarsView, CarDetailsView)


urlpatterns = [
    # Home page
    path('', TrafficReadingsView.as_view(), name='home'),
    
    # Traffic Readings
    path('traffic-readings/', TrafficReadingsView.as_view(), name='all-traffic-readings'),
    path('traffic-readings/<int:pk>/', TrafficReadingsUpdateView.as_view(), name='individual-traffic-reading'),
    path('traffic-readings/high-intensity/', HighIntensityTrafficReadingsView.as_view(), name='high-intensity-traffic-readings'),
    path('traffic-readings/medium-intensity/', MediumIntensityTrafficReadingsView.as_view(), name='medium-intensity-traffic-readings'),
    path('traffic-readings/low-intensity/', LowIntensityTrafficReadingsView.as_view(), name='low-intensity-traffic-readings'),
    path('create-traffic-reading/', CreateTrafficReadingView.as_view(), name='create-traffic-reading'),
    
    # Road Segments
    path('road-segments/', RoadSegmentsView.as_view(), name='all-road-segments'),
    path('road-segments/<int:pk>/', RoadSegmentsUpdateView.as_view(), name='individual-road-segment'),
    path('road-segments/high-intensity/', HighIntensityRoadSegmentsView.as_view(), name='high-intensity-road-segments'),
    path('road-segments/medium-intensity/', MediumIntensityRoadSegmentsView.as_view(), name='medium-intensity-road-segments'),
    path('road-segments/low-intensity/', LowIntensityRoadSegmentsView.as_view(), name='low-intensity-road-segments'),
    path('create-road-segment/', CreateRoadSegmentView.as_view(), name='create-road-segment'),
    
    # Sensors
    path('sensors/', SensorsView.as_view(), name='all-sensors'),
    path('sensors/<int:pk>/', SensorsUpdateView.as_view(), name='individual-sensor'),
    path('sensors-readings/', SensorReadingsView.as_view(), name='sensors-readings'),
    path('sensors-readings/<int:pk>/', SensorReadingsUpdateView.as_view(), name='individual-sensor-readings'),
    path('create-sensor-reading/', CreateSensorReadingView.as_view(), name='create-sensor-reading'),
    
    # Cars
    path('cars/', CarsView.as_view(), name='all-cars'),
    path('cars/<str:car_license_plate>/', CarDetailsView.as_view(), name='individual-car'),
]