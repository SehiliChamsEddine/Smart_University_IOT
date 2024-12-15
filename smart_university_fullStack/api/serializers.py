from rest_framework import serializers
from data_collect.models import ControlSettingsPublish ,ControlSettingsRecive

class ControlSettingsPublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlSettingsPublish
        fields = [
            'water_pump_status',
            'block1_status',
            'block2_status',
            'block3_status',
           
        
           
        ]
class ControlSettingsReciveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlSettingsRecive
        fields = [
           'water_pump_status',
            'block1_status',
            'block2_status',
            'block3_status',
            'fire_detection',
            'gas_detection',
            
        ]
