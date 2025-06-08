"""
Serializers for the PhD Students app.

This file contains serializers that convert PhDStudent model instances into JSON representations
and vice versa, enabling API functionality for the phd_students app.
"""

from rest_framework import serializers
from phd_students.models import PhDStudent

class PhDStudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the PhDStudent model.
    
    This serializer handles the conversion between PhDStudent model instances and their
    JSON representation. It includes all fields from the PhDStudent model and adds
    additional computed fields for related data.
    """
    
    # Computed fields for related objects
    supervisor_name = serializers.SerializerMethodField()
    research_group_name = serializers.SerializerMethodField()
    
    class Meta:
        """
        Meta class to specify model and fields for the serializer.
        """
        model = PhDStudent
        fields = [
            'id', 'title', 'name', 'research_group', 'supervisor',
            'enrollment_date', 'image_url', 'supervisor_name', 'research_group_name'
        ]
    
    def get_supervisor_name(self, obj):
        """Return the name of the supervisor professor."""
        if obj.supervisor:
            return obj.supervisor.name
        return None
    
    def get_research_group_name(self, obj):
        """Return the name of the research group this student belongs to."""
        if obj.research_group:
            return obj.research_group.name
        return None

class PhDStudentListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for PhDStudent list views.
    
    This serializer includes only the essential fields needed for list displays,
    optimizing performance by reducing data transfer.
    """
    
    # Include supervisor and research group names directly in the list view
    supervisor_name = serializers.SerializerMethodField()
    research_group_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PhDStudent
        fields = ['id', 'title', 'name', 'supervisor_name', 'research_group_name']  # Only essential fields
    
    def get_supervisor_name(self, obj):
        """Return the name of the supervisor professor."""
        if obj.supervisor:
            return obj.supervisor.name
        return None
    
    def get_research_group_name(self, obj):
        """Return the name of the research group this student belongs to."""
        if obj.research_group:
            return obj.research_group.name
        return None

# MOOChub compatible serializer for PhD Students
class MOOChubPhDStudentSerializer(serializers.ModelSerializer):
    """
    Serializer specifically formatted for MOOChub API compatibility.
    
    This serializer maps our internal PhDStudent model fields to the field names and
    structure expected by the MOOChub schema for interoperability with other platforms.
    """
    
    # MOOChub specific field mappings
    type = serializers.SerializerMethodField()
    honorificPrefix = serializers.CharField(source='title')
    affiliation = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    mentor = serializers.SerializerMethodField()
    
    class Meta:
        model = PhDStudent
        fields = [
            'id', 'type', 'name', 'honorificPrefix', 
            'affiliation', 'image', 'mentor', 'enrollment_date'
        ]
    
    def get_type(self, obj):
        """Return the type of resource according to MOOChub schema."""
        return "Person"
    
    def get_affiliation(self, obj):
        """Return affiliation information in MOOChub format."""
        if obj.research_group:
            return {
                "type": "Organization",
                "name": obj.research_group.name
            }
        return {
            "type": "Organization",
            "name": "German University of Digital Science"
        }
    
    def get_image(self, obj):
        """Return image information in MOOChub format."""
        if obj.image_url:
            return {
                "type": "ImageObject",
                "contentUrl": obj.image_url,
            }
        return None
    
    def get_mentor(self, obj):
        """Return supervisor information in MOOChub format."""
        if obj.supervisor:
            return {
                "type": "Person",
                "name": obj.supervisor.name,
                "honorificPrefix": obj.supervisor.title if hasattr(obj.supervisor, 'title') else ""
            }
        return None
