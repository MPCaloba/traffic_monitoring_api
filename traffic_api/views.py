from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, OuterRef, Subquery, F
from datetime import timedelta
from traffic_monitoring_api.settings import LOW_SPEED_THRESHOLD, HIGH_SPEED_THRESHOLD
from .permissions import IsAdminOrReadOnly, IsAnonymousReadOnly, HasAPIKey
from .models import TrafficReadings, RoadSegments, Sensors, SensorReadings, Cars
from .serializers import (TrafficReadingsSerializer, CreateTrafficReadingSerializer,
                        RoadSegmentsSerializer, CreateRoadSegmentSerializer,
                        SensorsSerializer, SensorReadingsSerializer, CreateSensorReadingSerializer,
                        CarsSerializer)



## TRAFFIC READINGS ---------------------------------------------------------------------------------------------
# 1 - ALL TRAFFIC READINGS
class TrafficReadingsView(ListAPIView):
    queryset = TrafficReadings.objects.all()
    serializer_class = TrafficReadingsSerializer

# 2 - UPDATE OR DELETE INDIVIDUAL TRAFFIC READINGS (only for admin use)
class TrafficReadingsUpdateView(RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        return [IsAnonymousReadOnly()]
    
    queryset = TrafficReadings.objects.all()
    serializer_class = TrafficReadingsSerializer

# 3 - HIGH INTENSITY TRAFFIC READINGS
class HighIntensityTrafficReadingsView(ListAPIView):
    queryset = TrafficReadings.objects.filter(speed__lte = LOW_SPEED_THRESHOLD)
    serializer_class = TrafficReadingsSerializer

# 4 - MEDIUM INTENSITY TRAFFIC READINGS
class MediumIntensityTrafficReadingsView(ListAPIView):
    queryset = TrafficReadings.objects.filter(speed__gt = LOW_SPEED_THRESHOLD, speed__lte = HIGH_SPEED_THRESHOLD)
    serializer_class = TrafficReadingsSerializer

# 5 - LOW INTENSITY TRAFFIC READINGS
class LowIntensityTrafficReadingsView(ListAPIView):
    queryset = TrafficReadings.objects.filter(speed__gt = HIGH_SPEED_THRESHOLD)
    serializer_class = TrafficReadingsSerializer

# 6 - CREATE TRAFFIC READING (only for admin use)
class CreateTrafficReadingView(CreateAPIView):
    queryset = TrafficReadings.objects.all()
    serializer_class = CreateTrafficReadingSerializer
    
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        return [IsAnonymousReadOnly()]



## ROAD SEGMENTS ------------------------------------------------------------------------------------------------
# 7 - ALL ROAD SEGMENTS
class RoadSegmentsView(ListAPIView):
    queryset = RoadSegments.objects.all()
    serializer_class = RoadSegmentsSerializer

# 8 - UPDATE OR DELETE INDIVIDUAL ROAD SEGMENTS (only for admin use)
class RoadSegmentsUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = RoadSegments.objects.all()
    serializer_class = RoadSegmentsSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        traffic_readings = instance.trafficreadings_set.all()
        traffic_readings_serializer = TrafficReadingsSerializer(traffic_readings, many=True)
        
        return Response({'road_segment': serializer.data, 'traffic_readings': traffic_readings_serializer.data})
    
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        return [IsAnonymousReadOnly()]

# 9 - HIGH INTENSITY ROAD SEGMENTS
class HighIntensityRoadSegmentsView(ListAPIView):
    def get_queryset(self):
        # Get the latest TrafficReading for each RoadSegment
        latest_readings = TrafficReadings.objects.filter(id=OuterRef('pk')).order_by('-id')
        
        # Get all road segments where the latest traffic reading has high intensity
        high_intensity_road_segments = RoadSegments.objects.annotate(latest_reading_id=Subquery(latest_readings.values('id')[:1])
        ).filter(Q(trafficreadings__id=F('latest_reading_id')) & Q(trafficreadings__speed__lte=LOW_SPEED_THRESHOLD))
        
        return high_intensity_road_segments

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Serialize the road segments
        serializer = RoadSegmentsSerializer(queryset, many=True)
        return Response(serializer.data)

# 10 - MEDIUM INTENSITY ROAD SEGMENTS
class MediumIntensityRoadSegmentsView(ListAPIView):
    def get_queryset(self):
        # Get the latest TrafficReading for each RoadSegment
        latest_readings = TrafficReadings.objects.filter(id=OuterRef('pk')).order_by('-id')
        
        # Get all road segments where the latest traffic reading has medium intensity
        medium_intensity_road_segments = RoadSegments.objects.annotate(latest_reading_id=Subquery(latest_readings.values('id')[:1])
        ).filter(Q(trafficreadings__id=F('latest_reading_id')) & Q(trafficreadings__speed__gt = LOW_SPEED_THRESHOLD, trafficreadings__speed__lte = HIGH_SPEED_THRESHOLD))
        
        return medium_intensity_road_segments

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Serialize the road segments
        serializer = RoadSegmentsSerializer(queryset, many=True)
        return Response(serializer.data)

# 11 - LOW INTENSITY ROAD SEGMENTS
class LowIntensityRoadSegmentsView(ListAPIView):
    def get_queryset(self):
        # Get the latest TrafficReading for each RoadSegment
        latest_readings = TrafficReadings.objects.filter(id=OuterRef('pk')).order_by('-id')
        
        # Get all road segments where the latest traffic reading has low intensity
        low_intensity_road_segments = RoadSegments.objects.annotate(latest_reading_id=Subquery(latest_readings.values('id')[:1])
        ).filter(Q(trafficreadings__id=F('latest_reading_id')) & Q(trafficreadings__speed__gt = HIGH_SPEED_THRESHOLD))
        
        return low_intensity_road_segments

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Serialize the road segments
        serializer = RoadSegmentsSerializer(queryset, many=True)
        return Response(serializer.data)

# 12 - CREATE ROAD SEGMENT (only for admin use)
class CreateRoadSegmentView(CreateAPIView):
    queryset = RoadSegments.objects.all()
    serializer_class = CreateRoadSegmentSerializer
    
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        return [IsAnonymousReadOnly()]


## SENSORS ------------------------------------------------------------------------------------------------------
# 13 - ALL SENSORS
class SensorsView(ListAPIView):
    queryset = Sensors.objects.all()
    serializer_class = SensorsSerializer

# 14 - UPDATE OR DELETE INDIVIDUAL SENSORS (only for admin use)
class SensorsUpdateView(RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        return [IsAnonymousReadOnly()]
    
    queryset = Sensors.objects.all()
    serializer_class = SensorsSerializer

# 15 - ALL SENSOR READINGS
class SensorReadingsView(ListAPIView):
    queryset = SensorReadings.objects.all()
    serializer_class = SensorReadingsSerializer

# 16 - UPDATE OR DELETE INDIVIDUAL SENSOR READINGS (only for admin use)
class SensorReadingsUpdateView(RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        return [IsAnonymousReadOnly()]
    
    queryset = SensorReadings.objects.all()
    serializer_class = SensorReadingsSerializer

# 17 - CREATE NEW SENSOR READING (for admin use only)
class CreateSensorReadingView(CreateAPIView):
    query_set = SensorReadings.objects.all()
    serializer_class = CreateSensorReadingSerializer
    permission_classes = [IsAdminOrReadOnly]



## CARS ---------------------------------------------------------------------------------------------------------
# 18 - ALL CARS
class CarsView(ListAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer

# 19 - INDIVIDUAL CARS
class CarDetailsView(RetrieveAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        return [IsAnonymousReadOnly()]
    
    def get(self, request, car_license_plate, *args, **kwargs):
        license_plate = car_license_plate
        cars = Cars.objects.filter(Q(car_license_plate__icontains=license_plate))
        serializer = CarsSerializer(cars, many=True)
        
        car_instance = cars.first()
        
        # Filter sensor readings for the last 24 hours
        cutoff_time = timezone.now() - timedelta(hours=24)
        sensor_readings = car_instance.sensorreadings_set.filter(timestamp__gte=cutoff_time)
        sensor_readings_serializer = SensorReadingsSerializer(sensor_readings, many=True)

        # Extract road segment and sensor IDs from the filtered sensor readings
        road_segment_ids = sensor_readings.values_list('road_segment_id', flat=True).distinct()
        sensor_ids = sensor_readings.values_list('sensor_uuid', flat=True).distinct()

        # Retrieve related road segments and sensors for the last 24 hours
        road_segments_data = RoadSegments.objects.filter(id__in=road_segment_ids)
        road_segments_serializer = RoadSegmentsSerializer(road_segments_data, many=True)

        sensors_data = Sensors.objects.filter(id__in=sensor_ids)
        sensors_serializer = SensorsSerializer(sensors_data, many=True)
        
        return Response({
            'car': serializer.data,
            'sensor_readings': sensor_readings_serializer.data,
            'sensors': sensors_serializer.data,
            'road_segments': road_segments_serializer.data,
        })