from django.db.models import Model, FloatField, AutoField, DateTimeField, CharField, UUIDField, ForeignKey, CASCADE
from .traffic_api_helpers import get_intensity


# 1 - ROAD SEGMENTS -----------------------------------------------------------------------------------------------
class RoadSegments(Model):
    id = AutoField(primary_key=True)
    long_start = FloatField()
    lat_start = FloatField()
    long_end = FloatField()
    lat_end = FloatField()
    length = FloatField()
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Get the latest id from existing recordings and increment by 1
            last_route = RoadSegments.objects.order_by('-id').first()
            if last_route:
                self.id = last_route.id + 1
            else:
                self.id = 1
            super(RoadSegments, self).save(*args, **kwargs)


# 2 - TRAFFIC READINGS --------------------------------------------------------------------------------------------
class TrafficReadings(Model):
    id = AutoField(primary_key=True)
    speed = FloatField(null=True, blank=True)
    road_segment_id = ForeignKey(RoadSegments, on_delete=CASCADE)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def intensity(self):
        return self.get_intensity(self.speed)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Get the latest id from existing recordings and increment by 1
            last_route = TrafficReadings.objects.order_by('-id').first()
            if last_route:
                self.id = last_route.id + 1
            else:
                self.id = 1
        super(TrafficReadings, self).save(*args, **kwargs)