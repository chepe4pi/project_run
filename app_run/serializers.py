from django.contrib.auth.models import User

from rest_framework import serializers

from app_run.models import Run

class RunUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = RunUserSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'first_name', 'last_name', 'type']

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        return 'athlete'
