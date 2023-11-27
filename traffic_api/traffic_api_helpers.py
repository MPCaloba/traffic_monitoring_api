# Not sure how would the threshold changes would be made in the future so I established them as env variables in settings.py
from traffic_monitoring_api.settings import LOW_SPEED_THRESHOLD, HIGH_SPEED_THRESHOLD

def get_intensity(speed):
    if speed is not None:
        if speed <= LOW_SPEED_THRESHOLD:
            intensity = "High"
        elif speed > LOW_SPEED_THRESHOLD and speed <= HIGH_SPEED_THRESHOLD:
            intensity = "Medium"
        else:
            intensity = "Low"
        return intensity
    else:
        return 'No Data'