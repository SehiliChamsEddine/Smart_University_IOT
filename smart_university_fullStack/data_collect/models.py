from django.db import models

# Create your models here.


class ControlSettingsPublish(models.Model):
    water_pump_status = models.BooleanField(default=False)
    block1_status = models.BooleanField(default=False)
    block2_status = models.BooleanField(default=False)
    block3_status = models.BooleanField(default=False)
    

    def __str__(self):
        return "Control Settings"
    
class ControlSettingsRecive(models.Model):
    water_pump_status = models.BooleanField(default=False)
    block1_status = models.BooleanField(default=False)
    block2_status = models.BooleanField(default=False)
    block3_status = models.BooleanField(default=False)
    fire_detection = models.BooleanField(default=False)
    gas_detection = models.BooleanField(default=False)

    def __str__(self):
        return "Control Settings"
class Tempurature(models.Model):
    tempurature = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
class Himidity(models.Model):
    himidity = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
class WaterLevel(models.Model):
    waterlevel = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)