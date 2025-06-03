"""
Serializers for the Professors app.

This file contains serializers that convert Professor model instances into JSON representations
and vice versa, enabling API functionality for the professors app.
"""

from rest_framework import serializers
from professors.models import Professor

class ProfessorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Professor model.
    
    This serializer handles the conversion between Professor model instances and their
    JSON representation. It includes all fields from the Professor model and adds
    additional computed fields for related data.
    """
    
    # Computed fields for related objects
    research_group_name = serializers.SerializerMethodField()
    leads_research_group_name = serializers.SerializerMethodField()
    
    class Meta:
        """
        Meta class to specify model and fields for the serializer.
        """
        model = Professor
        fields = [
            'id', 'title', 'name', 'position', 'bio', 'image_url',
            'research_group', 'leads_research_group',
            'research_group_name', 'leads_research_group_name'
        ]
    
    def get_research_group_name(self, obj):
        """Return the name of the research group this professor belongs to."""
        if obj.research_group:
            return obj.research_group.name
        return None
    
    def get_leads_research_group_name(self, obj):
        """Return the name of the research group this professor leads."""
        if obj.leads_research_group:
            return obj.leads_research_group.name
        return None

class ProfessorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Professor list views.
    
    This serializer includes only the essential fields needed for list displays,
    optimizing performance by reducing data transfer.
    """
    
    research_group_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Professor
        fields = ['id', 'title', 'name', 'position', 'research_group_name']  # Only essential fields
    
    def get_research_group_name(self, obj):
        """Return the name of the research group this professor belongs to."""
        if obj.research_group:
            return obj.research_group.name
        return None

# MOOChub compatible serializer for professors as instructors
class MOOChubPersonSerializer(serializers.ModelSerializer):
    """
    Serializer specifically formatted for MOOChub API compatibility.
    
    This serializer maps our internal Professor model fields to the field names and
    structure expected by the MOOChub schema for interoperability with other platforms.
    """
    
    # MOOChub specific field mappings
    type = serializers.SerializerMethodField()
    honorificPrefix = serializers.CharField(source='title')
    description = serializers.CharField(source='bio')
    image = serializers.SerializerMethodField()
    affiliation = serializers.SerializerMethodField()
    
    class Meta:
        model = Professor
        fields = [
            'id', 'type', 'name', 'honorificPrefix', 
            'description', 'image', 'affiliation'
        ]
    
    def get_type(self, obj):
        """Return the type of resource according to MOOChub schema."""
        return "Person"
    
    def get_image(self, obj):
        """Return image information in MOOChub format."""
        if obj.image_url:
            return {
                "type": "ImageObject",
                "contentUrl": obj.image_url,
            }
        return None
    
    def get_affiliation(self, obj):
        """Return affiliation information in MOOChub format."""
        # Return the research group as the affiliation if available
        if obj.research_group:
            return {
                "type": "Organization",
                "name": obj.research_group.name
            }
        # Otherwise return a default organization
        return {
            "type": "Organization",
            "name": "German University of Digital Science"
        }
