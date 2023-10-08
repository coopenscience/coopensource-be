from rest_framework import serializers
from .models import User, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'bio', 'category']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'project_name', 
            'project_url_on_catalog', 
            'project_url_external', 
            'project_description', 
            'keywords', 
            'fields_of_science', 
            'project_status', 
            'agency_sponsor', 
            'agency_sponsor_other', 
            'geographic_scope', 
            'participant_age', 
            'project_goals', 
            'participation_tasks', 
            'scistarter', 
            'email', 
            'start_date'
        ]
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    