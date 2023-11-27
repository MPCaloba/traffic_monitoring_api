from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, PrimaryKeyRelatedField, FloatField
from django.utils import timezone
from django.db.models import DateTimeField
from .models import RoadSegments, TrafficReadings
from .traffic_api_helpers import get_intensity


## TRAFFIC READINGS -----------------------------------------------------------------------------------------
# 1 - GET TRAFFIC READINGS AND INTENSITY
class TrafficReadingsSerializer(ModelSerializer):
    road_segment_id = PrimaryKeyRelatedField(queryset=RoadSegments.objects.all())
    intensity = SerializerMethodField()
    
    def get_intensity(self, obj):
        return get_intensity(obj.speed)
    
    class Meta:
        model = TrafficReadings
        fields = ['id', 'intensity', 'speed', 'road_segment_id']

# 2 - CREATE TRAFFIC READINGS
class CreateTrafficReadingSerializer(ModelSerializer):
    speed = FloatField()
    road_segment_id = PrimaryKeyRelatedField(queryset=RoadSegments.objects.all())
    
    class Meta:
        model = TrafficReadings
        fields = ['id', 'speed', 'road_segment_id']
    
    # Override the create function so the intensity property is not involved when creating a new instance
    def create(self, validated_data):
        # Removes the ‘speed’ and ‘road_segment_id’ fields from the validated data
        speed = validated_data.pop('speed')
        road_segment_id = validated_data.pop('road_segment_id')
        
        # Create a new instance just with these speed and road_segment_id
        new_traffic_reading = TrafficReadings.objects.create(speed=speed, road_segment_id=road_segment_id)
        return new_traffic_reading


## ROAD SEGMENTS --------------------------------------------------------------------------------------------
# 3 - GET ROAD SEGMENTS
class RoadSegmentsSerializer(ModelSerializer):
    traffic_readings = TrafficReadingsSerializer(many=True, read_only=True)
    traffic_readings_count = SerializerMethodField()
    
    def get_traffic_readings_count(self, obj):
        count = obj.trafficreadings_set.count()
        return count
    
    class Meta:
        model = RoadSegments
        fields = ['id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length', 'traffic_readings_count', 'traffic_readings']

# 4 - CREATE ROAD SEGMENTS
class CreateRoadSegmentSerializer(ModelSerializer):
    class Meta:
        model = RoadSegments
        fields = ['id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length']