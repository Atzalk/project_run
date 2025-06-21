from rest_framework import serializers
from .models import Run, User


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'


class UserSerializerForRun(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'

    athlete_data = UserSerializerForRun(read_only=True, source='athlete')
