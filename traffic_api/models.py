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


# 3 - SENSORS -----------------------------------------------------------------------------------------------------
class Sensors(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    uuid = UUIDField()
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Get the latest id from existing recordings and increment by 1
            last_route = Sensors.objects.order_by('-id').first()
            if last_route:
                self.id = last_route.id + 1
            else:
                self.id = 1
            super(Sensors, self).save(*args, **kwargs)


# 4 - CARS --------------------------------------------------------------------------------------------------------
class Cars(Model):
    id = AutoField(primary_key=True)
    car_license_plate = CharField(max_length=6)
    created_at = DateTimeField()
    
    @property
    def sensor_readings(self):
        return SensorReadings.objects.filter(car_license_plate=self.value)
    
    def __str__(self):
        return str(self.car_license_plate)


# 5 - SENSOR READINGS ---------------------------------------------------------------------------------------------
class SensorReadings(Model):
    id = AutoField(primary_key=True)
    road_segment_id = ForeignKey(RoadSegments, on_delete=CASCADE)
    car_license_plate = ForeignKey(Cars, on_delete=CASCADE)
    timestamp = DateTimeField()
    sensor_uuid = ForeignKey(Sensors, on_delete=CASCADE)
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Get the latest id from existing recordings and increment by 1
            last_route = SensorReadings.objects.order_by('-id').first()
            if last_route:
                self.id = last_route.id + 1
            else:
                self.id = 1
            super(SensorReadings, self).save(*args, **kwargs)