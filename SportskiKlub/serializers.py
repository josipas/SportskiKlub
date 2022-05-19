from rest_framework import serializers
from SportskiKlub.models import Coach, Location, Group, Term


class GroupSerializer(serializers.Serializer):
    groupId = serializers.CharField(required=True)
    coachId = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    location = serializers.ModelSerializer(instance=Location)
    term = serializers.CharField(required=True)

class GroupResponsePostSerializer(serializers.Serializer):
    groupId = serializers.CharField(required=True)

class GroupPostSerializer(serializers.Serializer):
    coachId = serializers.CharField(required=True)
    locationId = serializers.CharField(required=True)
    termId = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

class GroupUpdateSerializer(serializers.Serializer):
    locationId = serializers.CharField(required=True)
    termId = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

class CoachSerializer(serializers.Serializer):
    coachId = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    groups = serializers.JSONField(required=True)
    locations = serializers.ListField(required=True)

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

